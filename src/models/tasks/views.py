from flask import Blueprint, session, render_template

import src.models.users.decorators as user_decorators
from src.common.utils import Utils

from src.models.tasks.task import Task

task_blueprint = Blueprint('tasks', __name__)


@task_blueprint.route('/', methods=['POST', 'GET'])
@user_decorators.requires_login
def index():
    return render_template("tasks/index.jinja2")


@task_blueprint.route('/start/<string:task_id>', methods=['POST', 'GET'])
@user_decorators.requires_login
def start_task(task_id):
    task = Task.get_task_by_id(task_id)
    task.start_db_userid = session['email']
    task.start_at = Utils.get_timezone()
    task.update_to_mongo()


