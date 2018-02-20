import zipfile
import urllib.request as req
import xml.etree.ElementTree as ET
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
    xml_string = str(xml_files)  # converts 'NoneType' to string object
    legis_num = ET.parse('BILLS-115hconres98eh.xml')  # where I currently am
    root = legis_num.getroot()
    # purpose = r.xml_document.xpath('//official-title').text
    # print(legis_num.read())


def main(filename):
    with zipfile.ZipFile(FILENAME, 'r') as raw_zip:
        xml_files = zipfile.ZipFile.extractall(raw_zip)
        # print(xml_files)
        read_xml(xml_files)


retrieve_urls(FILENAME)
