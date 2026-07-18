from uuid import uuid4

from object_recognition_service.data.entities.image import Image
from dependency_injector.wiring import inject, Provide

from object_recognition_service.business.application_service import ObjectRecognitionApplicationService
from object_recognition_service.contracts.image.create_image_request import CreateImageRequest, CreateImageResponse
# from object_recognition_service.host.container import container

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

        original_name = file.filename or "unnamed"

        # 1. Lưu file vật lý qua ImageManager (dùng file_storage bên trong)
        entity = Image(
            id=uuid4(),
            file_name=original_name,
            file_size=file_size,
            mime_type=mime_type,
            file_path="",  # Tạm thời để trống, sẽ cập nhật sau khi lưu file thành công
        )

        # 2. Lưu metadata entity vào DB qua repository
        await self.image_manager.add(entity)
        await self.unit_of_work.commit()

        return CreateImageResponse(
            id=entity.id,
            file_name=entity.file_name,
            file_path=entity.file_path,
            file_size=entity.file_size,
            mime_type=entity.mime_type,
        )
