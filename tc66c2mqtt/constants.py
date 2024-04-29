from pathlib import Path

import tc66c2mqtt


CLI_EPILOG = 'Project Homepage: https://github.com/jedie/tc66c2mqtt'

BASE_PATH = Path(tc66c2mqtt.__file__).parent

BLEAK_CLIENT_TIMEOUT = 3
