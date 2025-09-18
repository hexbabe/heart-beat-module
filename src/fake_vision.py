from PIL import Image
from typing import Any, ClassVar, Dict, List, Mapping, Optional, Sequence

from typing_extensions import Self
from viam.components.camera import Camera
from viam.logging import getLogger
from viam.media.video import ViamImage, CameraMimeType
from viam.media.utils.pil import pil_to_viam_image
from viam.module.types import Reconfigurable
from viam.proto.app.robot import ServiceConfig
from viam.proto.common import PointCloudObject, ResourceName
from viam.proto.service.vision import Classification, Detection
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily
from viam.services.vision import CaptureAllResult, Vision
from viam.utils import ValueTypes, struct_to_dict

LOGGER = getLogger(__name__)


class FakeVision(Vision, Reconfigurable):
    MODEL: ClassVar[Model] = Model(
        ModelFamily("seanorg", "vision"), "fake-vision"
    )

    def __init__(self, name: str):
        super().__init__(name=name)

    @classmethod
    def new_service(
        cls, config: ServiceConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        """returns new vision service"""
        service = cls(config.name)
        service.reconfigure(config, dependencies)
        return service

    # Validates JSON Configuration
    @classmethod
    def validate_config(cls, config: ServiceConfig) -> Sequence[str]:
        return []

    def reconfigure(
        self, config: ServiceConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        attrs = struct_to_dict(config.attributes)
        camera_name = attrs.get("camera_name")
        
        if not camera_name:
            raise ValueError("Camera name is required but not provided")
        
        camera_resource_name = Camera.get_resource_name(camera_name)
        camera = dependencies.get(camera_resource_name)
        
        if not camera:
            raise ValueError(f"Camera '{camera_name}' not found in dependencies")
        
        self.camera_name = camera_name
        self.camera: Camera = camera

    async def get_properties(
        self,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> Vision.Properties:
        return Vision.Properties(
            classifications_supported=False,
            detections_supported=False,
            object_point_clouds_supported=False,
        )

    async def capture_all_from_camera(
        self,
        camera_name: str,
        return_image: bool = False,
        return_classifications: bool = False,
        return_detections: bool = False,
        return_object_point_clouds: bool = False,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
    ):
        img = await self.camera.get_image(timeout=timeout)
        # dumb
        return CaptureAllResult(
            image=img, classifications=[], detections=[]
        )

    async def get_object_point_clouds(
        self,
        camera_name: str,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> List[PointCloudObject]:
        raise NotImplementedError

    async def get_detections(
        self,
        image: ViamImage,
        *,
        extra: Mapping[str, Any],
        timeout: float,
    ) -> List[Detection]:
        return NotImplementedError

    async def get_classifications(
        self,
        image: ViamImage,
        count: int,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> List[Classification]:
        return NotImplementedError

    async def get_classifications_from_camera(
        self,
        camera_name: str,
        count: int,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> List[Classification]:
        raise NotImplementedError

    async def get_detections_from_camera(
        self, camera_name: str, *, extra: Mapping[str, Any], timeout: float
    ) -> List[Detection]:
        raise NotImplementedError

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs,
    ):
        raise NotImplementedError

    async def close(self):
        """Safely shut down the resource and prevent further use.

        Close must be idempotent. Later configuration may allow a resource to be "open" again.
        If a resource does not want or need a close function, it is assumed that the resource does not need to return errors when future
        non-Close methods are called.

        ::

            await component.close()

        """
        await super().close()
        return