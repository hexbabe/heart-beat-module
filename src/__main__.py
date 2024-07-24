import asyncio
import sys

from viam.module.module import Module
from viam.components.generic import Generic
from .module import HeartBeatModule

async def main():
    module = Module.from_args()
    module.add_model_from_registry(Generic.SUBTYPE, HeartBeatModule.MODEL)
    await module.start()

if __name__ == "__main__":
    asyncio.run(main())
