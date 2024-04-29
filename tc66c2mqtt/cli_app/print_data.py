import asyncio
import time

from bleak import AdvertisementData, BleakClient, BleakGATTCharacteristic, BleakScanner, BLEDevice

import rich_click as click
from cli_base.cli_tools.verbosity import OPTION_KWARGS_VERBOSE, setup_logging
from rich import print  # noqa
from tc66c2mqtt.cli_app import cli
from tc66c2mqtt.constants import BLEAK_CLIENT_TIMEOUT

from tc66c2mqtt.tc66 import parse_tc66_packet
from tc66c2mqtt.tc66_decryptor import tc66_decryptor

ASK_FOR_VALUES_COMMAND = bytearray(b'bgetva\r\n')

# Firmware >= 1.15
RX_CHARACTERISTIC_UUID = '0000ffe1-0000-1000-8000-00805f9b34fb'
TX_CHARACTERISTIC_UUID = '0000ffe2-0000-1000-8000-00805f9b34fb'

DEVICE_NAME = 'BT24-M'


def service_notification_handler(sender, data: bytearray):
    length = len(data)
    if length != 192:
        print(f'Wrong data: {length=} is not 192!')
        print(data)

    decoded_data = tc66_decryptor(crypted_data=data)
    if parsed_data := parse_tc66_packet(decoded_data):
        print(parsed_data)
    else:
        print('Error parsing data:', decoded_data)


async def device_info(device: BLEDevice):
    print(f'Connect to {device}...', flush=True, end='')

    async with BleakClient(device, timeout=BLEAK_CLIENT_TIMEOUT) as client:
        print('connected.')
        print(f'{client.services.services=}')

        tx_characteristic: BleakGATTCharacteristic = client.services.get_characteristic(
            specifier=TX_CHARACTERISTIC_UUID
        )
        print(f'tx_characteristic: {tx_characteristic}')
        print(f'{tx_characteristic.properties=}')

        rx_characteristic: BleakGATTCharacteristic = client.services.get_characteristic(
            specifier=RX_CHARACTERISTIC_UUID
        )
        print(f'rx_characteristic: {rx_characteristic}')
        print(f'{rx_characteristic.properties=}')

        try:
            count = 0
            while True:
                count += 1
                print(f'poll {count}...', flush=True, end='')
                await client.write_gatt_char(char_specifier=tx_characteristic, data=ASK_FOR_VALUES_COMMAND)
                await client.start_notify(char_specifier=rx_characteristic, callback=service_notification_handler)
                time.sleep(1)
        finally:
            print('stop notify')
            await client.stop_notify(char_specifier=rx_characteristic)


async def main():
    async with BleakScanner() as scanner:
        seen_addresses = set()
        print('Scanning...\n')

        async for device, advertisement_data in scanner.advertisement_data():
            device: BLEDevice
            advertisement_data: AdvertisementData

            if device.address in seen_addresses:
                continue

            seen_addresses.add(device.address)

            print('New device found:', device)
            print()
            print(advertisement_data)
            print()

            if device.name != DEVICE_NAME:
                print('skipped.')
            else:
                await device_info(device)

        print('Scan complete.')


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
def print_data(verbosity: int):
    """
    discover Bluetooth devices that can be connected to
    """

    # Bus 003 Device 014: ID 28e9:018a GDMicroelectronics TC66 USB Type-C Meter

    setup_logging(verbosity=verbosity)

    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            print(f'Error: {e}')
            print('Retrying in 1 second...')
            time.sleep(1)
