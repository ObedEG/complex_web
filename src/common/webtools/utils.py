import shlex
import subprocess


class Utils(object):

    @staticmethod
    def run_shell(cmd):
        args = shlex.split(cmd)
        r = subprocess.run(args=args, universal_newlines=False, stdout=subprocess.PIPE)
        return r.returncode  # 0 means it ran successfully!

