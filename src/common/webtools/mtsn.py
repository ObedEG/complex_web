import subprocess
from src.common.webtools import credentials


class MTSN(object):

    def __init__(self, serial_number):
        self.serial = serial_number.upper()
        self.mt = self.serial[2:6]
        self.model = self.get_model()
        self.mtsn = self.get_mtsn()
        self.pathl2 = "/dfcxact/mtsn/" + self.mtsn
        self.pathl3 = ""    # ... si se requiere, Funcion para Mandar buscar el path en el L3_BKUP

    def get_model(self):
        if len(self.serial) > 16:
            return self.serial[6:12]
        return self.serial[6:9]

    def get_mtsn(self):
        if len(self.serial) > 16:
            return self.serial[-8:]  # MTSN - Purley
        return self.serial[2:6] + self.serial[9:13] + "." + self.serial[13:]  # MTSN - Legacy

    @staticmethod
    def get_from_l2(pathl2):
        command = "ssh" + " " + credentials.L2_IP + " ls " + pathl2 + " 1>&2"
        response = subprocess.run(command, stderr=subprocess.PIPE, shell=True)
        return response.stderr
