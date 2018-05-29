from flask import Blueprint, request, redirect, render_template, url_for, flash, send_file
from src.common.webtools.xcat.unit import Unit
from src.common.webtools.xcat.xcat import Xcat
from src.common.webtools.csc.truven_utils import TruvenUtils
from src.common.webtools.csc.truven_unit import TruvenUnit
from src.common.webtools.webtools_utils import WebtoolsUtils
from werkzeug.utils import redirect, secure_filename
import os

csc_truven_blueprint = Blueprint('csc_truven', __name__)

truven_vm_ip = '172.15.0.22'
UPLOAD_FOLDER = '/data/webtools/uploads/csc/truven'
WORK_FOLDER = '/data/CSC/truven/settings'


@csc_truven_blueprint.route('/status', methods=['POST', 'GET'])
def truven_status():
    all_so = TruvenUtils.get_all_so()
    if request.method == 'POST':
        so = request.form['so']
        if so in all_so:
            return redirect(url_for(".status_by_so", so=so))
        else:
            return "Please provide a defined SO..."
    return render_template('csc/truven/main_status.jinja2', all_so=all_so)


@csc_truven_blueprint.route('/input_so_file/', methods=['POST', 'GET'])
def upload_units_by_so():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and TruvenUtils.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for(".read_uploaded_file", filename=filename))
    return render_template('csc/truven/update_file.jinja2')


@csc_truven_blueprint.route('/read_file/<filename>', methods=['POST', 'GET'])
def read_uploaded_file(filename):
    up_file = os.path.join(UPLOAD_FOLDER, filename)
    so = TruvenUtils.get_so_by_file(up_file)
    if TruvenUtils.validate_so(so) != 0:
        if TruvenUtils.create_settings_folder(so) == 0:
            cmd = 'cp {} {}/{}/unit_settings.csv'.format(up_file, WORK_FOLDER, so)
            if WebtoolsUtils.run_shell(cmd) == 0:
                if TruvenUtils.create_work_folder(so) == 0:
                    units = TruvenUtils.get_all_sn_by_file(up_file)
                    for serial in units:
                        mtm = serial[2:].split("J", 1)[0]
                        sn = serial[2:].replace(mtm, '')
                        TruvenUtils.create_serial_folder(so=so, serial=sn)
                        TruvenUtils.create_file_results(so=so, serial=sn)
                    return render_template('csc/truven/update_file_done.jinja2',
                                           filename=filename, so=so, num_units=len(units))
    else:
        return "This SO was created before!! {}".format(so)


@csc_truven_blueprint.route('/status/<string:so>')
def status_by_so(so):
    units = TruvenUtils.get_dict_units_settings_by_so(so)
    return render_template('csc/truven/units_status.jinja2', units=units, so=so)


@csc_truven_blueprint.route('/vm/setup/', methods=['POST', 'GET'])
def setup_vm():
    if request.method == 'POST':
        return True
    return render_template('csc/truven/units_status.jinja2')


@csc_truven_blueprint.route('/vm/workarea/', methods=['POST', 'GET'])
def workarea():
    if request.method == 'POST':
        so = request.form['so']
        if so in TruvenUtils.get_all_so():
            TruvenUtils.set_workarea(so)
        else:
            return "The SO: {} was not defined, please add a csv definition " \
                   "to http://10.34.70.230:81/csc_truven/input_so_file/".format(so)
    return render_template('csc/truven/workarea.jinja2')


@csc_truven_blueprint.route('/vm/workarea/<string:serial>', methods=['POST', 'GET'])
def test_unit(serial):
    unit = TruvenUnit(serial)
    return render_template('csc/truven/test_unit.jinja2', serial=serial, unit=unit)


@csc_truven_blueprint.route('/vm/workarea/<string:serial>/run_test', methods=['POST', 'GET'])
def run_test(serial):
    unit = TruvenUnit(serial)
    if TruvenUtils.run_test(unit) + TruvenUtils.get_result_logs(unit.SONUMBER, unit.sn, truven_vm_ip) == 0:
        return redirect(url_for(".workarea"))
    else:
        return "Something did not run correctly . . . verify log: /var/www/html/complex-web/log/uwsgi.log"


@csc_truven_blueprint.context_processor
def truven_utility():

    def get_number_of_units_by_so(so):
        return len(TruvenUtils.get_all_sn_by_so(so))

    def ping_device(ip):
        return WebtoolsUtils.ping_device(vm=truven_vm_ip, ip=ip)

    def get_workarea_units_dict():
        return TruvenUtils.get_workarea_units()

    def get_workarea_so():
        return TruvenUtils.get_workarea_so()

    def check_progress(so, serial):
        return TruvenUtils.check_progress(so, serial)

    return dict(get_number_of_units_by_so=get_number_of_units_by_so, ping_device=ping_device,
                get_workarea_units_dict=get_workarea_units_dict, get_workarea_so=get_workarea_so,
                check_progress=check_progress)
