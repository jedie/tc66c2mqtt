# tc66c2mqtt

[![tests](https://github.com/jedie/tc66c2mqtt/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/jedie/tc66c2mqtt/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/jedie/tc66c2mqtt/branch/main/graph/badge.svg)](https://app.codecov.io/github/jedie/tc66c2mqtt)
[![tc66c2mqtt @ PyPi](https://img.shields.io/pypi/v/tc66c2mqtt?label=tc66c2mqtt%20%40%20PyPi)](https://pypi.org/project/tc66c2mqtt/)
[![Python Versions](https://img.shields.io/pypi/pyversions/tc66c2mqtt)](https://github.com/jedie/tc66c2mqtt/blob/main/pyproject.toml)
[![License GPL-3.0-or-later](https://img.shields.io/pypi/l/tc66c2mqtt)](https://github.com/jedie/tc66c2mqtt/blob/main/LICENSE)

Send MQTT events from RDTech TC66C device

Tested with [Joy-IT TC66C](https://joy-it.net/de/products/JT-TC66C).


RDTech TC66C hardware info at sigrok:

 * https://sigrok.org/wiki/RDTech_TC66C


Used [Kaitai Struct](https://kaitai.io/) to parse the binary data from the TC66C device.
See: [tc66c.ksy](https://github.com/jedie/tc66c2mqtt/blob/main/tc66c2mqtt/tc66c.ksy)
and [tc66c.py](https://github.com/jedie/tc66c2mqtt/blob/main/tc66c2mqtt/tc66c.py).


## Bootstrap tc66c2mqtt

Clone the sources and just call the CLI to create a Python Virtualenv, e.g.:

```bash
~$ git clone https://github.com/jedie/tc66c2mqtt.git
~$ cd tc66c2mqtt
~/tc66c2mqtt$ ./cli.py --help
```
Output looks like:

[comment]: <> (✂✂✂ auto generated main help start ✂✂✂)
```
usage: ./cli.py [-h]
                {edit-settings,print-data,print-settings,publish-loop,scan,systemd-debug,systemd-remove,systemd-setup,
systemd-status,systemd-stop,update-readme-history,version,write}



╭─ options ──────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ -h, --help        show this help message and exit                                                                  │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ subcommands ──────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ {edit-settings,print-data,print-settings,publish-loop,scan,systemd-debug,systemd-remove,systemd-setup,systemd-stat │
│ us,systemd-stop,update-readme-history,version,write}                                                               │
│     edit-settings                                                                                                  │
│                   Edit the settings file. On first call: Create the default one.                                   │
│     print-data    Print TC66C data to console                                                                      │
│     print-settings                                                                                                 │
│                   Display (anonymized) MQTT server username and password                                           │
│     publish-loop  Print TC66C data to console                                                                      │
│     scan          Discover Bluetooth devices and there services/descriptors                                        │
│     systemd-debug                                                                                                  │
│                   Print Systemd service template + context + rendered file content.                                │
│     systemd-remove                                                                                                 │
│                   Remove Systemd service file. (May need sudo)                                                     │
│     systemd-setup                                                                                                  │
│                   Write Systemd service file, enable it and (re-)start the service. (May need sudo)                │
│     systemd-status                                                                                                 │
│                   Display status of systemd service. (May need sudo)                                               │
│     systemd-stop  Stops the systemd service. (May need sudo)                                                       │
│     update-readme-history                                                                                          │
│                   Update project history base on git commits/tags in README.md Will be exited with 1 if the        │
│                   README.md was updated otherwise with 0.                                                          │
│                                                                                                                    │
│                   Also, callable via e.g.:                                                                         │
│                       python -m cli_base update-readme-history -v                                                  │
│     version       Print version and exit                                                                           │
│     write         Write files from TC66C data to disk.                                                             │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated main help end ✂✂✂)


## Start hacking

Create dev virtualenv:

```bash
~$ git clone https://github.com/jedie/tc66c2mqtt.git
~$ cd tc66c2mqtt
~/tc66c2mqtt$ ./dev-cli.py --help
```
Output looks like:

[comment]: <> (✂✂✂ auto generated dev help start ✂✂✂)
```
usage: ./dev-cli.py [-h]
                    {check-code-style,coverage,fix-code-style,install,mypy,nox,pip-audit,publish,test,update,update-te
st-snapshot-files,version}



╭─ options ──────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ -h, --help        show this help message and exit                                                                  │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ subcommands ──────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ {check-code-style,coverage,fix-code-style,install,mypy,nox,pip-audit,publish,test,update,update-test-snapshot-file │
│ s,version}                                                                                                         │
│     check-code-style                                                                                               │
│                   Check code style by calling darker + flake8                                                      │
│     coverage      Run tests and show coverage report.                                                              │
│     fix-code-style                                                                                                 │
│                   Fix code style of all tc66c2mqtt source code files via darker                                    │
│     install       Install requirements and 'tc66c2mqtt' via pip as editable.                                       │
│     mypy          Run Mypy (configured in pyproject.toml)                                                          │
│     nox           Run nox                                                                                          │
│     pip-audit     Run pip-audit check against current requirements files                                           │
│     publish       Build and upload this project to PyPi                                                            │
│     test          Run unittests                                                                                    │
│     update        Update "requirements*.txt" dependencies files                                                    │
│     update-test-snapshot-files                                                                                     │
│                   Update all test snapshot files (by remove and recreate all snapshot files)                       │
│     version       Print version and exit                                                                           │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated dev help end ✂✂✂)



## Screenshots

### Home Assistant

![tc66c2mqtt 2024-05-15 at 22-17-52 zero2w3 – Home Assistant.png](https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/tc66c2mqtt/tc66c2mqtt%202024-05-15%20at%2022-17-52%20zero2w3%20%E2%80%93%20Home%20Assistant.png "tc66c2mqtt 2024-05-15 at 22-17-52 zero2w3 – Home Assistant.png")

### print data

test print data in terminal looks like:

```bash
~/tc66c2mqtt$ ./cli.py print-data
```

![2024-05-07_20-08_print_data.png](https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/tc66c2mqtt/2024-05-07_20-08_print_data.png "2024-05-07_20-08_print_data.png")


## History

[comment]: <> (✂✂✂ auto generated history start ✂✂✂)

* [v0.4.1](https://github.com/jedie/tc66c2mqtt/compare/v0.4.0...v0.4.1)
  * 2025-04-21 - Set min/max validation values in MQTT components of ha-services
* [v0.4.0](https://github.com/jedie/tc66c2mqtt/compare/v0.3.0...v0.4.0)
  * 2025-04-21 - Update README.md
  * 2025-04-21 - bugfix scan
  * 2025-04-21 - update CLI to tyro
  * 2025-04-21 - migrate pip-tools to uv
  * 2025-04-21 - Enhance scan
  * 2024-06-13 - typo: Not "Delta" it's "Data" voltage ;)
* [v0.3.0](https://github.com/jedie/tc66c2mqtt/compare/v0.2.0...v0.3.0)
  * 2024-06-12 - Expose Delta +/i and temperatur via MQTT, too.
* [v0.2.0](https://github.com/jedie/tc66c2mqtt/compare/v0.1.1...v0.2.0)
  * 2024-06-10 - Use Kaitai Struct and expose group Ah/Wh to MQTT add write command
  * 2024-06-10 - Fix some typos
  * 2024-05-31 - Update requirements
  * 2024-05-31 - print device info
  * 2024-05-15 - Simplify parsing TC66 data

<details><summary>Expand older history entries ...</summary>

* [v0.1.1](https://github.com/jedie/tc66c2mqtt/compare/v0.1.0...v0.1.1)
  * 2024-05-15 - README
  * 2024-05-15 - Update README.md
* [v0.1.0](https://github.com/jedie/tc66c2mqtt/compare/a912ba9...v0.1.0)
  * 2024-05-15 - Update requirements
  * 2024-05-15 - Handle TimeoutError seperate
  * 2024-05-15 - fix code style
  * 2024-05-15 - Expand MQTT sensors
  * 2024-05-07 - add screenshot
  * 2024-05-07 - Use rich "Progress" to display data on console
  * 2024-04-29 - Add initial state

</details>


[comment]: <> (✂✂✂ auto generated history end ✂✂✂)
