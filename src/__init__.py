"""
This file registers the model with the Python SDK.
"""

from viam.components.sensor import Sensor
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .pms7003 import pms7003

Registry.register_resource_creator(Sensor.SUBTYPE, pms7003.MODEL, ResourceCreatorRegistration(pms7003.new, pms7003.validate))
