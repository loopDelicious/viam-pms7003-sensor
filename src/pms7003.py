from serial import Serial
from typing import ClassVar, Mapping, Sequence, Any, Dict, Optional, Tuple, Final, List, cast
from typing_extensions import Self
from typing import Any, Final, Mapping, Optional
from viam.utils import SensorReading
from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName, Vector3
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily
from viam.components.sensor import Sensor
from viam.logging import getLogger

import time
import asyncio

LOGGER = getLogger(__name__)

class PMS7003(Sensor, Reconfigurable):
    
    """
    Sensor represents a physical sensing device that can provide measurement readings.
    """
    
    MODEL: ClassVar[Model] = Model(ModelFamily("joyce", "air"), "pms7003")
    
    # create any class parameters here, 'some_pin' is used as an example (change/add as needed)
    some_pin: int

    # Constructor
    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        my_class = cls(config.name)
        my_class.reconfigure(config, dependencies)
        return my_class

    # Validates JSON Configuration
    @classmethod
    def validate(cls, config: ComponentConfig):
        # here we validate config, the following is just an example and should be updated as needed
        return

    # Handles attribute reconfiguration
    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        # here we initialize the resource instance, the following is just an example and should be updated as needed
        return

    """ Implement the methods the Viam RDK defines for the Sensor API (rdk:component:sensor) """

    
    async def get_readings(
        self, *, extra: Optional[Mapping[str, Any]] = None, timeout: Optional[float] = None, **kwargs
    ) -> Mapping[str, SensorReading]:
        """
        Obtain the measurements/data specific to this sensor.
        """

        port = Serial('/dev/ttyAMA0', baudrate=9600)

        def parse_data(data):
            if len(data) < 2:
                return {}
            if data[0] == 0x42 and data[1] == 0x4d:
                pm1_0_CF1 = (data[4] << 8) + data[5]
                pm2_5_CF1 = (data[6] << 8) + data[7]
                pm10_CF1 = (data[8] << 8) + data[9]
                pm1_0_atm = (data[10] << 8) + data[11]
                pm2_5_atm = (data[12] << 8) + data[13]
                pm10_atm = (data[14] << 8) + data[15]
                particles_03um = (data[16] << 8) + data[17]
                particles_05um = (data[18] << 8) + data[19]
                particles_10um = (data[20] << 8) + data[21]
                particles_25um = (data[22] << 8) + data[23]
                particles_50um = (data[24] << 8) + data[25]
                particles_100um = (data[26] << 8) + data[27]
                LOGGER.info(f'PM1.0 (CF=1): {pm1_0_CF1} µg/m3')
                LOGGER.info(f'PM2.5 (CF=1): {pm2_5_CF1} µg/m3')
                LOGGER.info(f'PM10 (CF=1): {pm10_CF1} µg/m3')
                LOGGER.info(f'PM1.0 (atmospheric): {pm1_0_atm} µg/m3')
                LOGGER.info(f'PM2.5 (atmospheric): {pm2_5_atm} µg/m3')
                LOGGER.info(f'PM10 (atmospheric): {pm10_atm} µg/m3')
                LOGGER.info(f'Particles > 0.3µm: {particles_03um} / 0.1L')
                LOGGER.info(f'Particles > 0.5µm: {particles_05um} / 0.1L')
                LOGGER.info(f'Particles > 1.0µm: {particles_10um} / 0.1L')
                LOGGER.info(f'Particles > 2.5µm: {particles_25um} / 0.1L')
                LOGGER.info(f'Particles > 5.0µm: {particles_50um} / 0.1L')
                LOGGER.info(f'Particles > 10µm: {particles_100um} / 0.1L')

                # return a dictionary of the readings
                return {
                    "pm1_0_CF1": pm1_0_CF1,
                    "pm2_5_CF1": pm2_5_CF1,
                    "pm10_CF1": pm10_CF1,
                    "pm1_0_atm": pm1_0_atm,
                    "pm2_5_atm": pm2_5_atm,
                    "pm10_atm": pm10_atm,
                    "particles_03um": particles_03um,
                    "particles_05um": particles_05um,
                    "particles_10um": particles_10um,
                    "particles_25um": particles_25um,
                    "particles_50um": particles_50um,
                    "particles_100um": particles_100um
                }

            else:
                LOGGER.info('Data does not start with the expected start bytes.')
                return {}

        while port.in_waiting == 0:
            time.sleep(0.01)  # wait for 10 ms

        data = port.read(port.in_waiting)
        return parse_data(data)
        