from flask import Blueprint, session, render_template, url_for, request
from werkzeug.utils import redirect

import src.models.users.decorators as user_decorators
from src.common.utils import Utils
from src.models.failures.failure import Failure
from src.models.fixes.fix import Fix
from src.models.racks.rack import Rack
from src.models.tasks.task import Task

task_blueprint = Blueprint('tasks', __name__)


@task_blueprint.route('/start_test/<string:rack>', methods=['POST', 'GET'])
@user_decorators.requires_login
def start_test(rack):
    rack_to_test = Rack.get_rack_by_id(rack)
    rack_to_test.start_rack(session['email'])
    tasks_idlist = rack_to_test.tasks
    first_task = Task.get_task_by_id(tasks_idlist[0])
    first_task.start(session['email'])
    tasks = []
    for taskid in tasks_idlist:
        tasks.append(Task.get_task_by_id(taskid))
    return render_template('tasks/rack_tasks.jinja2', tasks=tasks)


@task_blueprint.route('/test/<string:rack>', methods=['POST', 'GET'])
@user_decorators.requires_login
def continue_test(rack):
    rack_to_test = Rack.get_rack_by_id(rack)
    tasks_idlist = rack_to_test.tasks
    tasks = []
    for taskid in tasks_idlist:
        tasks.append(Task.get_task_by_id(taskid))
    return render_template('tasks/rack_tasks.jinja2', tasks=tasks)


@task_blueprint.route('/test/passed/<string:task>', methods=['POST', 'GET'])
@user_decorators.requires_login
def passed(task):
    if request.method == 'POST':
        task_to_finish = Task.get_task_by_id(task)
        rack_look_up = Rack.get_rack_by_id(task_to_finish.rack)
        taskid_list = rack_look_up.tasks
        task_to_finish = Task.get_task_by_id(taskid_list[taskid_list.index(task)])
        task_to_finish.finish(session['email'])
        tasks = []
        for elem in taskid_list:
            if elem == task:
                if elem != taskid_list[-1]:
                    next_task = Task.get_task_by_id(taskid_list[taskid_list.index(elem)+1])
                    next_task.start(session['email'])
                else:
                    rack_look_up.finish_rack(session['email'])
            tasks.append(Task.get_task_by_id(elem))
        return redirect(url_for('.continue_test', rack=task_to_finish.rack))
    return render_template('tasks/confirm_pass.jinja2', task=task)

#  This is the trick to return the Rack, Failure or Fix object to the DOM (kind of special wrapper)
@task_blueprint.context_processor
def utility_task():
        def get_failure(failure):
            return Failure.get_failure_by_id(failure)

        def get_fix(fix):
            return Fix.get_fix_by_id(fix)

        def get_rack(rack):
            return Rack.get_rack_by_id(rack)

        def get_task_by_id(task):
            return Task.get_task_by_id(task)

        return dict(get_failure=get_failure, get_fix=get_fix, get_rack=get_rack, get_task_by_id=get_task_by_id)
