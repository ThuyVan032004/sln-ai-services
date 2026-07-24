import os
from uuid import uuid4

from shared.common.constants.env_constants import EnvConstants

from object_recognition_service.business.services.helpers.s3_helper import upload_image_to_s3

from object_recognition_service.data.entities.image import Image
from dependency_injector.wiring import inject, Provide

from object_recognition_service.business.application_service import ObjectRecognitionApplicationService
from object_recognition_service.contracts.image.create_image_request import CreateImageRequest, CreateImageResponse

class ImageService(ObjectRecognitionApplicationService):
    @inject
    def __init__(self, image_manager = Provide["image_manager"], unit_of_work = Provide["unit_of_work"]):
        super().__init__(unit_of_work=unit_of_work)
        self.image_manager = image_manager

    async def create(self, request: CreateImageRequest) -> CreateImageResponse:
        file = request.file
        file_content = await file.read()
        file_size = len(file_content)
        mime_type = file.content_type or "application/octet-stream"
        filename = file.filename or "unnamed"

        # 1. Upload to S3 first
        file_path = await upload_image_to_s3(
            file_content=file_content,
            file_name=filename,
            mime_type=mime_type,
            bucket_name=os.getenv(EnvConstants.AWS_S3_BUCKET),
            region_name=os.getenv(EnvConstants.AWS_REGION),
        )

        # 2. Save metadata with the real file_path
        entity = Image(
            id=uuid4(),
            file_name=filename,
            file_size=file_size,
            mime_type=mime_type,
            file_path=file_path,
        )

        await self.image_manager.add(entity)
        await self.unit_of_work.commit()

        return CreateImageResponse(
            id=entity.id,
            file_name=entity.file_name,
            file_path=entity.file_path,
            file_size=entity.file_size,
            mime_type=entity.mime_type,
        )