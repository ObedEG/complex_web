import shlex
import subprocess
from src.common.webtools.webtools_utils import WebtoolsUtils
from src.common.webtools.xcat.xcat import Xcat
from src.common.webtools.csc.truven_unit import TruvenUnit
import csv

ALLOWED_EXTENSIONS = set(['csv'])
csc_truven_vm = '172.15.0.22'


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
    def get_dict_units_settings_by_file(filename_path):
        unit_list = list()
        with open(filename_path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                unit_list.append(row)
            return unit_list

    @staticmethod
    def get_dict_units_settings_by_so(so):
        filename_path = '/data/CSC/truven/settings/{}/unit_settings.csv'.format(so)
        return TruvenUtils.get_dict_units_settings_by_file(filename_path)  # This is a list of dict of each unit

    @staticmethod
    def set_workarea(so):
        cmd = 'cp /data/CSC/truven/settings/{}/unit_settings.csv /data/CSC/truven/workarea/'.format(so)
        if Xcat.clean_xcat(vm=csc_truven_vm) == 0:
            Xcat.create_switch(switch='switch1', ip='172.30.50.1', vm=csc_truven_vm)
            if WebtoolsUtils.run_shell(cmd) == 0:
                units = TruvenUtils.get_dict_units_settings_by_so(so)
                for unit in units:
                    tu = TruvenUnit(unit['serial'])
                    Xcat.create_node(hostname=tu.hostname, ip_os=tu.ip_os,
                                     ip_bmc=tu.ip, vm=csc_truven_vm)
                    Xcat.set_node_macs(hostname=tu.hostname, macs=tu.format_mac_xcat(),
                                       vm=csc_truven_vm)
                return Xcat.restart_discovery_services(vm=csc_truven_vm)

    @staticmethod
    def get_workarea_units():
        workarea_file = '/data/CSC/truven/workarea/unit_settings.csv'
        cmd = 'ls {}'.format(workarea_file)
        if WebtoolsUtils.run_shell(cmd) == 0:
            return TruvenUtils.get_dict_units_settings_by_file(workarea_file)

    @staticmethod
    def get_workarea_so():
        workarea_file = '/data/CSC/truven/workarea/unit_settings.csv'
        cmd = 'ls {}'.format(workarea_file)
        if WebtoolsUtils.run_shell(cmd) == 0:
            return TruvenUtils.get_so_by_file(workarea_file)


    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
