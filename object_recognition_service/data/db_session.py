from shared.data import DbSessionBase


class ObjectRecognitionDbSession(DbSessionBase):
    def __init__(self):
        super().__init__()    