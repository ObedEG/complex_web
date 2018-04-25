import xml.etree.ElementTree as ET
# import pandas as pd


class XML2DataFrame:

    def __init__(self, xml_data):
        self.tree = ET.parse(xml_data)  # xml_data -> path/file location
        self.root = self.tree.getroot()

    def parse_root(self):
        return [self.parse_element(child) for child in iter(self.root)]

    def parse_element(self, element, parsed=None):
        if parsed is None:
            parsed = dict()
        for key in element.keys():
            parsed[key] = element.attrib.get(key)
        if element.text:
            parsed[element.tag] = element.text
        for child in list(element):
            self.parse_element(child, parsed)
        return parsed

#    def process_data(self):
#        structure_data = self.parse_root(self.root)
#        return pd.DataFrame(structure_data)

    def get_kitmacs(self):
        return self.parse_root()[0]['kitmacs'].split()

        """
        mac_list_xml
        ['MACKIT3=23S0894EF59D3F7',
        'MACKIT4=23S0894EF59D3F4',
        ...
        'ZATTR_00YD664-USBCAPT-0002-000=MACKIT5',
        'ZATTR_SBB7A01802-SB27A36576-0001-056=MACKIT1;MACKIT2;MACKIT3;MACKIT4']
        """

    def get_orderdata(self):
        """

        :return: a dict of xml - orderdata
        """
        data_list = self.parse_root()[0]['orderdata'].split('\n')
        """
        ['Shipdate 2018-04-11',
            'MONUMBER J1BX84301K00',
                'SONUMBER 4215683950', ... ]

        SOLINEITEM 000010
        Customer_name CONNECTRIASCP4363 PO IS 0323-2271
        Orderable_part 7X19TX2000
        Order_qty 2
        Ship_to_country US
        ZCUPO 23330840
        BSTKD_E
        CUSNO 1213385517

        """
        data_dict = dict()
        for data in [x for x in data_list if x != '']:
            data_dict[data.split(' ', 1)[0]] = data.split(' ', 1)[1]  # data_dict['Shipdate'] = '2018-04-11'
        return data_dict
