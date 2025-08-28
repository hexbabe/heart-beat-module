"""
This file registers the model with the Python SDK.
"""

from viam.components.generic import Generic
from viam.resource.registry import Registry, ResourceCreatorRegistration
from viam.services.vision import Vision

from .heartbeat import HeartBeatModule
from .fake_vision import FakeVision

Registry.register_resource_creator(Generic.API, HeartBeatModule.MODEL, ResourceCreatorRegistration(HeartBeatModule.new, HeartBeatModule.validate))
Registry.register_resource_creator(Vision.API, FakeVision.MODEL, ResourceCreatorRegistration(FakeVision.new_service, FakeVision.validate_config))
