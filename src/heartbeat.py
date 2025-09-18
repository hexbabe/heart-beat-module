from threading import Thread
import time
from typing import Any, ClassVar, Coroutine, List, Mapping, SupportsBytes, SupportsFloat, Optional
from typing_extensions import Self

from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.components.generic import Generic
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily
from viam.utils import ValueTypes

from viam.logging import getLogger

LOGGER = getLogger(__name__)

class HeartBeat(Thread):
    def __init__(self):
        super().__init__()
        LOGGER.info("Initializing separate thread to log stuff every second (this will log surprisingly?)")
        self.should_exec = True
        self.count = 0
    
    def run(self):
        while self.should_exec:
            LOGGER.debug(f"This is a log that should log repeatedly, but does not. Count: {self.count}")
            LOGGER.info(f"This is a log that should log repeatedly, but does not. Count: {self.count}")
            LOGGER.warning(f"This is a log that should log repeatedly, but does not. Count: {self.count}")
            LOGGER.error(f"This is a log that should log repeatedly, but does not. Count: {self.count}")
            self.count += 1
            time.sleep(1)

class HeartBeatModule(Generic):
    """
    Generic component, which represents any type of component that can execute arbitrary commands
    """
    MODEL: ClassVar[Model] = Model(ModelFamily("seanorg", "generic"), "heart-beat")
    heart_beat: ClassVar[HeartBeat]

    # Constructor
    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        LOGGER.info("Initializing module (this will log)")
        module_obj = cls(config.name)
        module_obj.heart_beat = HeartBeat()
        module_obj.heart_beat.start()
        LOGGER.info("Successfully started separate thread heartbeat logger (this will log)")
        return module_obj

    @classmethod
    def validate(cls, config: ComponentConfig):
        LOGGER.info("Validating (this will log)")
        return [], []

    async def do_command(self, command: Mapping[str, ValueTypes], *, timeout: Optional[float] = None, **kwargs) -> Coroutine[Any, Any, Mapping[str, ValueTypes]]:
        LOGGER.info("Pinged do_command (this will log)")
        return {
            "count": self.heart_beat.count
        }

    async def close(self):
        LOGGER.info("Closing component (this will log)")
        self.heart_beat.should_exec = False
        self.heart_beat.join()
