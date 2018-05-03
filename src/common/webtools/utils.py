import shlex
import subprocess


class Utils(object):

    @staticmethod
    def shell(cmd):
        args = shlex.split(cmd)
        print(args)
        r = subprocess.run(args=args, universal_newlines=False, stdout=subprocess.PIPE)
        return r  # returns the commplete subprocess object!

    @staticmethod
    def shell_checkoutput(cmd):
        """
        Alternatively, for trusted input, the shell’s own pipeline support
        may still be used directly:

        output=`dmesg | grep hda`
        becomes:

        output=check_output("dmesg | grep hda", shell=True)
        """
        output = subprocess.check_output(cmd, shell=True)
        return output

    @staticmethod
    def run_shell(cmd):
        args = shlex.split(cmd)
        print(args)
        r = subprocess.run(args=args, universal_newlines=False, stdout=subprocess.PIPE)
        return r.returncode  # 0 means it ran successfully!

    @staticmethod
    def run_true_shell(cmd):
        return subprocess.run(cmd, shell=True, stdout=subprocess.PIPE).returncode

    @staticmethod
    def stdout_shell(cmd):
        args = shlex.split(cmd)
        r = subprocess.run(args=args, universal_newlines=False, stdout=subprocess.PIPE)
        return r.stdout.decode()  # return the stdout of the ran cmd!

    @staticmethod
    def run_shell_stdin(cmd, stdin):
        args = shlex.split(cmd)
        r = subprocess.run(args=args, stdin=stdin, universal_newlines=False, stdout=subprocess.PIPE)
        return r.returncode  # 0 means it ran successfully!

    @staticmethod
    def truven_def(serial_number, mo):
        keys = ['serial', 'ip-os', 'hostname-bmc', 'ip-bmc', 'subnet-bmc', 'gateway-bmc']
        cmd = 'grep {0} /data/CSC/truven/{1}.csv'.format(serial_number, mo)
        r = Utils.stdout_shell(cmd)
        values = r.replace('\n', '').split(',')
        # values :
        #  ['1S7X19CTO1WWJ1003EMG', '172.20.101.1',
        # 'TRVWHIESQL04A-OOB', '10.235.249.49', '255.255.252.0', '10.235.248.1']
        return dict(zip(keys, values))
