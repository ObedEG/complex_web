from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
import src.models.users.decorators as user_decorators
from src.common.utils import Utils
from src.models.racks.rack import Rack
from src.models.tasks.task import Task
from src.models.users.user import User

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
    #  tasks = TaskController.get_tasks_by_racktype(racktype=rack.racktype, rack=_id)
    #  rack.update_tasks(tasks)
    return render_template('racks/edit_tasks.jinja2', rack=rack, tasks=tasks_list)


@rack_blueprint.route('/monitor')
def monitor():
    racks = Rack.get_all()
    return render_template('racks/monitor.jinja2', racks=racks)


@rack_blueprint.route('/monitor/<string:rack>')
def monitor_rack(rack):
    rack = Rack.get_rack_by_id(rack)
    return render_template('racks/monitor_rack.jinja2', rack=rack)


@rack_blueprint.route('/adding_tasks/<string:_id>', methods=['POST', 'GET'])
@user_decorators.requires_login
def racks_under_test():
    racks = Rack.get_all()
    return render_template('racks/monitor.jinja2', racks=racks)


#  This is the trick for run a python function from the DOM (kind of special wrapper)
@rack_blueprint.context_processor
def utility_mtytime():
        def get_mtytime(date):
            return Utils.get_mtytime(date).strftime("%d-%m-%Y at %H:%M")
        return dict(get_mtytime=get_mtytime)
