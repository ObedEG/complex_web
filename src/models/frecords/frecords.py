import uuid

import src.models.frecords.constants as FRecordConstants
from src.common.database import Database
from src.common.utils import Utils


class FRecord(object):
    def __init__(self, rack, task, started_at, start_user, description=None, badcomponent_sn=None,
                 badcomponent_device=None, badcomponent_replacement=None, node_number=None, node_sn=None, chassis_number=None,
                 chassis_sn=None, failed_step=None, finished_at=None, finish_user=None, feedback=None, _id=None):
        self.rack = rack
        self.task = task  # Task._id reference
        self.node_number = "" if node_number is None else node_number
        self.node_sn = "" if node_sn is None else node_sn
        self.chassis_number = "" if chassis_number is None else chassis_number
        self.chassis_sn = "" if chassis_sn is None else chassis_sn
        self.failed_step = "" if failed_step is None else failed_step
        self.description = "" if description is None else description # Describe the step (Task, Failure or Fix)
        self.badcomponent_sn = "" if badcomponent_sn is None else badcomponent_sn
        self.badcomponent_device = "" if badcomponent_device is None else badcomponent_device
        self.badcomponent_replacement = "" if badcomponent_replacement is None else badcomponent_replacement
        self.feedback = "" if feedback is None else feedback
        self.started_at = started_at
        self.start_user = start_user
        self.finished_at = "" if finished_at is None else finished_at
        self.finish_user = "" if finish_user is None else finish_user
        self._id = uuid.uuid1().hex if _id is None else _id

    def json(self):
        return {
            "rack": self.rack,
            "task": self.task,
            "node_number": self.node_number,
            "node_sn": self.node_sn,
            "chassis_number": self.chassis_number,
            "chassis_sn": self.chassis_sn,
            "failed_step": self.failed_step,
            "description": self.description,
            "badcomponent_sn": self.badcomponent_sn,
            "badcomponent_device": self.badcomponent_device,
            "badcomponent_replacement": self.badcomponent_replacement,
            "feedback": self.feedback,
            "started_at": self.started_at,
            "start_user": self.start_user,
            "finished_at": self.finished_at,
            "finish_user": self.finish_user,
            "_id": self._id
        }

    def save_to_db(self):
        Database.insert(FRecordConstants.COLLECTIONS, self.json())

    def update_to_mongo(self):
        Database.update(FRecordConstants.COLLECTIONS, {"_id": self._id}, self.json())

    def finish_feedback(self, feedback, user):
        self.feedback = feedback
        self.finish_user = user
        self.finished_at = Utils.get_utc_time()
        self.update_to_mongo()

    @classmethod
    def get_frecord_by_rack(cls, rack):
        return [cls(**elem) for elem in Database.find(FRecordConstants.COLLECTIONS, {"rack": rack})]

    @classmethod
    def get_frecord_by_task(cls, task):
        return [cls(**elem) for elem in Database.find(FRecordConstants.COLLECTIONS, {"task": task})]


    @classmethod
    def get_frecord_by_id(cls, frecord):
        return cls(**Database.find_one(FRecordConstants.COLLECTIONS, {"_id": frecord}))

    @staticmethod
    def get_number_of_frecords_nofeedback(task):
        return Database.count(FRecordConstants.COLLECTIONS, {"task": task, "feedback": ""})

    @staticmethod
    def get_number_of_frecords_by_task(task):
        return Database.count(FRecordConstants.COLLECTIONS, {"task": task})
