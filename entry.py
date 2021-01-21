import xml.etree.ElementTree as ET
class Entry:
    def __init__(self, parent, name):
        self.root = ET.SubElement(parent, name)

    def set_subelement(self, name, text):
        subElement = ET.SubElement(self.root, name)
        subElement.text = text
        return subElement

    def get_tree(self):
        return self.root