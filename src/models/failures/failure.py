import uuid

import src.models.failures.constants as FailuresConstants
from src.common.database import Database


class Failure(object):

    def __init__(self, rack, category, description, task, started_at=None, start_user=None,
                 finished_at=None, finish_user=None, fixes=None, solved=None, _id=None):
        self.rack = rack  # this is the Rack._id
        self.category = category  # According to racktype... and Task...
        self.description = description  # Describe the Failure
        self.task = task  # Task id related to
        self.started_at = "" if started_at is None else started_at
        self.start_user = "" if start_user is None else start_user
        self.finished_at = "" if finished_at is None else finished_at
        self.finish_user = "" if finish_user is None else finish_user
        self.fixes = [] if fixes is None else fixes  # this is the list of 'Fix._id' related
        self.solved = False if solved is None else solved
        self._id = uuid.uuid1().hex if _id is None else _id

    def json(self):
        return {
            "rack": self.rack,
            "category": self.category,
            "description": self.description,
            "task": self.task,
            "started_at": self.started_at,
            "start_user": self.start_user,
            "finished_at": self.finished_at,
            "finish_user": self.finish_user,
            "fixes": self.fixes,
            "solved": self.solved,
            "_id": self._id
        }

    #  This function add a new element [Fix._id] of the fixes (list)
    def add_fix(self, fix):
        self.fixes.append(fix)
        self.update_to_mongo()

    def finish(self):
        self.solved = True
        self.update_to_mongo()

    def save_to_db(self):
        Database.insert(FailuresConstants.COLLECTIONS, self.json())

    def update_to_mongo(self):
        Database.update(FailuresConstants.COLLECTIONS, {"_id": self._id}, self.json())

    @classmethod
    def get_failure_by_id(cls, failure):
        return cls(**Database.find_one(FailuresConstants.COLLECTIONS, {"_id": failure}))