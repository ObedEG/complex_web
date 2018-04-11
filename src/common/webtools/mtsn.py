import subprocess
import shlex
#import pandas as pd
from src.common.webtools import credentials as crd


class MTSN(object):
    
    def __init__(self, serial_number):
        self.serial = serial_number.upper()
        self.mtm = self.get_mtm()
        self.sn = self.get_sn()
        self.mtsn = self.get_mtsn()
        self.path_mtsn = self.get_available_mtsn_l2()
        # self.pathl2 = "/dfcxact/old-mtsn/" + self.mtsn
        # self.pathl2_work = "/dfcxact/work/old_mtsn/" + self.mtsn  # despues de 2-3 dias se mueve aca...
        # self.pathl3 = self.get_list_path_l3()  # despues de una semana, se mueve al L3_BKUP

    def get_mtm(self):
        return self.serial[2:].split("J")[0]  # Remove 1S and get the 1st splitted str before 'J' (sn)

    def get_sn(self):
        return self.serial[2:].replace(self.mtm, '')  # Remove 1S and MTM to get the sn

    def get_mtsn(self):
        mtsn_list = []
        if len(self.sn) > 7:
            mtsn_list.append('{}'.format(self.sn))  # MTSN - Purley
        else:
            mtsn_list.append('0{}'.format(self.sn))
        mtsn_list.append('{}{}.{}'.format(self.mtm[:4], self.sn[:4], self.sn[4:]))  # MTSN - Legacy
        return mtsn_list

    def get_available_mtsn_l2(self):
        available_mtsn = []
        for mtsn in self.mtsn:
            checked_path = self.check_exists_mtsn(paths=self.path_l2(mtsn),
                                   server='10.34.70.220')
            if checked_path != []:
                available_mtsn.extend(checked_path)
        return available_mtsn

    def check_exists_mtsn(self, paths, server):
        """
        This method check if a folder mtsn exists and return the list of mtsn available
        :param paths: This is a list of paths "/dfcxact/.../<MSTN>"
        :param server: L2 or BKUP
        :return: list of mtsn available
        """
        mtsn_exists = []
        for path in paths:
            command = 'test -d ' + path + ' && echo True || echo False'
            remote_shell = 'ssh ' + server + ' ' + command
            args = shlex.split(remote_shell)
            shell_result = subprocess.run(args=args, universal_newlines=False, stdout=subprocess.PIPE)
            if shell_result.stdout.strip().decode('ascii') == 'True':
                mtsn_exists.append(path)
        return mtsn_exists

    def path_l2(self, mtsn):
        path_l2 = []
        path_l2.append('/dfcxact/mtsn/{}'.format(mtsn))  # Index 0
        path_l2.append('/dfcxact/old-mtsn/{}'.format(mtsn))  # Index 1
        path_l2.append('/dfcxact/work/old_mtsn/{}'.format(mtsn))  # Index 2
        return path_l2

    @staticmethod
    def dict_folder_date(paths, server):
        """
        This function shows to the web user the DATE, time, path, Server
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
            dict_path_server[path] = shell_result.stdout
            print(dict_path_server)
        print(dict_path_server)
        return dict_path_server  # dict -> { '/dfcxact/old-mtsn/J10039LP': 'Sun Apr  8 10:23:47 CDT 2018' }

    @staticmethod
    def path_bkup(mtsn):
        path_backup = []
        path_backup.append('/data/old-mtsn/*/{}'.format(mtsn))
        return path_backup