"""
This file registers the model with the Python SDK.
"""

from viam.components.generic import Generic
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .module import HeartBeatModule

Registry.register_resource_creator(Generic.SUBTYPE, HeartBeatModule.MODEL, ResourceCreatorRegistration(HeartBeatModule.new, HeartBeatModule.validate))
