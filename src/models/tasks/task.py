import uuid

import src.models.tasks.constants as TasksConstants
from src.common.database import Database
from src.common.utils import Utils


class Task(object):
    def __init__(self, db_rackid, category, description,
                 db_failureid=None, start_at=None, start_db_userid=None,
                 finish_at=None, finish_db_userid=None, status=None, _id=None):
        self.db_rackid = db_rackid
        self.category = category
        self.description = description
        self.db_failureid = None if db_failureid is None else db_failureid
        self.start_at = None if start_at is None else start_at
        self.start_db_userid = None if start_db_userid is None else start_db_userid
        self.finish_at = None if finish_at is None else finish_at
        self.finish_db_userid = None if finish_db_userid is None else finish_db_userid
        self.status = "Readiness" if status is None else status
        self._id = uuid.uuid4().hex if _id is None else _id

    def update_to_mongo(self):
        Database.update(TasksConstants.COLLECTION, {"_id": self._id}, self.json())
        return True

    def json(self):
        return {
            "_id": self._id,
            "db_rackid": self.db_rackid,
            "category": self.category,
            "description": self.description,
            "db_failureid": self.db_failureid,
            "start_at": self.start_at,
            "start_db_userid": self.start_db_userid,
            "finish_at": self.finish_at,
            "finish_db_userid": self.finish_db_userid,
            "status": self.status
        }

    @classmethod
    def get_task_by_id(cls, db_taskid):
        return cls(**Database.find_one(TasksConstants.COLLECTIONS, {"_id": db_taskid}))

    def finish(self):
        pass

    def failed(self):
        pass
