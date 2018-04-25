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
        return r.stdout.decode()  # return the stdout of the ran cmd!

    @staticmethod
    def truven_def(serial_number):
        truven = dict()
        keys = ['serial', 'ip-os', 'hostname-xcc', 'ip-xcc', 'subnet-xcc', 'gateway-xcc']
        cmd = 'grep {} /data/CSC/truven/serial_ip.csv'.format(serial_number)
        r = Utils.stdout_shell(cmd)
        values = r.replace('\n', '').split(',')
        # values :
        #  ['1S7X19CTO1WWJ1003EMG', '172.20.101.1',
        # 'TRVWHIESQL04A-OOB', '10.235.249.49', '255.255.252.0', '10.235.248.1']
        return dict(zip(keys, values))
