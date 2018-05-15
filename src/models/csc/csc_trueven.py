from flask import Blueprint, request, redirect, render_template, url_for, flash, send_file
from src.common.webtools.xcat.unit import Unit
from src.common.webtools.xcat.xcat import Xcat
from src.common.webtools.csc.csc_utils import CscUtils
from src.common.webtools.webtools_utils import WebtoolsUtils
from werkzeug.utils import redirect, secure_filename
import os

csc_truven_blueprint = Blueprint('csc_truven', __name__)

truven_vm_ip = '172.15.0.22'
UPLOAD_FOLDER = '/data/webtools/uploads/csc/truven'
WORK_FOLDER = '/data/CSC/truven/settings'


@csc_truven_blueprint.route('/add_unit', methods=['POST', 'GET'])
def truven_addunit():
    if request.method == 'POST':
        if str(request.form['serial']).startswith('1S'):
            unit = Unit(request.form['serial'])
            # unit_dict = WebtoolsUtils.truven_def(serial_number=unit.serial, mo=unit.MONUMBER)
            # Xcat.create_node(hostname=unit.sn.lower(), ip_os=unit_dict['ip-os'],

            #                 ip_bmc=unit_dict['ip-bmc'], vm=truven_vm_ip)
            Xcat.set_node_macs(hostname=unit.sn.lower(), macs=unit.format_mac_xcat(),
                               vm=truven_vm_ip)
            return redirect(url_for(".truven_menu"))
        else:
            return "Please SCAN a correct Serial Number"
    return render_template('csc/truven_addunit.jinja2')


@csc_truven_blueprint.route('/status', methods=['POST', 'GET'])
def truven_status():
    if request.method == 'POST':
        if str(request.form['serial']).startswith('1S'):
            unit = Unit(request.form['serial'])
            #unit_dict = WebtoolsUtils.truven_def(serial_number=unit.serial, mo=unit.MONUMBER)
            #Xcat.create_node(hostname=unit.sn.lower(), ip_os=unit_dict['ip-os'],
            #                 ip_bmc=unit_dict['ip-bmc'], vm=truven_vm_ip)
            Xcat.set_node_macs(hostname=unit.sn.lower(), macs=unit.format_mac_xcat(),
                               vm=truven_vm_ip)
            return redirect(url_for(".truven_menu"))
        else:
            return "Please SCAN a correct Serial Number"

    return render_template('csc/truven_addunit.jinja2')


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
        if file and CscUtils.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for(".read_uploaded_file", filename=filename))
    return render_template('csc/truven/update_file.jinja2')


@csc_truven_blueprint.route('/read_file/<filename>', methods=['POST', 'GET'])
def read_uploaded_file(filename):
    up_file = os.path.join(UPLOAD_FOLDER, filename)
    so = CscUtils.get_so_by_file(up_file)
    if CscUtils.create_settings_folder(so) == 0:
        cmd = 'cp {} {}/{}/unit_settings.csv'.format(up_file, WORK_FOLDER, so)
        if WebtoolsUtils.run_shell(cmd) == 0:
            if CscUtils.create_work_folder(so) == 0:
                units = CscUtils.get_all_sn_by_file(up_file)
                for serial in units:
                    mtm = serial[2:].split("J", 1)[0]
                    sn = serial[2:].replace(mtm, '')
                    CscUtils.create_serial_folder(so=so, serial=sn)
                return render_template('csc/truven/update_file_done.jinja2',
                                       filename=filename, so=so, num_units=len(units))
