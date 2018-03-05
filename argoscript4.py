#!/usr/bin/env python3
import zipfile
import urllib.request as req
import xml.etree.ElementTree as ET
import glob
import sys
import os


def main(anything):
    # we are specifying constants that will be used to construct path to url
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
        elif type == 'hjres':
            read_xml_hjres(xml_files, type)
        '''
        elif type =='hres':
            read_xml_hres(xml_files, type)
        elif type == 'h':
            read_xml_h(xml_files, type)
        elif type =='sconres':
            read_xml_sconres(xml_files, type)
        elif type == 'sjres':
            read_xml_sjres(xml_files, type)
        elif type =='sres':
            read_xml_sres(xml_files, type)
        elif type == 's':
            read_xml_s(xml_files, type)
        '''


def read_xml_hconres(xml_files, type):
    xml_files = glob.glob('*.xml')
    zip_files = glob.glob('*.zip')
    for x in xml_files:
        with open(x, 'r', encoding='utf8') as hconres_elem:
            hconres_number = []
            hconres_title = []
            hconres_congress = []
            hconres_session = []
            hconres_stage = []
            hconres_type = []
            hconres_origin = []
            hconres_pub_pri = []
            hconres_amend_number = []
            hconres_amend_degree = []
            hconres_amend_type = []
            hconres_amend_stage = []
            for event, elem in ET.iterparse(hconres_elem):
                if elem.tag == 'legis-num' and event == 'end':
                    hconres_number.append(elem.text)
                    print(hconres_number)
                '''
                elif elem.tag == 'resolution' and event == 'end':
                    hconres_origin.append(elem.get('key'.capitalize()))
                    hconres_pub_pri.append(elem.get('public-private'.capitalize()))
                    hconres_stage.append(elem.get('resolution-stage'.capitalize))
                    hconres_type.append(elem.get('resolution-type'.capitalize))
                elif elem.tag == 'official-title' and event == 'end':
                    hconres_title.append(elem.text)
                elif elem.tag == 'congress' and event == 'end':
                    raw_congress = []
                    raw_congress.append(elem.text)
                    for r in raw_congress:
                        if elem.text in ['115th CONGRESS']:
                            hconres_congress.append(elem.text.replace(
                                '115th CONGRESS', '115th'))
                        elif elem.text in ['One Hundred Fifteenth Congress of the United States of America']:
                            hconres_congress.append(elem.text.replace(
                                'One Hundred Fifteenth Congress of the United States of America', '115th'))
                        else:
                            print('You missed a congress!')
                elif elem.tag == 'session' and event == 'end':
                    raw_session = []
                    raw_session.append(elem.text)
                    for r in raw_session:
                        if elem.text in ['2d Session']:
                            hconres_session.append(
                                elem.text.replace('2d Session', '2nd'))
                        elif elem.text in ['At the Second Session']:
                            hconres_session.append(elem.text.replace(
                                'At the Second Session', '2nd'))
                        else:
                            print('You missed a session!')
                elif elem.tag == 'amendment-doc' and event == 'end':
                    hconres_amend_number.append(elem.get('legis-num'))
                    hconres_amend_degree.append(elem.get('amend-degree'.capitalize()))
                    hconres_amend_type.append(elem.get('legis-type'.capitalize()))
                    hconres_amend_stage.append(elem.get('amend-type'))
        with open(x, 'r', encoding='utf8') as hconres_bodytext:
            #  find a way to distinguish amendments
            hconres_text = []
            hconres_amend_text = []
            hconres_read = hconres_bodytext.read()
            root = ET.fromstring(hconres_read)
            hconres_findall = root.findall('./resolution-body//')
            for x in hconres_findall:
                for y in x.finall('./'):
                    hconres_itertext = y.itertext()
                    for z in hconres_itertext:
                        print(z)
        f = open(x, 'r')
        dd = f.read()
        root = ET.fromstring(dd)
        rb = root.findall('./resolution-body//')
        for x in rb:
            for y in x.findall('./'):
                j = y.itertext()
                for ll in j:
                    print(ll)
        '''
            elem.clear()
    remove_files(xml_files)
    remove_files(zip_files)
    #  push_to_db(hconres_number, hconres_title, hconres_congress, hconres_session, hconres_stage, hconres_type, hconres_origin, hconres_pub_pri, hconres_text)


def read_xml_hjres(xml_files, type):
    xml_files = glob.glob('*.xml')
    zip_files = glob.glob('*.zip')
    for x in xml_files:
        with open(x, 'r', encoding='utf8') as hjres_elem:
            hjres_number = []
            hjres_title = []
            hjres_congress = []
            hjres_session = []
            hjres_stage = []
            hjres_type = []
            hjres_origin = []
            hjres_pub_pri = []
            hjres_amend_number = []
            hjres_amend_degree = []
            hjres_amend_type = []
            hjres_amend_stage = []
            for event, elem in ET.iterparse(hjres_elem):
                if elem.tag == 'legis-num' and event == 'end':
                    hjres_number.append(elem.text)
                    print(hjres_number)
            elem.clear()
    remove_files(xml_files)
    remove_files(zip_files)
    #  push_to_db(hconres_number, hconres_title, hconres_congress, hconres_session, hconres_stage, hconres_type, hconres_origin, hconres_pub_pri, hconres_text)


def read_xml_hres(xml_files, type):
    pass


def read_xml_h(xml_files, type):
    pass


def read_xml_sconres(xml_files, type):
    pass


def read_xml_sjres(xml_files, type):
    pass


def read_xml_sres(xml_files, type):
    pass


def read_xml_s(xml_files, type):
    pass


def remove_files(file):
    for x in file:
        os.remove(x)


def push_to_db(placeholder):
    success = bool
    if success:
        return 1
    else:
        return 0


def csv_file(whatever):
    pass  # still need a csv function


if __name__ == '__main__':
    main(sys.argv)
