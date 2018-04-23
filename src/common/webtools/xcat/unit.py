from src.common.webtools.utils import Utils
from src.common.webtools.XML2DataFrame import XML2DataFrame


class Unit(object):

    def __init__(self, serial_number):
        self.serial = serial_number.upper()
        self.mtm = self.get_mtm()
        self.sn = self.get_sn()
        self.path_to_xml = self.get_path_xml()  # string '/data/CSC/mediabuild/<serial>.xml'
        self.macs = self.get_macs()  # list of macs ---> 08:94:ef:59:cf:45
        self.Shipdate = self.get_dict_data['Shipdate']
        self.MONUMBER = self.get_dict_data['MONUMBER']
        self.SONUMBER = self.get_dict_data['SONUMBER']
        self.SOLINEITEM = self.get_dict_data['SOLINEITEM']
        self.Customer_name = self.get_dict_data['Customer_name']
        self.Order_qty = self.get_dict_data['Order_qty']

    def get_mtm(self):
        return self.serial[2:].split("J", 1)[0]  # Remove 1S, split until 1st J

    def get_sn(self):
        return self.serial[2:].replace(self.mtm, '')

    def get_path_xml(self):
        return '/data/CSC/mediabuild/{}.xml'.format(self.serial)

    def get_mackit(self):
        mac_dict = dict()
        mac_list_xml = XML2DataFrame(self.path_to_xml).get_kitmacs()
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
        return mac_dict.values()  # A list of mackit values ...'MACKIT':'23S-raw-mac'

    def get_macs(self):
        mac_list = []
        for rawmac in list(self.get_mackit()):
            mac = rawmac[3:].lower()  # remove 23S and do lowercase --> '0894ef59cf45'
            sc_mac = ':'.join(mac[i:i+2] for i in range(0, len(mac), 2))  # '08:94:ef:59:cf:45'
            mac_list.append(sc_mac)
        return mac_list

    def format_mac_xcat(self):
        return '|'.join(self.macs)  # String -> 08:94:ef:59:cf:45|3c:18:a0:0b:f6:66

    def copy_xml_from_l2(self):
        cmd = 'scp 10.34.70.220:/dfcxact/mediabuild/UNIT_DATA_MB/{}.xml /data/CSC/mediabuild/'.format(self.serial)
        return Utils.run_shell(cmd)

    def get_dict_data(self):
        return XML2DataFrame(self.path_to_xml).get_orderdata()
