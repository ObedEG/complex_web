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
        self.status = "Waiting..." if status is None else status  # could be: Waiting..., Running, Debugging, Finished
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

        elif racktype == "ic":
            task_list.append(cls(rack=rack, category="Power on validation",
                                 description="PDUs power on (Apply power to rack)").save_task())
            task_list.append(cls(rack=rack, category="Power on validation",
                                 description="All power supplies on").save_task())
            task_list.append(cls(rack=rack, category="Power on validation",
                                 description="Validate that there are no error LED's on any devices").save_task())
            task_list.append(cls(rack=rack, category="Power redundancy check",
                                 description="Check if  the rack devices are wired in power redundant configfuration").save_task())
            task_list.append(cls(rack=rack, category="Power redundancy check",
                                 description="Perform power redundancy test per  p-07918, if apply").save_task())
            task_list.append(cls(rack=rack, category="Network Validation",
                                 description="Connectivity validated to each connected network port").save_task())
            task_list.append(cls(rack=rack, category="Network Validation",
                                 description="Correct Port Speed validated").save_task())
            task_list.append(cls(rack=rack, category="Peripheral Setup",
                                 description="Set up IP and hostname for 1G switches").save_task())
            task_list.append(cls(rack=rack, category="Peripheral Setup",
                                 description="Set up IP and hostname for 10G switches").save_task())
            task_list.append(cls(rack=rack, category="Peripheral Setup",
                                 description="Set Up IP/hostname/ & update firmware/image for HIGHSPEED Switches (IB Mellanox / OPA) if apply").save_task())
            task_list.append(cls(rack=rack, category="Peripheral Setup",
                                 description="Check switches image and update if required").save_task())
            task_list.append(cls(rack=rack, category="Peripheral Setup",
                                 description="Set up IP PDUs & save logs").save_task())
            task_list.append(cls(rack=rack, category="Discovery",
                                 description="Turn on nodes/servers to discover macs (run xcat-genesis image)").save_task())
            task_list.append(cls(rack=rack, category="Discovery",
                                 description="Run netboot image and Verify NODES vs P2P, run in console:  for i in `nodels all`; do rbeacon $i on; sleep 1;done").save_task())
            task_list.append(cls(rack=rack, category="Discovery",
                                 description="Discovery FPC, run: configfpc -V -i ens5 --ip 192.168.0.100 ***ens5 could change").save_task())
            task_list.append(cls(rack=rack, category="Discovery",
                                 description="Verify FPC vs P2P (ping fpc, remove their ethernet cable, connect cable again)").save_task())
            task_list.append(cls(rack=rack, category="Firmware Check",
                                 description="Verify FW Levels of all servers (run in xcat >>> rinv all firm | xcoll), update FW if required according to current Best Recipe").save_task())
            task_list.append(cls(rack=rack, category="Firmware Check",
                                 description="Verify FW Levels of FPC, update FW if required according to current Best Recipe").save_task())
            task_list.append(cls(rack=rack, category="RAID set up",
                                 description="Set up a RAID 1, locate drives: storcli /call show all; then run: storcli /cX add vd type=raid1 drives=XX:X-X *** 'X' is the number related").save_task())
            task_list.append(cls(rack=rack, category="Run Image",
                                 description="Install redhat image into HDD").save_task())
            task_list.append(cls(rack=rack, category="Linpack",
                                 description="Follow linpack procedure for Mellanox/OPA").save_task())
            task_list.append(cls(rack=rack, category="Power Cycle Test",
                                 description="Complete 4 AC power cycle").save_task())
            task_list.append(cls(rack=rack, category="Data Collect",
                                 description="Add RACK,CPOM,MFG info to xcat node's groups <br>(EXAMPLE, run in console: chdef all groups=all,compute,ipmi,RACKA1,CPOM201700063,MFGJ11E8PG) and run the script: /home/MAKEINFO/getinfo.sh").save_task())
            task_list.append(cls(rack=rack, category="Clear for ship",
                                 description="Clear IMM: /home/ALLEASY/clearIMM.sh").save_task())
            task_list.append(cls(rack=rack, category="Clear for ship",
                                 description="Clear FPC: /home/ALLEASY/clearFPC.sh").save_task())
            task_list.append(cls(rack=rack, category="Clear for ship",
                                 description="Clear Image in HDD: /home/ALLEASY/clearOS.sh").save_task())
            task_list.append(cls(rack=rack, category="CMOS settings",
                                 description="Select cmos config from >>> home/ALLEASY/cmos_settings ,<br> then run: pasu all batch *selected_cmos_settings*").save_task())
            task_list.append(cls(rack=rack, category="Customer settings",
                                 description="Apply changes to cover client requirements").save_task())
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

    def delete_task(self):
        Database.remove(TasksConstants.COLLECTIONS, {'_id': self._id})

    @classmethod
    def get_task_by_id(cls, task):
        return cls(**Database.find_one(TasksConstants.COLLECTIONS, {"_id": task}))

    @classmethod
    def get_current_task(cls, rack):
        return cls(**Database.find_one(TasksConstants.COLLECTIONS,
                                       {"rack": rack, "status": {"$in": ['Running', 'Debugging']}}))

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

    @staticmethod
    def get_passed_tasks(rack):
        return Database.count(TasksConstants.COLLECTIONS, {"status": "Finished", "rack": rack})

    @staticmethod
    def get_number_of_tasks(rack):
        return Database.count(TasksConstants.COLLECTIONS, {"rack": rack})

    @staticmethod
    def get_tasks_progress(rack):
        return Utils.percentage(Task.get_passed_tasks(rack),
                                Task.get_number_of_tasks(rack))
