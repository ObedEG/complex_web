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
                units = TruvenUtils.get_all_sn_by_so(so)
                for unit in units:
                    tu = TruvenUnit(unit)
                    Xcat.create_node(hostname=tu.sn, ip_os=tu.ip_os,
                                     ip_bmc=tu.ip, vm=csc_truven_vm)
                    Xcat.set_node_macs(hostname=tu.sn, macs=tu.format_mac_xcat(),
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

    """
    --- Test tools ---
    """

    @staticmethod
    def copy_asu_to_unit(vm, sn):
        cmd = 'ssh {0} scp /root/asu64 {1}:/root/'.format(vm, sn)
        return WebtoolsUtils.run_shell(cmd)

    @staticmethod
    def verify_unit_tools(vm, sn):
        asu64 = 'ssh {0} psh {1} ls /root/asu64'.format(vm, sn)
        ipmitool = 'ssh {0} psh {1} ipmitool lan print 1'.format(vm, sn)
        if WebtoolsUtils.run_shell(asu64) == 0:
            return WebtoolsUtils.run_shell(ipmitool)

    @staticmethod
    def change_xcc_hostname(vm, sn, xcc_hostname):
        cmd = 'ssh {0} psh {1} /root/asu64 set IMM.HostName1 {2} --kcs'.format(vm, sn, xcc_hostname)
        return WebtoolsUtils.run_shell(cmd)

    @staticmethod
    def change_xcc_netmask(vm, sn, xcc_netmask):
        cmd = 'ssh {0} psh {1} ipmitool lan set 1 netmask {2}'.format(vm, sn, xcc_netmask)
        return WebtoolsUtils.run_shell(cmd)

    @staticmethod
    def change_xcc_gateway(vm, sn, xcc_gateway):
        cmd = 'ssh {0} psh {1} ipmitool lan set 1 defgw ipaddr {2}'.format(vm, sn, xcc_gateway)
        return WebtoolsUtils.run_shell(cmd)

    @staticmethod
    def run_test(unit):
        if TruvenUtils.copy_asu_to_unit(vm=csc_truven_vm, sn=unit.ip_os) == 0:
            if TruvenUtils.verify_unit_tools(vm=csc_truven_vm, sn=unit.sn) == 0:
                hostname = TruvenUtils.change_xcc_hostname(vm=csc_truven_vm, sn=unit.sn, xcc_hostname=unit.hostname)
                netmask = TruvenUtils.change_xcc_netmask(vm=csc_truven_vm, sn=unit.sn, xcc_netmask=unit.subnet)
                gateway = TruvenUtils.change_xcc_gateway(vm=csc_truven_vm, sn=unit.sn, xcc_gateway=unit.gateway)
                if hostname + netmask + gateway == 0:
                    return "We finished the XCC/IMM configuration ..."

    """
    --- Data Collection tools ---
    """

    @staticmethod
    def create_file_results(so, serial):
        cmd_asu = 'touch /data/CSC/truven/units/{0}/{1}/asu_showall_{1}.log'.format(so, serial)
        cmd_ipmitool = 'touch /data/CSC/truven/units/{0}/{1}/ipmitool_lan_{1}.log'.format(so, serial)
        return WebtoolsUtils.run_shell(cmd_asu) + WebtoolsUtils.run_shell(cmd_ipmitool)

    @staticmethod
    def write_stdoutput_file(output_list, pathfile):
        """
        :param output_list: list of strings generated by r.stdout (subprocess.run(args).stdout.decode()
        :param pathfile: path and filename, example: '/data/webtools/nodes_list/{}'.format(file)
        :return: 0 if ran well
        """
        file = open(pathfile, 'w')
        for line in output_list:
            file.writelines(line + "\n")
        file.close()
        return WebtoolsUtils.run_shell('ls {}'.format(pathfile))

    @staticmethod
    def get_asu_showall_log(vm, sn):
        asu = 'ssh {0} psh {1} /root/asu64 show all --kcs'.format(vm, sn)
        return WebtoolsUtils.stdout_shell(asu).split('\n')  # output_list

    @staticmethod
    def get_ipmitool_lan_log(vm, sn):
        ipmitool = 'ssh {0} psh {1} ipmitool lan print 1'.format(vm, sn)
        return WebtoolsUtils.stdout_shell(ipmitool).split('\n')  # output_list

    @staticmethod
    def get_result_logs(so, serial, vm):
        if TruvenUtils.create_file_results(so, serial) == 0:
            if TruvenUtils.write_stdoutput_file(output_list=TruvenUtils.get_asu_showall_log(vm, serial),
                                                    pathfile='/data/CSC/truven/units/{0}/{1}/asu_showall_{1}.log'
                                                    .format(so, serial)) + \
                   TruvenUtils.write_stdoutput_file(output_list=TruvenUtils.get_ipmitool_lan_log(vm, serial),
                                                    pathfile='/data/CSC/truven/units/{0}/{1}/ipmitool_lan_{1}.log'
                                                    .format(so, serial)) == 0:
                return "and results are save at /data/CSC/truven/units/{0}/{1}/".format(so, serial)
