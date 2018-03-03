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
        with open(x, 'r', encoding='utf8') as xml_parse:
            hconres_dms_id = []
            hconres_number = []
            hconres_title = []
            hconres_congress = []
            hconres_session = []
            hconres_stage = []
            hconres_type = []
            hconres_origin = []
            hconres_pub_pri = []
            hconres_text = []
            amend_number = []
            amend_congress = []
            amend_session = []
            amend_stage = []
            amend_degree = []
            amend_type = []
            amend_origin = []
            amend_text = []
            for event, elem in ET.iterparse(xml_parse):
                # CONCURRENT RESOLUTIONS
                if elem.tag == 'resolution' and event == 'end':
                    hconres_dms_id.append(elem.get('dms-id'))
                    hconres_origin.append(elem.get('key'))
                    hconres_pub_pri.append(elem.get('public-private'))
                    hconres_stage.append(elem.get('resolution-stage'))
                    hconres_type.append(elem.get('resolution-type'))
                elif elem.tag == 'legis-num' and event == 'end':
                    hconres_number.append(elem.text)
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
                elif elem.tag == 'text' or elem.tag == 'quote' or elem.tag == 'enum' or elem.tag == 'division' or elem.tag == 'header' or elem.tag == 'quoted-block' or elem.tag == 'after-quoted-block' or elem.tag == 'paragraph' and event == 'end':
                    if elem.text is not None and elem.text != ' ':
                        temp_list = []
                        temp_list.append(elem.text)
                        # returning last index results in one cacatenated element not distinguished from xml files
                        hconres_text = temp_list
                        print(hconres_text)
                    elif elem.tag == 'division':
                        if elem.text is None:
                            pass  # need a way to replace None with string 'Division' then append to hconres_text
                # AMENDMENT
                elif elem.tag == 'amendment-doc' and event == 'end':
                    amend_number.append(elem.get('legis-num'))
                    amend_degree.append(elem.get('amend-degree'))
                    amend_type.append(elem.get('legis-type'))
                    amend_stage.append(elem.get('amend-type'))
                elif elem.tag == 'legis-num' and event == 'end':
                    amend_number.append(elem.text)
                elif elem.tag == 'congress' and event == 'end':
                    raw_congress = []
                    raw_congress.append(elem.text)
                    for r in raw_congress:
                        if elem.text in ['115th CONGRESS']:
                            amend_congress.append(elem.text.replace(
                                '115th CONGRESS', '115th'))
                        elif elem.text in ['One Hundred Fifteenth Congress of the United States of America']:
                            amend_congress.append(elem.text.replace(
                                'One Hundred Fifteenth Congress of the United States of America', '115th'))
                        else:
                            print('You missed a congress!')
                elif elem.tag == 'session' and event == 'end':
                    raw_session = []
                    raw_session.append(elem.text)
                    for r in raw_session:
                        if elem.text in ['2d Session']:
                            amend_session.append(
                                elem.text.replace('2d Session', '2nd'))
                        elif elem.text in ['At the Second Session']:
                            amend_session.append(elem.text.replace(
                                'At the Second Session', '2nd'))
                        else:
                            print('You missed a session!')
                elif elem.tag == 'dc:publisher' and event == 'end':
                    raw_publisher = []
                    raw_publisher.append(elem.text)
                    for r in raw_publisher:
                        if elem.text in ['U.S. House of Representatives']:
                            amend_origin.append(elem.text.replace(
                                'U.S. House of Representatives', 'House'))
                        else:
                            print('You missed an origin!')
                elif elem.tag == 'amendment-doc':
                    if elem.tag == 'text' and event == 'end':
                        pass
            elem.clear()
    remove_files(xml_files)
    push_to_db(hconres_dms_id, hconres_number, hconres_title, hconres_congress,
               hconres_session, hconres_stage, hconres_type, hconres_origin, hconres_pub_pri, hconres_text, amend_number, amend_congress, amend_session, amend_stage, amend_degree, amend_type, amend_origin, amend_text)


def remove_files(file):
    for x in file:
        os.remove(x)


def push_to_db(dms_id, legis_num, official_title, congress, session, resolution_stage, resolution_type, origin, public_private, hconres_text, amend_number, amend_congress, amend_session, amend_stage, amend_degree, amend_type, amend_origin, amend_text):
    success = bool
    if success:
        return 1
    else:
        return 0


def csv_file(whatever):
    pass  # still need a csv function


if __name__ == '__main__':
    main(sys.argv)
