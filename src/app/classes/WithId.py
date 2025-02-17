import hashlib

class WithId:
    def __init__(self, id: str):
        self.id = id

    def get_id(self) -> str:
        return self.id

    @staticmethod
    def create_id(attribute1, attribute2):
        return hashlib.sha1((attribute1 + attribute2).encode()).hexdigest()
