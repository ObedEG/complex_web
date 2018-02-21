import subprocess
from src.common.webtools import credentials


class MTSN(object):

    def __init__(self, serial_number):
        self.serial = serial_number.upper()
        self.mt = self.serial[2:6]
        self.model = self.get_model()
        self.mtsn = self.get_mtsn()
        self.pathl2 = "/dfcxact/old-mtsn/" + self.mtsn
        self.pathl2_work = "/dfcxact/work/old_mtsn/" + self.mtsn  # despues de 2-3 dias se mueve aca...
        #  self.pathl3 = self.get_list_path_l3()  # despues de una semana, se mueve al L3_BKUP

    def get_model(self):
        if len(self.serial) > 16:
            return self.serial[6:12]
        return self.serial[6:9]

    def get_mtsn(self):
        if len(self.serial) > 16:
            return self.serial[-8:]  # MTSN - Purley
        return self.serial[2:6] + self.serial[9:13] + "." + self.serial[13:]  # MTSN - Legacy

    def get_list_path_l3(self):
        command = "ls -d /data/old-mtsn/*/" + self.mtsn + " 1>&2"
        remote_shell = "ssh " + credentials.L3_BKUP_IP + command
        mtsn_list = subprocess.run(remote_shell, stderr=subprocess.PIPE, shell=True)
        return mtsn_list.stderr  # lista de paths encontradas en L3. . . !!!!!!!!!!!!!!!!!!!

    @staticmethod
    def get_from_l2(pathl2):
        command = " ls -d " + pathl2 + " 1>&2"
        remote_shell = "ssh " + credentials.L2_IP + command
        response = subprocess.run(remote_shell, stderr=subprocess.PIPE, shell=True)
        return response.stderr
