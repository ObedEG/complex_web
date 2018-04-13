from flask import Blueprint, session, render_template, url_for, request
from src.common.webtools.mtsn import MTSN
from werkzeug.utils import redirect
import shlex, subprocess

webtool_blueprint = Blueprint('TEWebtools', __name__)


@webtool_blueprint.route('/get_tstlog', methods=['POST', 'GET'])
def get_tstlog():
    if request.method == 'POST':
        unit = MTSN(request.form['serial'])

        return render_template('TEWebtools/results.jinja2', paths=unit.paths_l2_mtsn, server='10.34.70.220')
    return render_template('TEWebtools/get_testerlog.jinja2')


@webtool_blueprint.route('/get_mtsn/', methods=['POST', 'GET'])
def show_folder():
    if request.method == 'POST':
        unit = MTSN(request.form['serial'])
        return render_template('TEWebtools/get_mtsn_results.jinja2', unit=unit.paths_l2_mtsn, server='10.34.70.220')
    return render_template('TEWebtools/get_mtsn.jinja2')


@webtool_blueprint.context_processor
def utility_webtool():
    def get_testerlog(path):
        return print(path)

    def dict_path_date(paths, server):
        """
                :param paths: list of available mstn-paths
                :param server: would be L2 or Backup
                :return: dict_path_date_server - this is a dict which PATH is key and DATE is the value
        """
        dict_path_server = {}
        for path in paths:
            command = 'date -r ' + path
            remote_shell = 'ssh ' + server + ' ' + command
            args = shlex.split(remote_shell)
            shell_result = subprocess.run(args=args, universal_newlines=False, stdout=subprocess.PIPE)
            dict_path_server[path] = shell_result.stdout.strip().decode('ascii')
            print(dict_path_server)
        print(dict_path_server)
        return dict_path_server  # dict -> { '/dfcxact/old-mtsn/J10039LP': 'Sun Apr  8 10:23:47 CDT 2018' }

    return dict(get_testerlog=get_testerlog, dict_path_date=dict_path_date)
