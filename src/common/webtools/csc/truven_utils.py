import shlex
import subprocess
from src.common.webtools.webtools_utils import WebtoolsUtils
import csv
ALLOWED_EXTENSIONS = set(['csv'])


class TruvenUtils(object):

    @staticmethod
    def get_so_by_file(filename_path):
        with open(filename_path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                so = row['so']
        return so

    @staticmethod
    def validate_so(so):
        cmd = 'ls -d /data/CSC/truven/settings/{}'.format(so)
        return WebtoolsUtils.run_shell(cmd)  # '0' if ran correctly

    @staticmethod
    def get_all_so():
        cmd = 'ls /data/CSC/truven/settings/'
        return WebtoolsUtils.stdout_shell(cmd).split()  # list of SOs

    @staticmethod
    def create_settings_folder(so):
        cmd = 'mkdir -p /data/CSC/truven/settings/{}/'.format(so)
        return WebtoolsUtils.run_shell(cmd)  # '0' if ran correctly

    @staticmethod
    def create_work_folder(so):
        cmd = 'mkdir -p /data/CSC/truven/units/{}/'.format(so)
        return WebtoolsUtils.run_shell(cmd)

    @staticmethod
    def create_serial_folder(so, serial):
        cmd = 'mkdir -p /data/CSC/truven/units/{}/{}'.format(so, serial)
        return WebtoolsUtils.run_shell(cmd)

    @staticmethod
    def get_all_sn_by_file(filename_path):
        all_sn = list()
        with open(filename_path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                all_sn.append(row['serial'])
            return all_sn

    @staticmethod
    def get_all_sn_by_so(so):
        filename_path = '/data/CSC/truven/settings/{}/unit_settings.csv'.format(so)
        return TruvenUtils.get_all_sn_by_file(filename_path)

    @staticmethod
    def get_dict_units_settings_by_so(so):
        unit_list = list()
        filename_path = '/data/CSC/truven/settings/{}/unit_settings.csv'.format(so)
        with open(filename_path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                unit_list.append(row)
            return unit_list  # This is a list of dict of each unit

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
