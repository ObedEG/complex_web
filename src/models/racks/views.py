from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
import src.models.users.decorators as user_decorators
from src.common.utils import Utils
from src.models.racks.rack import Rack
from src.models.users.user import User

rack_blueprint = Blueprint('racks', __name__)


@rack_blueprint.route('/rdns_register', methods=['POST', 'GET'])
def rdns_register():
    rack_id = request.form['rack_id']
    lerom = request.form['lerom']
    client = request.form['client']
    sn = request.form['sn']
    mo = request.form['mo']
    so = request.form['so']
    ship_date = request.form['ship_date']
    email = session['email']
    rack = Rack(rack_id, lerom, client, sn, mo, so, ship_date)
    print(rack)
    if rack.rdns(email):
        rack.save_to_db()
        return render_template("racks/define_type.jinja2", rack=rack)


@rack_blueprint.route('/', methods=['POST', 'GET'])
def home_template():
    return render_template('racks/rdns_rack_form.jinja2')


@rack_blueprint.route('/rdns_monitoring')
@user_decorators.requires_login
def rdns_monitor():
    racks = Rack.get_all()
    return render_template('racks/monitor.jinja2', racks=racks)


@rack_blueprint.route('/rdns_rack/<string:lerom>/<string:rack_id>')
@user_decorators.requires_login
def rdns_rack(lerom, rack_id):
    rack = Rack.get_rack_by_lerom_rackid(lerom, rack_id)
    return render_template('racks/rdns_ready.jinja2', rack=rack)


@rack_blueprint.context_processor
def utility_mtytime():
        def get_mtytime(date):
            return Utils.get_mtytime(date).strftime("%d-%m-%Y at %H:%M")
        return dict(get_mtytime=get_mtytime)
