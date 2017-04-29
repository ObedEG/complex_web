import uuid

import src.models.racks.constants as RacksConstants
import src.models.tasks.constants as TasksConstants
import src.models.failures.constants as FailuresConstants
import src.models.fixes.constants as FixesConstants
from src.common.database import Database
from src.common.utils import Utils
from src.models.tasks.task import Task


class Rack(object):
    def __init__(self, rackid, crm, mfg_so, lerom, mtm, customer, racktype, sn, expected_ship_date, ctb_date,
                 estimated_ship_date, comments, status=None, start_user=None, started_at=None, finish_user=None,
                 finished_at=None, _id=None, tasks=None):
        self.rackid = rackid
        self.crm = crm
        self.mfg_so = mfg_so
        self.lerom = lerom
        self.mtm = mtm
        self.customer = customer
        self.racktype = racktype
        self.sn = sn
        self.expected_ship_date = expected_ship_date
        self.ctb_date = ctb_date
        self.estimated_ship_date = estimated_ship_date
        self.comments = comments  # Describe current rack status, which VM to use, etc
        self.status = "Readiness" if status is None else status  # Readiness, Running, Debugging, Passed
        self.start_user = "" if start_user is None else start_user
        self.started_at = "" if started_at is None else started_at
        self.finish_user = "" if finish_user is None else finish_user
        self.finished_at = "" if finished_at is None else finished_at
        self._id = uuid.uuid4().hex if _id is None else _id
        self.tasks = Task.get_tasks_by_racktype(racktype=self.racktype, rack=self._id) if tasks is None else tasks

    def save_to_db(self):
        Database.insert(RacksConstants.COLLECTIONS, self.json())

    def json(self):
        return {
            "_id": self._id,
            "rackid": self.rackid,
            "crm": self.crm,
            "mfg_so": self.mfg_so,
            "lerom": self.lerom,
            "mtm": self.mtm,
            "customer": self.customer,
            "racktype": self.racktype,
            "sn": self.sn,
            "expected_ship_date": self.expected_ship_date,
            "ctb_date": self.ctb_date,
            "estimated_ship_date": self.estimated_ship_date,
            "comments": self.comments,
            "status": self.status,
            "start_user": self.start_user,
            "started_at": self.started_at,
            "finish_user": self.finish_user,
            "finished_at": self.finished_at,
            "tasks": self.tasks
        }

    @classmethod
    def get_all(cls):
        """
        This classmethod will get all the current racks
        :return:
        """
        return [cls(**elem)for elem in Database.find(RacksConstants.COLLECTIONS, {})]

    @classmethod
    def get_racks_under_test(cls):
        # Readinnes, Running, Debugging, Passed
        return [cls(**elem)for elem in Database.find(RacksConstants.COLLECTIONS,
                                                     {"status": {"$in": ['Running', 'Debugging']}})]

    @classmethod
    def get_racks_under_readiness(cls):
        # Readinnes, Running, Debugging, Passed
        return [cls(**elem) for elem in Database.find(RacksConstants.COLLECTIONS, {"status": 'Readiness'})]

    @classmethod
    def get_rack_by_id(cls, _id):
        return cls(**Database.find_one(RacksConstants.COLLECTIONS, {"_id": _id}))

    def update_tasks(self, tasks):
        self.tasks = tasks
        self.update_to_mongo()

    def fix_rack(self):
        self.status = "Running"
        self.update_to_mongo()

    def start_rack(self, user):
        self.status = "Running"
        self.started_at = Utils.get_utc_time()
        self.start_user = user
        self.update_to_mongo()

    def failed_rack(self):
        self.status = "Debugging"
        self.update_to_mongo()

    def finish_rack(self, user):
        self.status = "Passed"
        self.finished_at = Utils.get_utc_time()
        self.finish_user = user
        self.update_to_mongo()

    def update_to_mongo(self):
        Database.update(RacksConstants.COLLECTIONS, {"_id": self._id}, self.json())

    def delete(self):
        Database.remove(RacksConstants.COLLECTIONS, {'_id': self._id})
        Database.remove(TasksConstants.COLLECTIONS, {'rack': self._id})
        Database.remove(FailuresConstants.COLLECTIONS, {'rack': self._id})
        Database.remove(FixesConstants.COLLECTIONS, {'rack': self._id})
