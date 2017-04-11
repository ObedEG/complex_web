import uuid

import src.models.fixes.constants as FixesConstants
from src.common.database import Database


class Fix(object):

    def __init__(self, rack, category, description, started_at=None, start_user=None,
                 finished_at=None, finish_user=None, failure=None, task=None, solution=None, feedback=None, _id=None):
        self.rack = rack
        self.category = category  # According to racktype... and Task...
        self.description = description  # Describe the step (Task, Failure or Fix)
        self.started_at = "" if started_at is None else started_at
        self.start_user = "" if start_user is None else start_user
        self.finished_at = "" if finished_at is None else finished_at
        self.finish_user = "" if finish_user is None else finish_user
        self.failure = "" if failure is None else failure  # if it fails here will be the failure._id
        self.task = "" if task is None else task  # add the Task._id related
        self.solution = False if solution is None else solution
        self.feedback = "" if feedback is None else feedback
        self._id = uuid.uuid1().hex if _id is None else _id