from src.common.webtools.utils import Utils
from src.common.webtools.XML2DataFrame import XML2DataFrame


class Unit(object):

    def __init__(self, serial_number):
        self.serial = serial_number.upper()
        self.mtm = self.get_mtm()
        self.sn = self.get_sn()
        self.path_to_xml = self.get_path_xml()  # string '/data/CSC/mediabuild/<serial>.xml'
        self.mackit = self.get_mackit()  # dict of 'MACKIT':'23S-raw-mac'
        self.macs = self.get_macs()  # list of macs ---> 08:94:ef:59:cf:45

    def get_mtm(self):
        return self.serial[2:].split("J")[0]  # Remove 1S, split until J

    def get_sn(self):
        return self.serial[2:].replace(self.mtm, '')

    def get_path_xml(self):
        return '/data/CSC/mediabuild/{}.xml'.format(self.serial)

    def get_mackit(self):
        mac_dict = dict()
        mac_list_xml = XML2DataFrame(self.path_to_xml).parse_root()[0]['kitmacs'].split()
        """
        mac_list_xml
        ['MACKIT3=23S0894EF59D3F7',
        'MACKIT4=23S0894EF59D3F4',
        ...
        'ZATTR_00YD664-USBCAPT-0002-000=MACKIT5',
        'ZATTR_SBB7A01802-SB27A36576-0001-056=MACKIT1;MACKIT2;MACKIT3;MACKIT4']
        """
        for a in mac_list_xml:
            mackit = a.split('=')
            if str(mackit[1])[0:3] == '23S':
                mac_dict[mackit[0]] = mackit[1]
        """
        mac_dict
        {'MACKIT2': '23S0894EF59CF45',
            ...
            'MACKIT1': '23S0894EF59CF44'}
        """
        return mac_dict  # A dict of 'MACKIT':'23S-raw-mac'

    def get_macs(self):
        mac_list = []
        for rawmac in list(self.mackit.values()):
            mac = rawmac[3:].lower()  # remove 23S and do lowercase --> '0894ef59cf45'
            sc_mac = ':'.join(mac[i:i+2] for i in range(0, len(mac), 2))  # '08:94:ef:59:cf:45'
            mac_list.append(sc_mac)
        return mac_list

    def format_mac_xcat(self):
        macs_string = ''
        for i in range(len(self.macs)):
            if i != len(self.macs)-1:
                macs_string += self.mac[i] + '|'
            else:
                macs_string += self.mac[i]
        return macs_string  # String -> 08:94:ef:59:cf:45|3c:18:a0:0b:f6:66

    def copy_xml_from_l2(self):
        cmd = 'scp 10.34.70.220:/dfcxact/mediabuild/UNIT_DATA_MB/{}.xml /data/CSC/mediabuild/'.format(self.serial)
        return Utils.run_shell(cmd)
