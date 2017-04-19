import uuid

import src.models.fixes.constants as FixesConstants
from src.common.database import Database


class Fix(object):

    def __init__(self, rack, failure, task, category, description, started_at=None, start_user=None,
                 finished_at=None, finish_user=None, solution=None, feedback=None, _id=None):
        self.rack = rack
        self.task = task  # Task._id reference
        self.failure = failure  # failure._id reference
        self.category = category  # According to racktype... and Task...
        self.description = description  # Describe the step (Task, Failure or Fix)
        self.started_at = "" if started_at is None else started_at
        self.start_user = "" if start_user is None else start_user
        self.finished_at = "" if finished_at is None else finished_at
        self.finish_user = "" if finish_user is None else finish_user
        self.solution = False if solution is None else solution
        self.feedback = "" if feedback is None else feedback  # add a feedback when finished_at != ""
        self._id = uuid.uuid1().hex if _id is None else _id

    def json(self):
        return {
            "rack": self.rack,
            "failure": self.failure,
            "task": self.task,
            "category": self.category,
            "description": self.description,
            "started_at": self.started_at,
            "start_user": self.start_user,
            "finished_at": self.finished_at,
            "finish_user": self.finish_user,
            "solution": self.solution,
            "feedback": self.feedback,
            "_id": self._id
        }

    def save_to_db(self):
        Database.insert(FixesConstants.COLLECTIONS, self.json())

    def update_to_mongo(self):
        Database.update(FixesConstants.COLLECTIONS, {"_id": self._id}, self.json())

    def passed(self):
        self.feedback = "PASSED"
        self.solution = True
        self.update_to_mongo()

    def failed(self, feedback):
        self.feedback = feedback
        self.update_to_mongo()

    @classmethod
    def get_fix_by_id(cls, fix):
        return cls(**Database.find_one(FixesConstants.COLLECTIONS, {"_id": fix}))
