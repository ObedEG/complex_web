import uuid

import src.models.tasks.constants as TasksConstants
from src.common.database import Database
from src.common.utils import Utils


class Task(object):

    def __init__(self, rack, category, description, started_at=None, start_user=None,
                 finished_at=None, finish_user=None, failure=None, status=None, _id=None):
        self.rack = rack
        self.category = category  # According to racktype... and Task...
        self.description = description  # Describe the step (Task, Failure or Fix)
        self.started_at = "" if started_at is None else started_at
        self.start_user = "" if start_user is None else start_user
        self.finished_at = "" if finished_at is None else finished_at
        self.finish_user = "" if finish_user is None else finish_user
        self.failure = "" if failure is None else failure  # if it fails here will be the failure._id
        self.status = "Waiting..." if status is None else status  # could be: Running, Debugging, Finished
        self._id = uuid.uuid1().hex if _id is None else _id

    def json(self):
        return {
            "rack": self.rack,
            "description": self.description,
            "started_at": self.started_at,
            "start_user": self.start_user,
            "finished_at": self.finished_at,
            "finish_user": self.finish_user,
            "category": self.category,
            "failure": self.failure,
            "status": self.status,
            "_id": self._id
        }

    @classmethod
    def get_tasks_by_racktype(cls, racktype, rack):
        task_list = []
        if racktype == "ryo":
            task_list.append(cls(rack=rack, category="Power on validation",
                                 description="PDUs power on (Apply power to rack)").save_task())
            task_list.append(cls(rack=rack, category="Power on validation",
                                 description="All devices power on (power on servers/devices)").save_task())
            task_list.append(cls(rack=rack, category="Power on validation",
                                  description="Validate that there are no error LED's on any devices").save_task())
            task_list.append(cls(rack=rack, category="Power redundancy check",
                                  description="Check if  the rack devices are wired in power redundant configuration").save_task())
            task_list.append(cls(rack=rack, category="Power redundancy check",
                                  description="Perform power redundancy test per  p-07918, if apply").save_task())
            task_list.append(cls(rack=rack, category="Power Cycle",
                                  description="Complete one AC power cycle").save_task())
            return task_list

        elif racktype == "ryo_nw":
            task_list.append(cls(rack=rack, category="Power on validation",
                                 description="PDUs power on (Apply power to rack)").save_task())
            task_list.append(cls(rack=rack, category="Power on validation",
                                 description="All devices power on (power on servers/devices)").save_task())
            task_list.append(cls(rack=rack, category="Power on validation",
                                 description="Validate that there are no error LED's on any devices").save_task())
            task_list.append(cls(rack=rack, category="Power redundancy check",
                                 description="Check if  the rack devices are wired in power redundant configuration").save_task())
            task_list.append(cls(rack=rack, category="Power redundancy check",
                                 description="Perform power redundancy test per  p-07918, if apply").save_task())
            task_list.append(cls(rack=rack, category="Network Validation",
                                 description="Connectivity validated to each connected network port").save_task())
            task_list.append(cls(rack=rack, category="Network Validation",
                                 description="Correct Port Speed validated").save_task())
            task_list.append(cls(rack=rack, category="Data Collect",
                                 description="Collect the port speed evidence of each switch. Login into the switch console and get the interfaces status, save the log into a text file").save_task())
            task_list.append(cls(rack=rack, category="Power Cycle",
                                 description="Complete one AC power cycle").save_task())
            return task_list
        else:
            return task_list

    #  [cls(**elem) for elem in Database.find(RacksConstants.COLLECTIONS, {})]
    def save_task(self):
        Database.insert(TasksConstants.COLLECTIONS, self.json())
        return self._id

    def update_to_mongo(self):
        Database.update(TasksConstants.COLLECTIONS, {"_id": self._id}, self.json())

    def save_to_mongo(self):
        Database.insert(TasksConstants.COLLECTIONS, self.json())

    @classmethod
    def get_task_by_id(cls, task):
        return cls(**Database.find_one(TasksConstants.COLLECTIONS, {"_id": task}))

    def start(self, user):
        self.status = "Running"
        self.started_at = Utils.get_utc_time()
        self.start_user = user
        self.update_to_mongo()

    def finish(self, user):
        self.status = "Finished"
        self.finished_at = Utils.get_utc_time()
        self.finish_user = user
        self.update_to_mongo()

    def failed(self, failure):
        self.failure = failure
        self.status = "Debugging"
        self.update_to_mongo()
