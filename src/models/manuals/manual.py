import uuid

from src.common.database import Database
import src.models.manuals.constants as ManualsConstants


class Manual(object):
    def __init__(self, file_name, path, description, _id=None):
        self.file_name = file_name
        self.path = path  # This is the location path including the filename
        self.description = description
        self._id = uuid.uuid4.hex() if _id is None else _id

    def json(self):
        return {
            "file_name": self.file_name,
            "path": self.path,
            "description": self.description,
            "_id": self._id
        }

    def save_to_db(self):
        Database.insert(ManualsConstants.COLLECTIONS, self.json())
        return True

    @classmethod
    def get_manual_by_id(cls, manual_db_id):
        return cls(**Database.find_one(ManualsConstants.COLLECTIONS, {"_id": manual_db_id}))

    @classmethod
    def get_all(cls):
        return [cls(**elem) for elem in Database.find(ManualsConstants.COLLECTIONS, {})]
