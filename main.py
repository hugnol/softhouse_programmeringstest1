import sys, os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from entry import Entry
#    File Converter Program
#   ---------------------------
# | Input: row-based fileformat |
# | Output: XML fileformat      |
#   ---------------------------

def main(argv):
    inputFilePath = argv[0] 
    outputFilePath = argv[1]

    try:
        inputFile = open(inputFilePath, 'r')
    except:
        print('Unable to open file {}'.format(inputFilePath))
        sys.exit(1)

    # Creating the root node of the tree
    root = ET.Element('people')
    while True:
        row = inputFile.readline()
        if not row:
            break
        data = (row.rstrip()).split('|', 1)
        data[1] = data[1].split('|') 
        
        if data[0] == 'P':
            personEntry = Entry(root, 'person')
            try:
                personEntry.set_subelement('firstname', data[1][0])
                personEntry.set_subelement('lastname', data[1][1])
            except:
                pass
        elif data[0] == 'T':
            phoneEntry = Entry(personEntry.get_tree(), 'phone')
            try:
                phoneEntry.set_subelement('mobile', data[1][0])
                phoneEntry.set_subelement('landline', data[1][1])
            except:
                pass
        elif data[0] == 'A':
            addressEntry = Entry(personEntry.get_tree(), 'address')
            try:
                addressEntry.set_subelement('street', data[1][0])
                addressEntry.set_subelement('city', data[1][1])
                addressEntry.set_subelement('postnumber', data[1][2])
            except:
                pass
        elif data[0] == 'F':
            familyEntry = Entry(personEntry.get_tree(), 'family')
            try:
                familyEntry.set_subelement('name', data[1][0])
                familyEntry.set_subelement('born', data[1][1])
            except:
                pass
            
            while True:
                prev = inputFile.tell()
                row = inputFile.readline()
                if not row:
                    break
                data = (row.rstrip()).split('|', 1)
                data[1] = data[1].split('|')
                if data[0] == 'T':
                    phoneEntry = Entry(familyEntry.get_tree(), 'phone')
                    try:
                        phoneEntry.set_subelement('mobile', data[1][0])
                        phoneEntry.set_subelement('landline', data[1][1])
                    except:
                        pass
                elif data[0] == 'A':
                    addressEntry = Entry(familyEntry.get_tree(), 'address')
                    try:
                        addressEntry.set_subelement('street', data[1][0])
                        addressEntry.set_subelement('city', data[1][1])
                        addressEntry.set_subelement('postnumber', data[1][2])
                    except:
                        pass
                else:
                    inputFile.seek(prev)
                    break

    xmlstring = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    with open(outputFilePath, 'w') as outputFile:
        outputFile.write(xmlstring)
    inputFile.close()

if __name__ == "__main__":
    main(sys.argv[1:])