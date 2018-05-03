from flask import Blueprint, request, redirect, render_template, url_for
from src.common.webtools.xcat.unit import Unit
from src.common.webtools.xcat.xcat import Xcat
from src.common.webtools.utils import Utils

csc_blueprint = Blueprint('csc', __name__)

truven_vm_ip = '172.15.0.22'


@csc_blueprint.route('/main')
def main_menu():
    return render_template('csc/main_module.jinja2')


@csc_blueprint.route('/truven')
def truven_menu():
    return render_template('csc/truven_menu.jinja2')


@csc_blueprint.route('/truven/add_unit', methods=['POST', 'GET'])
def truven_addunit():
    if request.method == 'POST':
        if str(request.form['serial']).startswith('1S'):
            unit = Unit(request.form['serial'])
            unit.copy_xml_from_l2()
            unit_dict = Utils.truven_def(serial_number=unit.serial)
            Xcat.create_node(hostname=unit.sn.lower(), ip_os=unit_dict['ip-os'],
                             ip_bmc=unit_dict['ip-bmc'], vm=truven_vm_ip)
            Xcat.set_node_macs(hostname=unit.sn.lower(), macs=unit.format_mac_xcat(),
                               vm=truven_vm_ip)
            return redirect(url_for(".truven_menu"))
        else:
            return "Please SCAN a correct Serial Number"
    return render_template('csc/truven_addunit.jinja2')
