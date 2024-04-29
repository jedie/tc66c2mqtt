import asyncio
import time

import rich_click as click
from cli_base.cli_tools.verbosity import OPTION_KWARGS_VERBOSE, setup_logging
from rich import print  # noqa

from tc66c2mqtt.cli_app import cli
from tc66c2mqtt.constants import DEFAULT_DEVICE_NAME
from tc66c2mqtt.data_classes import TC66PollData
from tc66c2mqtt.tc66c_bluetooth import poll


def poll_callback(*, parsed_data: TC66PollData):
    print(parsed_data)


@cli.command()
@click.option('-v', '--verbosity', **OPTION_KWARGS_VERBOSE)
@click.option(
    '--device-name',
    default=DEFAULT_DEVICE_NAME,
    show_default=True,
    help='Bluetooth device name',
)
def print_data(verbosity: int, device_name: str):
    """
    Print TC66C data to console
    """
    setup_logging(verbosity=verbosity)

    while True:
        try:
            asyncio.run(
                poll(
                    device_name=device_name,
                    poll_callback=poll_callback,
                )
            )
        except Exception as e:
            print(f'Error: {e}')
            print('Retrying in 1 second...')
            time.sleep(1)
