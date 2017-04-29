from flask import Blueprint, send_file, render_template, request, url_for, redirect, session
import src.models.users.decorators as user_decorators
from src.common.utils import Utils
from src.models.failures.failure import Failure
from src.models.fixes.fix import Fix
from src.models.racks.rack import Rack
from src.models.tasks.task import Task

failure_blueprint = Blueprint('failures', __name__)


@failure_blueprint.route('/report/<string:rack>/<string:task>', methods=['POST', 'GET'])
@user_decorators.requires_login
def report(rack, task):
    if request.method == 'POST':
        if len(request.form["text"]) < 20:
            return render_template('failures/wrong_failure_description.jinja2', task=task, rack=rack)
        failure = Failure(rack=rack, category=Task.get_task_by_id(task).category,
                          description=request.form["text"], task=task, started_at=Utils.get_utc_time(),
                          start_user=session['email'])
        failure.save_to_db()
        rackobject = Rack.get_rack_by_id(rack)
        rackobject.failed_rack()
        taskobject = Task.get_task_by_id(task)
        taskobject.failed(failure._id)
        return redirect(url_for('fixes.add_new_fix', rack=rack, task=task, failure=failure._id))

    return render_template('failures/report.jinja2', task=task, rack=rack)


@failure_blueprint.route('/report/<string:task>', methods=['POST'])
@user_decorators.requires_login
def cancel(task):
    rack_task = Task.get_task_by_id(task)
    rackid = rack_task.rack
    return redirect(url_for('tasks.start_test', rack=rackid))


#  This is the trick to return the Rack, Failure or Fix object to the DOM (kind of special wrapper)
@failure_blueprint.context_processor
def utility_task():
        def get_failure(failure):
            return Failure.get_failure_by_id(failure)

        def get_fix(fix):
            return Fix.get_fix_by_id(fix)

        def get_rack(rack):
            return Rack.get_rack_by_id(rack)

        return dict(get_failure=get_failure, get_fix=get_fix, get_rack=get_rack)

"""
@failure_blueprint.route('/report/<string:task>')
@user_decorators.requires_login
def add_fix_to_failure_fix_list(task):
    return
"""