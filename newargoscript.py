#!/usr/bin/env python3
import zipfile
import urllib.request as req
import xml.etree.ElementTree as ET
import glob
import sys
import os


FILENAME = ('BILLS-115-2-hconres.zip')


def main(anything):
    retrieve_urls(FILENAME)


def retrieve_urls(filename):
    try:
        data = req.urlretrieve('https://www.govinfo.gov/bulkdata/BILLS/115/2/hconres/BILLS-115-2-hconres.zip',
                               filename=filename)
        open_zip(filename)
    except req.URLError as e:
        raise
    # req.urlcleanup()  # is this where it's supposed to go?


def open_zip(filename):
    with zipfile.ZipFile(FILENAME, 'r') as raw_zip:
        xml_files = zipfile.ZipFile.extractall(raw_zip)
        read_xml(xml_files)


def read_xml(xml_files):
    xml_files = glob.glob('*.xml')
    for x in xml_files:
        # try:
        with open(x, 'r', encoding='utf8') as xml_parse:
            legis_num = []
            for event, elem in ET.iterparse(xml_parse):
                if event == 'end':
                    if elem.tag == 'legis-num':
                        legis_num.append(elem.text)
                        print(legis_num)
                elem.clear()
    remove_files(xml_files)
    push_to_db(legis_num)
    # except ET.ParseError as e:
    # pass


def remove_files(file):
    for x in file:
        os.remove(x)


def push_to_db(legis_num):
    success = bool
    if success:
        return 1
    else:
        return 0


def csv_file(whatever):
    pass  # still need a csv function


if __name__ == '__main__':
    main(sys.argv)

print(push_to_db)
