from flask import Blueprint, session, render_template, url_for, request
from src.common.webtools import mtsn
from werkzeug.utils import redirect

webtool_blueprint = Blueprint('TEWebtools', __name__)


@webtool_blueprint.route('/get_tstlog', methods=['POST', 'GET'])
def get_tstlog():
    if request.method == 'POST':
        unit = mtsn.MTSN(request.form['serial'])
        return "This is a test to connect . . . so go an look up: ls /dfcxact/mtsn/{}".format(unit.mtsn)
    return render_template('TEWebtools/get_testerlog.jinja2')
