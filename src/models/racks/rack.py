import uuid
from src.common.database import Database
from src.common.utils import Utils
from src.models.tasks.task import Task
from src.models.users.user import User
import src.models.racks.constants as RacksConstants


class Rack(object):
    def __init__(self, rack_id, lerom, client, sn, mo, so, ship_date, best_recipe=None, vm=None, rack_type=None, fc=None,
                 rdns_start=None, rdns_start_db_userid=None, rdns_finish=None, rdns_finish_db_userid=None,
                 test_start=None, test_start_db_userid=None, test_finish=None, test_finish_db_userid=None,
                 tasks_list=None, status_desc=None, status_porcent=None, _id=None):
        self.rack_id = rack_id
        self.lerom = lerom
        self.client = client
        self.sn = sn
        self.mo = mo
        self.so = so
        self.ship_date = ship_date
        self.best_recipe = '' if best_recipe is None else best_recipe
        self.vm = '' if vm is None else vm
        self.rack_type = '' if rack_type is None else rack_type
        self.fc = Rack.get_fc_by_rack_type(rack_type) if fc is None else fc
        self.rdns_start = Utils.get_timezone() if rdns_start is None else rdns_start
        self.rdns_start_db_userid = '' if rdns_start_db_userid is None else rdns_start_db_userid
        self.rdns_finish = '' if rdns_finish is None else rdns_finish
        self.rdns_finish_db_userid = '' if rdns_finish_db_userid is None else rdns_finish_db_userid
        self.test_start = '' if test_start is None else test_start
        self.test_start_db_userid = '' if test_start_db_userid is None else test_start_db_userid
        self.test_finish = '' if test_finish is None else test_finish
        self.test_finish_db_userid = '' if test_finish_db_userid is None else test_finish_db_userid
        self.tasks_list = [] if tasks_list is None else tasks_list
        self.status_desc = "Readiness" if status_desc is None else status_desc
        self.satus_porcent = 0 if status_porcent is None else status_porcent
        self._id = uuid.uuid4().hex if _id is None else _id

    @staticmethod
    def get_fc_by_rack_type(rack_type):
        return "Pending for {}".format(rack_type)

    def rdns(self, email):
        self.rdns_start_db_userid = User.find_id_by_email(email)
        return True

    def save_to_db(self):
        return Database.insert(RacksConstants.COLLECTIONS, self.json())

    def json(self):
        return {
            "rack_id": self.rack_id,
            "lerom": self.lerom,
            "client": self.client,
            "rack_type": self.rack_type,
            "fc": self.fc,
            "sn": self.sn,
            "mo": self.mo,
            "so": self.so,
            "ship_date": self.ship_date,
            "best_recipe": self.best_recipe,
            "vm": self.vm,
            "tasks_list": self.tasks_list,
            "status_desc": self.status_desc,
            "status_porcent": self.satus_porcent,
            "_id": self._id,
            "rdns_start": self.rdns_start,
            "rdns_start_db_userid": self.rdns_start_db_userid,
            "rdns_finish": self.rdns_finish,
            "rdns_finish_db_userid": self.rdns_finish_db_userid,
            "test_start": self.test_start,
            "test_start_db_userid": self.test_start_db_userid,
            "test_finish": self.test_finish,
            "test_finish_db_userid": self.test_finish_db_userid
        }

    @classmethod
    def get_all(cls):
        """
        This classmethod will get all the current racks
        :return:
        """
        return [cls(**elem)for elem in Database.find(RacksConstants.COLLECTIONS, {})]

    @classmethod
    def get_rack_by_lerom_rackid(cls, lerom, rack_id):
        return cls(**Database.find_one("racks", {"lerom": lerom, "rack_id": rack_id}))

    def create_ryo(self):
        self.task_list.append(Task(db_rackid=self._id, category="Power on validation",
                              description="PDUs power on (Apply power to rack)"))
        self.task_list.append(Task(db_rackid=self._id, category="Power on validation",
                              description="All devices power on (power on servers/devices)"))
        self.task_list.append(Task(db_rackid=self._id, category="Power on validation",
                              description="Validate that there are no error LED's on any devices"))

        self.task_list.append(Task(db_rackid=self._id, category="Power redundancy check",
                                  description="Check if  the rack devices are wired in power redundant configuration"))
        self.task_list.append(Task(db_rackid=self._id, category="Power redundancy check",
                                   description="Perform power redundancy test per  p-07918, if apply"))

        self.task_list.append(Task(db_rackid=self._id, category="Power Cycle",
                                   description="Complete one AC power cycle"))

        return True
