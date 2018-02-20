import zipfile
import urllib.request as req
import xml.etree.ElementTree as ET
import glob
import io
import sys
import csv


FILENAME = ('BILLS-115-2-hconres.zip')


def retrieve_urls(filename):
    try:
        data = req.urlretrieve('https://www.govinfo.gov/bulkdata/BILLS/115/2/hconres/BILLS-115-2-hconres.zip',
                               filename=filename)
    except req.URLError as e:
        raise


def read_xml(xml_files):
    xml_files = glob.glob('*.xml')
    for x in xml_files:
        with open(x, 'r', encoding='utf8') as xml_parse:
            tree = ET.parse(xml_parse)
            legis_num = tree.findall('resolution/form')
            for lenu in legis_num:
                print(lenu.find('legis-num').text)


def main(filename):
    with zipfile.ZipFile(FILENAME, 'r') as raw_zip:
        xml_files = zipfile.ZipFile.extractall(raw_zip)
        read_xml(xml_files)


if __name__ == '__main__':
    main(sys.argv)

retrieve_urls(FILENAME)
