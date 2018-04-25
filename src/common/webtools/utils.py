import shlex
import subprocess


class Utils(object):

    @staticmethod
    def run_shell(cmd):
        args = shlex.split(cmd)
        r = subprocess.run(args=args, universal_newlines=False, stdout=subprocess.PIPE)
        return r.returncode  # 0 means it ran successfully!

    @staticmethod
    def stdout_shell(cmd):
        args = shlex.split(cmd)
        r = subprocess.run(args=args, universal_newlines=False, stdout=subprocess.PIPE)
        return r.stdout  # return the stdout of the ran cmd!

    @staticmethod
    def truven_def(serial_number):
        truven = dict()
        keys = list()
        keys.extend('serial', 'ip-os', 'hostname-xcc', 'ip-xcc', 'subnet-xcc', 'gateway-xcc')
        cmd = 'grep {} /data/CSC/truven/serial_ip.csv'.format(serial_number)
        r = Utils.stdout_shell(cmd)
        for key, result in keys, r.split(','):
            truven[key] = result
        return truven
