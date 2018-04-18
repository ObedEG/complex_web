import xml.etree.ElementTree as ET
# import pandas as pd


class XML2DataFrame:

    def __init__(self, xml_data):
        self.tree = ET.parse(xml_data)  #  xml_data is the path-file where is located
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

"""
>>> new_element[0]
<Element 'filename' at 0x7f49a792a638>
>>> new_element[1]
<Element 'bomout' at 0x7f49a792a6d8>
>>> new_element[2]
<Element 'dfcout' at 0x7f49a792a728>

See get_mackit --- in unit.py --- to get macs
>>> new_element[3]
<Element 'kitmacs' at 0x7f49a792a778>

>>> new_element[4]
<Element 'vars' at 0x7f49a792a7c8>
>>> new_element[5]
<Element 'orderdata' at 0x7f49a792a818>
>>> new_element[6]
<Element 'nested' at 0x7f49a792a908>
"""