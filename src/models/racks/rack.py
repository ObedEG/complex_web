import uuid

import src.models.racks.constants as RacksConstants
from src.common.database import Database
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
        self.status = "Not Under Test" if status is None else status # NotUnderTest, Running, Debugging, Passed
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
    def get_rack_by_id(cls, _id):
        return cls(**Database.find_one(RacksConstants.COLLECTIONS, {"_id": _id}))

    @classmethod
    def get_rack_by_lerom_rackid(cls, lerom, rackid):
        return cls(**Database.find_one(RacksConstants.COLLECTIONS, {"lerom": lerom, "rackid": rackid}))

    def update_tasks(self, tasks):
        self.tasks = tasks
        self.update_to_mongo()

    def update_to_mongo(self):
        Database.update(RacksConstants.COLLECTIONS, {"_id": self._id}, self.json())

    def delete(self):
        Database.remove(RacksConstants.COLLECTIONS, {'_id': self._id})
