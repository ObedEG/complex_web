import shlex
import subprocess
import openpyxl
ALLOWED_EXTENSIONS = set(['csv', 'xlsx'])


class WebtoolsUtils(object):

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
    def stdout_shell(cmd):
        args = shlex.split(cmd)
        print(args)
        r = subprocess.run(args=args, universal_newlines=False, stdout=subprocess.PIPE)
        return r.stdout.decode()  # return the stdout of the ran cmd!

    @staticmethod
    def ping_device(vm, ip):
        cmd = 'ssh {0} ping -c 1 -w 1 {1}'.format(vm, ip)
        stdout = WebtoolsUtils.stdout_shell(cmd).split('\n')
        """['PING 172.15.0.22 (172.15.0.22) 56(84) bytes of data.',
        '64 bytes from 172.15.0.22: icmp_seq=1 ttl=64 time=0.187 ms',
        '',
        '--- 172.15.0.22 ping statistics ---',
        '1 packets transmitted, 1 received, 0% packet loss, time 0ms',
        'rtt min/avg/max/mdev = 0.187/0.187/0.187/0.000 ms', '']"""
        if stdout[1] is not '':
            return "ONLINE"  # Device ONLINE
        else:
            return "OFFLINE"

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @staticmethod
    def handle_excel(filename_path):
        l1 = ["112", "102", "117", "103", "104", "116", "108", "115", "113", "114"]
        book = openpyxl.load_workbook(filename_path)
        for sheet in l1:
            cells = []
            current_sheet = book[sheet]
            for cell in range(2, 38):
                cells.append(current_sheet['A{}'.format(cell)])
            WebtoolsUtils.create_nodes_list_file(cells, sheet + '.lst')
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
        return WebtoolsUtils.run_shell('scp /data/webtools/nodes_list/{} '
                            '10.34.70.220:/dfcxact/workarea/Complex/Microsoft/node_status/nodes_list/'.format(file))

    @staticmethod
    def pass_itac_csc(serial, mo):
        cmd = 'ssh 10.34.70.220 python /dfcxact/dless/itac_client.py -n {0} -s complex -c -w {1}'.format(serial, mo)
        return WebtoolsUtils.run_shell(cmd)

