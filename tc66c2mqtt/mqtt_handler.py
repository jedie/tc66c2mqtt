import logging

from ha_services.mqtt4homeassistant.components.sensor import Sensor
from ha_services.mqtt4homeassistant.device import MainMqttDevice, MqttDevice
from ha_services.mqtt4homeassistant.mqtt import get_connected_client

import tc66c2mqtt
from tc66c2mqtt.data_classes import TC66PollData
from tc66c2mqtt.user_settings import UserSettings


logger = logging.getLogger(__name__)


class Tc66cMqttHandler:
    def __init__(self, user_settings: UserSettings, verbosity: int):
        self.user_settings = user_settings
        self.device_name = user_settings.device_name

        self.mqtt_client = get_connected_client(settings=user_settings.mqtt, verbosity=verbosity)
        self.mqtt_client.loop_start()

        self.main_device = None

    def init_device(self, *, parsed_data: TC66PollData):
        self.main_device = MainMqttDevice(
            name='TC66C 2 MQTT',
            uid=str(parsed_data.serial),
            manufacturer='tc66c2mqtt',
            sw_version=tc66c2mqtt.__version__,
            config_throttle_sec=self.user_settings.mqtt.publish_config_throttle_seconds,
        )
        self.mqtt_device = MqttDevice(
            main_device=self.main_device,
            name=self.device_name,
            uid=str(parsed_data.serial),
            manufacturer='RDTech',
            sw_version=parsed_data.version,
            config_throttle_sec=self.user_settings.mqtt.publish_config_throttle_seconds,
        )
        self.voltage = Sensor(
            device=self.mqtt_device,
            name='Voltage',
            uid='voltage',
            device_class='voltage',
            state_class='measurement',
            unit_of_measurement='V',
            suggested_display_precision=3,
        )
        self.current = Sensor(
            device=self.mqtt_device,
            name='Current',
            uid='current',
            device_class='current',
            state_class='measurement',
            unit_of_measurement='A',
            suggested_display_precision=3,
        )
        self.power = Sensor(
            device=self.mqtt_device,
            name='Power',
            uid='power',
            device_class='power',
            state_class='measurement',
            unit_of_measurement='W',
            suggested_display_precision=3,
        )

    def __call__(self, *, parsed_data: TC66PollData):
        print(parsed_data)

        if self.main_device is None:
            self.init_device(parsed_data=parsed_data)

        self.main_device.poll_and_publish(self.mqtt_client)

        self.voltage.set_state(parsed_data.voltage)
        self.voltage.publish(self.mqtt_client)

        self.current.set_state(parsed_data.current)
        self.current.publish(self.mqtt_client)

        self.power.set_state(parsed_data.power)
        self.power.publish(self.mqtt_client)
