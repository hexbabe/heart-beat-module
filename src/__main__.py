import asyncio
import sys

from viam.module.module import Module
from viam.components.generic import Generic
from viam.services.vision import Vision
from .fake_vision import FakeVision
from .heartbeat import HeartBeatModule

async def main():
    module = Module.from_args()
    module.add_model_from_registry(Generic.API, HeartBeatModule.MODEL)
    module.add_model_from_registry(Vision.API, FakeVision.MODEL)
    await module.start()

if __name__ == "__main__":
    asyncio.run(main())
