from shared.contracts.requests.update_request import UpdateRequest, UpdateResponse


class DeleteModelRequest(UpdateRequest):
    id: str

class DeleteModelResponse(UpdateResponse):
    pass