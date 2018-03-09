import zipfile
import urllib.request as req
import xml.etree.ElementTree as ET
import glob
import sys
import os


def main(anything):
    bills = 'BILLS'
    congress = '115'
    sessions = ['1', '2']
    types = ['hconres', 'hjres']
    for session in sessions:
        step_1 = '/' + bills + '/' + congress + '/' + session
        zip_1 = bills + '-' + congress + '-' + session
        for type in types:
            step_2 = step_1 + '/' + type + '/'
            zip_2 = zip_1 + '-' + type + '.zip'
            retrieve_urls(path_to_file=step_2, filename=zip_2, type=type)


def retrieve_urls(path_to_file, filename, type):
    try:
        data = req.urlretrieve('https://www.govinfo.gov/bulkdata' + path_to_file + filename,
                               filename=filename)
        open_zip(filename, type)
    except req.URLError as e:
        raise


def open_zip(filename, type):
    with zipfile.ZipFile(filename, 'r') as raw_zip:
        xml_files = zipfile.ZipFile.extractall(raw_zip)
        if type == 'hconres':
            read_xml_hconres(xml_files, type)


def read_xml_hconres(xml_files, type):
    xml_files = glob.glob('*.xml')
    zip_files = glob.glob('*.zip')
    for x in xml_files:
        with open(x, 'r', encoding='utf8') as hconres_elem:
            for event, elem in ET.iterparse(hconres_elem):
                if elem.tag == 'legis-num' or elem.tag == 'form' and event == 'end':
                    if elem.tag == 'legis-num':
                        hconres_number = []
                        hconres_number.append(elem.text.title())
                        print(hconres_number)
        with open(x, 'r', encoding='utf8') as hconres_title:
            hconres_read = hconres_title.read()
            root = ET.fromstring(hconres_read)
            hconres_findall = root.findall(
                './form/official-title')
            for f in hconres_findall:
                hconres_itertext = ''.join(f.itertext())
                hconres_title = []
                hconres_title.append(
                    hconres_itertext.rstrip().split('\n\t\t\t'))
                print(hconres_title)
        elem.clear
    remove_files(xml_files)
    remove_files(zip_files)


def read_xml_hjres(xml_files, type):
    pass


def remove_files(file):
    for x in file:
        os.remove(x)


if __name__ == '__main__':
    main(sys.argv)
