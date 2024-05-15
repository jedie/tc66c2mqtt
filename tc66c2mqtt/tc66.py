import logging

from tc66c2mqtt.data_classes import TC66PollData

logger = logging.getLogger(__name__)


def parse_bytes(data: bytes, scale: float | None = None):
    """
    >>> parse_bytes(b'\\x01\\x00', 1)
    1.0
    >>> parse_bytes(b'\\x02\\x00\\x00\\x00', 1000)
    0.002
    >>> parse_bytes(b'\\x03\\x00')
    3
    """
    value = int.from_bytes(data, 'little')
    if scale is None:
        return value
    return float(value) / scale


def validate_prefix(data: bytes, prefix: str):
    """
    >>> validate_prefix(b'pac1data', 'pac1')
    True
    >>> validate_prefix(b'foobar', 'pac1')
    False
    """
    return data[:4] == prefix.encode()


def parse_tc66_packet(data: bytes) -> TC66PollData | None:
    """
    https://sigrok.org/wiki/RDTech_TC66C#Protocol_response_format_(%22Poll_data%22)
    """
    pac1, pac2, pac3 = data[:64], data[64:128], data[128:192]

    if not all([validate_prefix(pac, f'pac{i}') for i, pac in enumerate([pac1, pac2, pac3], start=1)]):
        logger.error('Invalid prefixes!')
        return None

    ###################################################################
    # pac1 values:

    product_name = pac1[4:8].decode('utf-8')  # Product name, e.g.: "TC66"
    version = pac1[8:12].decode('utf-8')  # Version (e.g., 1.14)
    serial = parse_bytes(pac1[12:16])

    number_of_runs = parse_bytes(pac1[44:48])

    voltage = parse_bytes(pac1[48:52], scale=10_000)
    current = parse_bytes(pac1[52:56], scale=100_000)
    power = parse_bytes(pac1[56:60], scale=10_000)

    # Compare V * A = W ;)
    power_calc = voltage * current
    diff = abs(power - power_calc)
    if diff > 0.0002:
        logger.warning(f'Power calculation diff: {power=}, {power_calc=} ({diff=})')

    # pac1[60:64] contains CRC16/MODBUS

    ###################################################################
    # pac2 values:

    resistor = parse_bytes(pac2[4:8], scale=10)

    group0Ah = parse_bytes(pac2[8:12], scale=1_000)
    group0Wh = parse_bytes(pac2[12:16], scale=1_000)

    group1Ah = parse_bytes(pac2[16:20], scale=1_000)
    group1Wh = parse_bytes(pac2[20:24], scale=1_000)

    temperature_sign = parse_bytes(pac2[24:28])
    temperature = parse_bytes(pac2[28:32])
    if temperature_sign:
        temperature = -temperature

    data_plus = parse_bytes(pac2[32:36], scale=100)
    data_minus = parse_bytes(pac2[36:40], scale=100)

    # pac2[40:60] contains unknown data -> ignore
    # pac2[60:64] contains CRC16/MODBUS

    ###################################################################
    # pac3 values:
    # pac3 = data[128:192] -> All data are unknown

    return TC66PollData(
        product_name=product_name,
        version=version,
        serial=serial,
        number_of_runs=number_of_runs,
        #
        voltage=voltage,
        current=current,
        power=power,
        #
        resistor=resistor,
        #
        group0Ah=group0Ah,
        group0Wh=group0Wh,
        group1Ah=group1Ah,
        group1Wh=group1Wh,
        #
        temperature=temperature,
        #
        data_plus=data_plus,
        data_minus=data_minus,
    )
