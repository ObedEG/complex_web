import shlex
import subprocess
from src.common.webtools.webtools_utils import WebtoolsUtils
import csv
ALLOWED_EXTENSIONS = set(['csv'])


class CscUtils(object):

    @staticmethod
    def get_so_by_file(filename_path):
        with open(filename_path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                return row['so']

    @staticmethod
    def create_settings_folder(so):
        cmd = 'mkdir -p /data/CSC/truven/settings/{}/'.format(so)
        return WebtoolsUtils.run_shell(cmd)  # '0' if ran correctly

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
