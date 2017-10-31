from flask import Blueprint, send_file, render_template, request, url_for, redirect, session
import src.models.users.decorators as user_decorators
from src.common.utils import Utils
from src.models.racks.rack import Rack
from src.models.tasks.task import Task
from src.models.frecords.frecords import FRecord
from src.models.users.user import User

frecord_blueprint = Blueprint('frecords', __name__)


@frecord_blueprint.route('/create_report/<string:rack>/<string:task>', methods=['POST', 'GET'])
@user_decorators.requires_login
def create_report(rack, task):
    if request.method == 'POST':
        rack_to_test = Rack.get_rack_by_id(rack)
        node_number = request.form['node_number']
        node_sn = request.form['node_sn']

        chassis_number = request.form['chassis_number']
        chassis_sn = request.form['chassis_sn']

        failed_step = request.form['failed_step']
        description = request.form['description']

        badcomponent_sn = request.form['badcomponent_sn']
        badcomponent_device = request.form['badcomponent_device']
        badcomponent_replacement = request.form['badcomponent_replacement']

        frecord = FRecord(rack=rack, task=task, start_user=session['email'], started_at=Utils.get_utc_time(),
                          description=description, badcomponent_device=badcomponent_device,
                          badcomponent_sn=badcomponent_sn, badcomponent_replacement=badcomponent_replacement,
                          node_number=node_number, node_sn=node_sn,  chassis_number=chassis_number,
                          chassis_sn=chassis_sn, failed_step=failed_step)
        frecord.save_to_db()
        Task.get_task_by_id(task).failed(True)
        rack_to_test.failed_rack()
        return redirect(url_for('tasks.continue_test', rack=rack))
    return render_template('frecords/create_report.jinja2', rack=rack, task=task)


@frecord_blueprint.route('/feedback/<string:frecord>', methods=['POST', 'GET'])
@user_decorators.requires_login
def feedback(frecord):
    failure_record = FRecord.get_frecord_by_id(frecord)
    if request.method == 'POST':
        feedback_from_form = request.form['feedback']
        failure_record.finish_feedback(feedback=feedback_from_form, user=session['email'])

        if FRecord.get_number_of_frecords_nofeedback(failure_record.task) == 0:
            Task.get_task_by_id(failure_record.task).not_failed_frecord()
            return redirect(url_for('tasks.continue_test', rack=failure_record.rack))
        return redirect(url_for('tasks.continue_test', rack=failure_record.rack))
    return render_template('frecords/feedback_form.jinja2', frecord=failure_record, rack=failure_record.rack)


@frecord_blueprint.route('/edit_report/<string:frecord>', methods=['POST', 'GET'])
@user_decorators.requires_login
def edit(frecord):
    failure_record = FRecord.get_frecord_by_id(frecord)
    if request.method == 'POST':

        failure_record.node_number = request.form['node_number']
        failure_record.node_sn = request.form['node_sn']

        failure_record.chassis_number = request.form['chassis_number']
        failure_record.chassis_sn = request.form['chassis_sn']

        failure_record.failed_step = request.form['failed_step']
        if request.form['description'] != "":
            new_comment = request.form['failed_step']
            failure_record.description += "<br><br>" + Utils.get_monterrey_time() + " " \
                                          + User.find_by_email(session['email']).name + ": <br>" \
                                          + request.form['description']
        failure_record.badcomponent_sn = request.form['badcomponent_sn']
        failure_record.badcomponent_device = request.form['badcomponent_device']
        failure_record.badcomponent_replacement = request.form['badcomponent_replacement']
        failure_record.update_to_mongo()
        return redirect(url_for('tasks.continue_test', rack=failure_record.rack))
    return render_template('frecords/edit_form.jinja2', rack=failure_record.rack, task=failure_record.task,
                           frecord=failure_record)

