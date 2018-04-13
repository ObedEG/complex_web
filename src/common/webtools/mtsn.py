import subprocess
import shlex
import os
import zipfile
#import pandas as pd
from src.common.webtools import credentials as crd


class MTSN(object):

    def __init__(self, serial_number):
        self.serial = serial_number.upper()
        self.mtm = self.get_mtm()
        self.sn = self.get_sn()
        self.mtsn = self.get_mtsn()
        self.paths_l2_mtsn = self.get_available_mtsn_l2()
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
        """
        Quick fix to get a uniq mtsn... not a list of 2 mtsn
        """
        for mtsn in mtsn_list:
            cmd = 'ssh 10.34.70.220 ls /dfcxact/mtsn/{}'.format(mtsn)
            args = shlex.split(cmd)
            r = subprocess.run(args=args, universal_newlines=False, stdout=subprocess.PIPE)
            if r.returncode != 0:
                mtsn_list.remove(mtsn)
        return mtsn_list[0]

    def get_available_mtsn_l2(self):
        available_mtsn = []
        checked_path = self.check_exists_mtsn(paths=self.path_l2(self.mtsn), server='10.34.70.220')
        for path in checked_path:
            if path != []:
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

    def path_bkup(self, mtsn):
        path = '/data/old-mtsn/*/{}'.format(mtsn)
        comm = 'ssh 10.34.70.223 ls -d ' + path
        args = shlex.split(comm)
        r = subprocess.run(args=args, universal_newlines=False, stderr=subprocess.PIPE)
        if r.stderr is not None:
            print('There is a mtsn in server-backup and it is: {}'.format())
            return r.stdout.decode('ascii').split()  # List of the found mtsn-paths
        else:
            return None  # There is no mtsn in backup-server
        # Example :
        #   ['/data/old-mtsn/16-12-50/5465J103.G64',
        #   '/data/old-mtsn/16-12-51/5465J103.G64',
        #   '/data/old-mtsn/16-12-52/5465J103.G64']

    @staticmethod
    def copy_folder(mtsn, path, server):
        here = path.replace(mtsn, '')
        cmd = 'scp -r ' + server + ':' + path + ' ' + here
        args = shlex.split(cmd)
        r = subprocess.run(args=args, universal_newlines=False, stdout=subprocess.PIPE)
        return r.returncode  # 0 means it ran successfully!

    @staticmethod
    def zip_mtsn(path, mtsn):
        """
        :param path: /dfcxact/old-mtsn/J1003EMG/
        :param mtsn: J1003EMG
        :return: 0 if the .zip was created . . .
        """
        cwdpath = os.getcwd()  # save original path (*where you run this py file)
        zip_name = mtsn + '.zip'
        zf = zipfile.ZipFile(zip_name, "w")
        path_mtsn = path.replace(mtsn, '')
        absfolder = os.path.abspath(path_mtsn)  # make sure folder is absolute
        os.chdir(absfolder)
        for dirs, subdirs, files in os.walk('./' + mtsn):
            zf.write(dirs)
            for filename in files:
                zf.write(os.path.join(dirs, filename))
        zf.close()
        os.chdir(cwdpath)
        """
        This is a very simple solution...
        Pending provide a clean up for mtsn and its .zip files
        """
        cmd = 'ls ' + path_mtsn + mtsn + '.zip'
        args = shlex.split(cmd)
        r = subprocess.run(args=args, universal_newlines=False, stdout=subprocess.PIPE)
        return r.returncode  # 0 means it ran successfully!
