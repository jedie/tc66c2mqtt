import asyncio
import dataclasses
import datetime
import json
import time
from pathlib import Path

import rich_click as click
from cli_base.cli_tools.verbosity import OPTION_KWARGS_VERBOSE, setup_logging
from rich import print  # noqa

from tc66c2mqtt.cli_app import cli
from tc66c2mqtt.constants import DEFAULT_DEVICE_NAME
from tc66c2mqtt.data_classes import TC66PollData
from tc66c2mqtt.tc66c import Tc66c
from tc66c2mqtt.tc66c_bluetooth import poll


class FileWriter:
    def __init__(self, count: int):
        self.count = count

    def __enter__(self):
        return self

    def __call__(self, *, crypted_data: bytes, decoded_data: bytes, parsed_data: TC66PollData):
        tc66c = Tc66c.from_bytes(decoded_data)

        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')

        raw_out_path = Path(f'tc66c_{timestamp}_raw.bin')
        raw_out_path.write_bytes(crypted_data)

        decoded_out_path = Path(f'tc66c_{timestamp}_decoded.bin')
        decoded_out_path.write_bytes(decoded_data)

        parsed_out_path = Path(f'tc66c_{timestamp}_parsed.json')
        parsed_data = dataclasses.asdict(parsed_data)
        json_data = json.dumps(parsed_data, indent=4, sort_keys=True)
        parsed_out_path.write_text(json_data)

        print(f'{self.count:02} wrote {timestamp} files...', tc66c.unknown.hex())
        self.count -= 1
        if self.count <= 0:
            print('Done writing files')
            raise SystemExit(0)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            return False


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
@click.option(
    '--device-name',
    default=DEFAULT_DEVICE_NAME,
    show_default=True,
    help='Bluetooth device name',
)
@click.option(
    '--count',
    default=10,
    show_default=True,
    help='Number of files to write',
)
def write(verbosity: int, device_name: str, count: int):
    """
    Write files from TC66C data to disk.
    """
    setup_logging(verbosity=verbosity)

    with FileWriter(count=count) as file_writer:
        while file_writer.count > 0:
            try:
                asyncio.run(poll(device_name=device_name, poll_callback=file_writer))
            except Exception as e:
                print(f'Error: {e}')
                print('Retrying in 1 second...')
                time.sleep(1)
