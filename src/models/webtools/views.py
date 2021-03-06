from flask import Blueprint, session, render_template, url_for, request, send_file, flash, send_from_directory
from src.common.webtools.mtsn import MTSN
from src.common.webtools.webtools_utils import WebtoolsUtils
from werkzeug.utils import redirect, secure_filename
import shlex
import subprocess
import os

webtool_blueprint = Blueprint('TEWebtools', __name__)

UPLOAD_FOLDER = '/data/webtools/uploads'


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
        return render_template('TEWebtools/get_mtsn_results.jinja2', unit=unit, server='10.34.70.220')
    return render_template('TEWebtools/get_mtsn.jinja2')


@webtool_blueprint.route('/download_mtsn', methods=['GET'])
def download_folder():
    server = request.args.get('server')
    path = request.args.get('path')
    mtsn = request.args.get('mtsn')
    print('Here you have the server: {}, path: {} and mtsn: {}'.format(server, path, mtsn))
    if MTSN.copy_folder(mtsn, path, server) == 0:
        print('I passed the copy_folder function!!')
        try:
            if MTSN.zip_mtsn(path, mtsn) == 0:
                print('I passed the zip_mtsn function!!')
                absfolder = os.path.abspath(path)
                print(absfolder + '.zip')
                return send_file(absfolder + '.zip', attachment_filename=mtsn + '.zip') # Revisar por que pasa "download_folder.zip"
        except Exception as e:
            return str(e)


@webtool_blueprint.route('/nodes_status/upload_file', methods=['GET', 'POST'])
def upload_file():
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
        if file and WebtoolsUtils.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for(".return_file", filename=filename))
    return render_template('TEWebtools/node_status/update_file.jinja2')


@webtool_blueprint.route('/upload_iso', methods=['GET', 'POST'])
def upload_iso():
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
        if file and WebtoolsUtils.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for(".confirm_upload", filename=filename))
    return render_template('TEWebtools/uploader.jinja2')

@webtool_blueprint.route('/upload_sucess', methods=['GET', 'POST'])
def confirm_upload(filename):
    return render_template('TEWebtools/upload_success.jinja2', filename=filename)


@webtool_blueprint.route('/node_status/result/<filename>', methods=['GET', 'POST'])
def return_file(filename):
    WebtoolsUtils.handle_excel(os.path.join(UPLOAD_FOLDER, filename))
    #Utils.run_shell('ssh 10.34.70.220 /dfcxact/workarea/Complex/Microsoft/node_status/run_tst_status')
    # Utils.run_shell('scp 10.34.70.220:/dfcxact/workarea/Complex/Microsoft/node_status/status/summary_status.csv '
    #                '/data/webtools/nodes_status')
    #return send_from_directory('/data/webtools/nodes_status', 'summary_status.csv')
    return render_template('TEWebtools/node_status/get_results.jinja2')

@webtool_blueprint.context_processor
def utility_webtool():
    def get_testerlog(path):
        return print(path)

    def dict_path_date(path, server):
        """
                :param path: available mstn-path
                :param server: would be L2 or Backup
                :return: DATE from l2 --- date -r
        """
        cmd = 'date -r ' + path
        r = 'ssh ' + server + ' ' + cmd
        args = shlex.split(r)
        shell_result = subprocess.run(args=args, universal_newlines=False, stdout=subprocess.PIPE)
        return shell_result.stdout.strip().decode('ascii')  # /dfcxact/old-mtsn/J10039LP, 'Sun Apr  8 10:23:47 CDT 2018'

    return dict(get_testerlog=get_testerlog, dict_path_date=dict_path_date)
