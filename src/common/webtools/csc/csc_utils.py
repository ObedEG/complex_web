import shlex
import subprocess
from src.common.webtools.webtools_utils import WebtoolsUtils
import openpyxl
ALLOWED_EXTENSIONS = set(['csv'])


class CscUtils(object):

    @staticmethod
    def get_so_by_file(filename_path):
        book = openpyxl.load_workbook(filename_path)
        sheet = book.active
        SO = str(sheet['A2'].value)
        book.close()
        return SO

    @staticmethod
    def create_settings_folder(so):
        cmd = 'mkdir -p /data/CSC/truven/settings/{}/'.format(so)
        return WebtoolsUtils.run_shell(cmd)  # '0' if ran correctly

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
