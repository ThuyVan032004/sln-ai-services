from shared.src.contracts.requests.create_request import CreateRequest, CreateResponse


class CreateImageRequest(CreateRequest):
    file_name: str
    file_path: str
    file_size: int
    mime_type: str
    
class CreateImageResponse(CreateResponse):
    id: str
    file_name: str
    file_path: str
    file_size: int
    mime_type: str