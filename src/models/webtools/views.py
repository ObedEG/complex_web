from flask import Blueprint, session, render_template, url_for, request
from src.common.webtools.mtsn import MTSN
from werkzeug.utils import redirect

webtool_blueprint = Blueprint('TEWebtools', __name__)


@webtool_blueprint.route('/get_tstlog', methods=['POST', 'GET'])
def get_tstlog():
    if request.method == 'POST':
        unit = MTSN(request.form['serial'])
        return render_template('TEWebtools/results.jinja2', path=unit.pathl2)
    return render_template('TEWebtools/get_testerlog.jinja2')


@webtool_blueprint.context_processor
def utility_webtool():
    def get_testerlog(pathtol2):
        return MTSN.get_from_l2(pathtol2)
    return dict(get_testerlog=get_testerlog)
