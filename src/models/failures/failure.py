import uuid

import src.models.failures.constants as FailuresConstants
from src.common.database import Database


class Failure(object):

    def __init__(self, rack, category, description, started_at=None, start_user=None,
                 finished_at=None, finish_user=None, task=None, fixes=None, solved=None, _id=None):
        self.rack = rack  # this is the Rack._id
        self.category = category  # According to racktype... and Task...
        self.description = description  # Describe the step (Task, Failure or Fix)
        self.started_at = "" if started_at is None else started_at
        self.start_user = "" if start_user is None else start_user
        self.finished_at = "" if finished_at is None else finished_at
        self.finish_user = "" if finish_user is None else finish_user
        self.task = "" if task is None else task  # add the Task._id related
        self.fixes = [] if fixes is None else fixes  # this is the list of 'Fix._id' related
        self.solved = False if solved is None else solved
        self._id = uuid.uuid1().hex if _id is None else _id
