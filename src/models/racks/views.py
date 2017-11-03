from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
import src.models.users.decorators as user_decorators
from src.common.utils import Utils
from src.models.failures.failure import Failure
from src.models.fixes.fix import Fix
from src.models.frecords.frecords import FRecord
from src.models.racks.rack import Rack
from src.models.tasks.task import Task
from src.models.users.user import User
from src.models.frecords.views import frecord_blueprint
from src.models.tasks.views import task_blueprint

rack_blueprint = Blueprint('racks', __name__)


@rack_blueprint.route('/create_rack', methods=['POST', 'GET'])
@user_decorators.requires_login
def create_rack():
    if request.method == 'POST':
        rackid = request.form['rackid']
        crm = request.form['crm']
        mfg_so = request.form['mfg_so']
        lerom = request.form['lerom']
        mtm = request.form['mtm']
        customer = request.form['customer']
        racktype = request.form['racktype']
        sn = request.form['sn']
        expected_ship_date = request.form['expected_ship_date']
        ctb_date = request.form['ctb_date']
        estimated_ship_date = request.form['estimated_ship_date']
        comments = request.form['comments']
        rack = Rack(rackid, crm, mfg_so, lerom, mtm, customer, racktype, sn,
                    expected_ship_date, ctb_date, estimated_ship_date, comments)
        rack.save_to_db()
        return redirect(url_for(".adding_tasks", _id=rack._id))
    return render_template('racks/form.jinja2')


@rack_blueprint.route('/edit_info')
@user_decorators.requires_login
def edit():
    return render_template('racks/editor.jinja2', racks=Rack.get_all())


@rack_blueprint.route('/edit_info/<string:rack_id>', methods=['POST', 'GET'])
@user_decorators.requires_login
def edit_info(rack_id):
    if request.method == 'POST':
        rackid = request.form['rackid']
        crm = request.form['crm']
        mfg_so = request.form['mfg_so']
        lerom = request.form['lerom']
        mtm = request.form['mtm']
        customer = request.form['customer']
        sn = request.form['sn']
        expected_ship_date = request.form['expected_ship_date']
        ctb_date = request.form['ctb_date']
        estimated_ship_date = request.form['estimated_ship_date']
        comments = request.form['comments']
        rack = Rack.get_rack_by_id(rack_id)
        rack.rackid = rackid
        rack.crm = crm
        rack.mfg_so = mfg_so
        rack.lerom = lerom
        rack.mtm = mtm
        rack.customer = customer
        rack.sn = sn
        rack.expected_ship_date = expected_ship_date
        rack.ctb_date = ctb_date
        rack.estimated_ship_date = estimated_ship_date
        rack.comments = comments
        rack.update_to_mongo()
        return redirect(url_for('.edit'))
    return render_template('racks/edit_info.jinja2', rack=Rack.get_rack_by_id(rack_id))


@rack_blueprint.route('/adding_tasks/<string:_id>', methods=['POST', 'GET'])
@user_decorators.requires_login
def adding_tasks(_id):
    rack = Rack.get_rack_by_id(_id)
    tasks_list = []
    for elem in rack.tasks:
        tasks_list.append(Task.get_task_by_id(elem))
    return render_template('racks/edit_tasks.jinja2', rack=rack, tasks=tasks_list)


@rack_blueprint.route('/adding_tasks/<string:_id>/<string:task>', methods=['POST', 'GET'])
@user_decorators.requires_login
def removing_task(_id, task):
    rack = Rack.get_rack_by_id(_id)
    rack.tasks.remove(task)
    rack.update_tasks(rack.tasks)
    Task.get_task_by_id(task).delete_task()
    return redirect(url_for('racks.adding_tasks', _id=_id))


@rack_blueprint.route('/monitor')
def monitor():
    racks = Rack.get_all()
    title = "Rack Orders Monitor"
    message = "Click on 'Details' for more information"
    return render_template('racks/monitor.jinja2', racks=racks, title=title, message=message)


@rack_blueprint.route('/monitor/<string:rack>')
def monitor_rack(rack):
    rack = Rack.get_rack_by_id(rack)
    return render_template('racks/monitor_rack.jinja2', rack=rack)


@rack_blueprint.route('/test')
@user_decorators.requires_login
def racks_under_test():
    racks = Rack.get_racks_under_test()
    title = "Racks Under Test"
    message = "Select a rack to continue testing"

    return render_template('racks/monitor.jinja2', racks=racks, title=title, message=message)


@rack_blueprint.route('/test/start')
@user_decorators.requires_login
def racks_under_readiness():
    racks = Rack.get_racks_under_readiness()
    title = "Racks in Readiness"
    message = "Click on <strong>START</strong> button to begin"
    return render_template('racks/monitor.jinja2', racks=racks, title=title, message=message)


@rack_blueprint.route('/delete/<string:rack>', methods=['POST', 'GET'])
@user_decorators.requires_login
def delete_rack(rack):
    Rack.get_rack_by_id(rack).delete()
    return render_template('racks/delete.jinja2', rack=rack)


@rack_blueprint.route('/monitor/testreport/<string:rack>', methods=['POST', 'GET'])
def show_test_report(rack):
    rack_report = Rack.get_rack_by_id(rack)
    tasks = []
    for elem in rack_report.tasks:
        tasks.append(Task.get_task_by_id(elem))
    return render_template('racks/test_report.jinja2', rack=rack_report, tasks=tasks)


#  This is the trick to return the Rack, Failure or Fix object to the DOM (kind of special wrapper)

@task_blueprint.context_processor
@frecord_blueprint.context_processor
@rack_blueprint.context_processor
def utility_task():
        def get_failure(failure):
            return Failure.get_failure_by_id(failure)

        def get_fix(fix):
            return Fix.get_fix_by_id(fix)

        def get_rack(rack):
            return Rack.get_rack_by_id(rack)

        def get_mty_time(time):
            return time.astimezone(Utils.MONTERREY).strftime(Utils.FMT)

        def get_user(email):
            return User.find_by_email(email)

        def get_progress(rack):  # This function takes the rack._id
            return Task.get_tasks_progress(rack)  # ...and return the tasks progress

        def get_current_task_by_rack(rack):
            return Task.get_current_task(rack)

        def get_frecord_by_rack(rack):
            return FRecord.get_frecord_by_rack(rack)

        def get_frecord_by_task(task):
            return FRecord.get_frecord_by_task(task)

        def get_number_of_frecords_by_task(task):
            return FRecord.get_number_of_frecords_by_task(task)

        return dict(get_failure=get_failure, get_fix=get_fix, get_rack=get_rack,
                    get_mty_time=get_mty_time, get_user=get_user, get_progress=get_progress,
                    get_current_task_by_rack=get_current_task_by_rack, get_frecord_by_rack=get_frecord_by_rack,
                    get_number_of_frecords_by_task=get_number_of_frecords_by_task,
                    get_frecord_by_task=get_frecord_by_task)


"""
This is the trick for run a python function from the DOM (kind of special wrapper)
@rack_blueprint.context_processor
def utility_mtytime():
        def get_mtytime(date):
            return Utils.get_mtytime(date).strftime("%d-%m-%Y at %H:%M")
        return dict(get_mtytime=get_mtytime)
"""


@rack_blueprint.route('/ms_create_rack', methods=['POST', 'GET'])
@user_decorators.requires_login
def ms_create_rack():
    if request.method == 'POST':
        rackid = request.form['rackid']
        crm = ""
        mfg_so = ""
        lerom = ""
        mtm = ""
        customer = "Microsoft"
        racktype = "ms"
        sn = request.form['sn']
        expected_ship_date = ""
        ctb_date = ""
        estimated_ship_date = ""
        comments = request.form['comments']
        rack = Rack(rackid, crm, mfg_so, lerom, mtm, customer, racktype, sn,
                    expected_ship_date, ctb_date, estimated_ship_date, comments, status="Readiness")
        rack.save_to_db()
        return redirect(url_for(".ms_racks_under_test", _id=rack._id))  # Here put only the 1st stage and BSL
    return render_template('racks/ms_form.jinja2')


@rack_blueprint.route('/ms_test')
@user_decorators.requires_login
def ms_racks_under_test():
    racks = Rack.get_ms_racks_under_test()
    title = "Microsoft Racks"
    message = "Select a rack to see the test report"

    return render_template('racks/ms_monitor.jinja2', racks=racks, title=title, message=message)


@rack_blueprint.route('/ms_passed_racks')
@user_decorators.requires_login
def ms_passed_racks():
    racks = Rack.get_ms_racks_passed()
    title = "Microsoft Racks"
    message = "Select a rack to see the test report"

    return render_template('racks/ms_monitor.jinja2', racks=racks, title=title, message=message)

@rack_blueprint.route('/ms_readiness')
@user_decorators.requires_login
def ms_racks_under_readiness():
    racks = Rack.get_ms_racks_under_readinnes()
    title = "Microsoft Racks"
    message = "Select a rack to continue a test report "

    return render_template('racks/ms_monitor_readiness.jinja2', racks=racks, title=title, message=message)


@rack_blueprint.route('/ms_racks_monitor', methods=['POST', 'GET'])
def ms_racks_monitor():
    racks = Rack.get_ms_racks_under_test()
    title = "Microsoft Racks"
    message = "<small>Select a rack to see the test report</small>"
    if request.method == 'POST':
        query = request.form['query']
        if query == "all":
            racks = Rack.get_ms_racks()
            message += "<br><h3>ALL RACKS</h3>"
        elif query == "under_test":
            racks = Rack.get_ms_racks_under_test()
            message += "<br><h3>RACKS UNDER TEST</h3>"
        elif query == "passed":
            racks = Rack.get_ms_racks_passed()
            message += "<br><h3>PASSED RACK</h3>"
        elif query == "under_readiness":
            racks = Rack.get_ms_racks_under_readinnes()
            message += "<br><h3>RACKS UNDER READINESS</h3>"
        return render_template('racks/ms_racks_monitor.jinja2', racks=racks, title=title, message=message)
    #  Es posible un POST para mandar llamar los racks por status . . .
    return render_template('racks/ms_racks_monitor.jinja2', racks=racks, title=title, message=message)


@rack_blueprint.route('/ms_rack_monitor_details/<string:rack>')
def ms_rack_monitor_details(rack):
    rack_to_test = Rack.get_rack_by_id(rack)
    tasks_idlist = rack_to_test.tasks
    tasks = []
    for taskid in tasks_idlist:
        tasks.append(Task.get_task_by_id(taskid))
    return render_template('tasks/ms_rack_details.jinja2', tasks=tasks)
