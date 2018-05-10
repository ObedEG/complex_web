import shlex
import subprocess
import openpyxl
ALLOWED_EXTENSIONS = set(['csv', 'xlsx'])


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
        cmd = 'grep {0} /data/CSC/truven/{1}/{1}.csv'.format(serial_number, mo)
        r = Utils.stdout_shell(cmd)
        values = r.replace('\n', '').split(',')
        # values :
        #  ['1S7X19CTO1WWJ1003EMG', '172.20.101.1',
        # 'TRVWHIESQL04A-OOB', '10.235.249.49', '255.255.252.0', '10.235.248.1']
        return dict(zip(keys, values))

    @staticmethod
    def get_mo_truven_list():
        cmd = 'ls /data/CSC/truven/*/*.csv'
        csv_file = Utils.shell(cmd).stdout.split()

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

    @staticmethod
    def handle_excel(filename_path):
        l1 = ["112", "102", "117", "103", "104", "116", "108", "115", "113", "114"]
        book = openpyxl.load_workbook(filename_path)
        for sheet in l1:
            cells = []
            current_sheet = book[sheet]
            for cell in range(2, 38):
                cells.append(current_sheet['A{}'.format(cell)])
            Utils.create_nodes_list_file(cells, sheet + '.lst')
        book.close()

    @staticmethod
    def create_nodes_list_file(node_list, file):
        print(node_list)
        str_list = [str(x.value) for x in node_list if x.value is not None]
        print(str_list)
        nodes_file_lst = open('/data/webtools/nodes_list/{}'.format(file), 'w')
        for line in str_list:
            # Revisar la ultima unidad... que no tenga salto de linea ...
            nodes_file_lst.writelines(line + "\n")
        nodes_file_lst.close()
        return Utils.run_shell('scp /data/webtools/nodes_list/{} '
                            '10.34.70.220:/dfcxact/workarea/Complex/Microsoft/node_status/nodes_list/'.format(file))

