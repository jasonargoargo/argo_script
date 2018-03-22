import zipfile
import urllib.request as req
import xml.etree.ElementTree as ET
import glob
import sys
import os
import itertools
import csv


number = []
session = []
stage = []
text = []


def main(anything):
    bills = 'BILLS'
    congress = '115'
    sessions = ['1', '2']
    types = ['hconres', 'hjres', 'hres', 'hr', 'sconres', 'sjres', 'sres', 's']
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
        elif type == 'hres':
            read_xml_hres(xml_files, type)
        elif type == 'hr':
            read_xml_hr(xml_files, type)
        elif type == 'sconres':
            read_xml_sconres(xml_files, type)
        elif type == 'sjres':
            read_xml_sjres(xml_files, type)
        elif type == 'sres':
            read_xml_sres(xml_files, type)
        elif type == 's':
            read_xml_s(xml_files, type)


def read_xml_hconres(xml_files, type):
    xml_files = glob.glob('BILLS-115hconres*.xml')
    zip_files = glob.glob('BILLS-115-?-hconres.zip')
    global number
    global session
    global stage
    global text
    for x in xml_files:
        with open(x, 'r', encoding='utf8') as hconres_xml:
            for event, elem in ET.iterparse(hconres_xml):
                if elem.tag == 'resolution' and event == 'end':
                    try:
                        stage.append(elem.get('resolution-stage').title().replace('-', ' '))
                    except AttributeError:
                        print('hconres-stage')
                        continue
                elif elem.tag == 'amendment-doc' and event == 'end':
                    try:
                        stage.append(elem.get('amend-type').title().replace('-', ' '))
                    except AttributeError:
                        print('hconres-stage')
                        continue
                elif elem.tag == 'legis-num' or elem.tag == 'form' and event == 'end':
                    if elem.tag == 'legis-num':
                        try:
                            number.append(elem.text.title())
                        except AttributeError:
                            print('hconres-number')
                            continue
                elif elem.tag == 'legis-num' or elem.tag == 'engrossed-amendment-form' and event == 'end':
                    if elem.tag == 'legis-num':
                        try:
                            number.append(elem.text.title())
                        except AttributeError:
                            print('hconres-number')
                            continue
                elif elem.tag == 'session' or elem.tag == 'form' and event == 'end':
                    if elem.tag == 'session':
                        try:
                            session.append(elem.text.replace(
                                'At the First Session', '1st Session').replace('2d Session', '2nd Session').replace('At the Second Session', '2nd Session'))
                        except AttributeError:
                            print('hconres-session')
                            continue
                elif elem.tag == 'session' or elem.tag == 'engrossed-amendment-form' and event == 'end':
                    if elem.tag == 'session':
                        try:
                            session.append(elem.text.replace(
                                'At the First Session', '1st Session').replace('2d Session', '2nd Session').replace('At the Second Session', '2nd Session'))
                        except AttributeError:
                            print('hconres-session')
                            continue
                    elem.clear
    remove_files(xml_files)
    remove_files(zip_files)


def read_xml_hjres(xml_files, type):
    xml_files = glob.glob('BILLS-115hjres*.xml')
    zip_files = glob.glob('BILLS-115-?-hjres.zip')
    global number
    global session
    global stage
    global text
    for x in xml_files:
        with open(x, 'r', encoding='utf8') as hjres_xml:
            for event, elem in ET.iterparse(hjres_xml):
                if elem.tag == 'resolution' and event == 'end':
                    try:
                        stage.append(elem.get('resolution-stage').title().replace('-', ' '))
                    except AttributeError:
                        print('hjres-stage')
                        continue
                elif elem.tag == 'amendment-doc' and event == 'end':
                    try:
                        stage.append(elem.get('amend-type').title().replace('-', ' '))
                    except AttributeError:
                        print('hjres-stage')
                        continue
                elif elem.tag == 'legis-num' or elem.tag == 'form' and event == 'end':
                    if elem.tag == 'legis-num':
                        try:
                            number.append(elem.text.title())
                        except AttributeError:
                            print('hjres-number')
                            continue
                elif elem.tag == 'legis-num' or elem.tag == 'engrossed-amendment-form' and event == 'end':
                    if elem.tag == 'legis-num':
                        try:
                            number.append(elem.text.title())
                        except AttributeError:
                            print('hjres-number')
                            continue
                elif elem.tag == 'session' or elem.tag == 'form' and event == 'end':
                    if elem.tag == 'session':
                        try:
                            session.append(elem.text.replace(
                                'At the First Session', '1st Session').replace('2d Session', '2nd Session').replace('At the Second Session', '2nd Session'))
                        except AttributeError:
                            print('hjres-session')
                            continue
                elif elem.tag == 'session' or elem.tag == 'engrossed-amendment-form' and event == 'end':
                    if elem.tag == 'session':
                        try:
                            session.append(elem.text.replace(
                                'At the First Session', '1st Session').replace('2d Session', '2nd Session').replace('At the Second Session', '2nd Session'))
                        except AttributeError:
                            print('hjres-session')
                            continue
                    elem.clear
    remove_files(xml_files)
    remove_files(zip_files)


def read_xml_hres(xml_files, type):
    xml_files = glob.glob('BILLS-115hres*.xml')
    zip_files = glob.glob('BILLS-115-?-hres.zip')
    global number
    global session
    global stage
    global text
    for x in xml_files:
        with open(x, 'r', encoding='utf8') as hres_xml:
            for event, elem in ET.iterparse(hres_xml):
                if elem.tag == 'resolution' and event == 'end':
                    try:
                        stage.append(elem.get('resolution-stage').title().replace('-', ' '))
                    except AttributeError:
                        print('hres-stage')
                        continue
                elif elem.tag == 'amendment-doc' and event == 'end':
                    try:
                        stage.append(elem.get('amend-type').title().replace('-', ' '))
                    except AttributeError:
                        print('hres-stage')
                        continue
                elif elem.tag == 'legis-num' or elem.tag == 'form' and event == 'end':
                    if elem.tag == 'legis-num':
                        try:
                            number.append(elem.text.title())
                        except AttributeError:
                            print('hres-number')
                            continue
                elif elem.tag == 'legis-num' or elem.tag == 'engrossed-amendment-form' and event == 'end':
                    if elem.tag == 'legis-num':
                        try:
                            number.append(elem.text.title())
                        except AttributeError:
                            print('hres-number')
                            continue
                elif elem.tag == 'session' or elem.tag == 'form' and event == 'end':
                    if elem.tag == 'session':
                        try:
                            session.append(elem.text.replace(
                                'At the First Session', '1st Session').replace('2d Session', '2nd Session').replace('At the Second Session', '2nd Session'))
                        except AttributeError:
                            print('hres-session')
                            continue
                elif elem.tag == 'session' or elem.tag == 'engrossed-amendment-form' and event == 'end':
                    if elem.tag == 'session':
                        try:
                            session.append(elem.text.replace(
                                'At the First Session', '1st Session').replace('2d Session', '2nd Session').replace('At the Second Session', '2nd Session'))
                        except AttributeError:
                            print('hres-session')
                            continue
                    elem.clear
    remove_files(xml_files)
    remove_files(zip_files)


def read_xml_hr(xml_files, type):
    xml_files = glob.glob('BILLS-115hr*.xml')
    zip_files = glob.glob('BILLS-115-?-hr.zip')
    global number
    global session
    global stage
    global text
    for x in xml_files:
        with open(x, 'r', encoding='utf8') as hr_xml:
            for event, elem in ET.iterparse(hr_xml):
                if elem.tag == 'bill' and event == 'end':
                    try:
                        stage.append(elem.get('bill-stage').title().replace('-', ' '))
                    except AttributeError:
                        print('hr-stage')
                        continue
                elif elem.tag == 'amendment-doc' and event == 'end':
                    try:
                        stage.append(elem.get('amend-type').title().replace('-', ' '))
                    except AttributeError:
                        print('hr-stage')
                        continue
                elif elem.tag == 'legis-num' or elem.tag == 'form' and event == 'end':
                    if elem.tag == 'legis-num':
                        try:
                            number.append(elem.text.title())
                        except AttributeError:
                            print('hr-number')
                            continue
                elif elem.tag == 'legis-num' or elem.tag == 'engrossed-amendment-form' and event == 'end':
                    if elem.tag == 'legis-num':
                        try:
                            number.append(elem.text.title())
                        except AttributeError:
                            print('hr-number')
                            continue
                elif elem.tag == 'session' or elem.tag == 'form' and event == 'end':
                    if elem.tag == 'session':
                        try:
                            session.append(elem.text.replace(
                                'At the First Session', '1st Session').replace('2d Session', '2nd Session').replace('At the Second Session', '2nd Session'))
                        except AttributeError:
                            print('hr-session')
                            continue
                elif elem.tag == 'session' or elem.tag == 'engrossed-amendment-form' and event == 'end':
                    if elem.tag == 'session':
                        try:
                            session.append(elem.text.replace(
                                'At the First Session', '1st Session').replace('2d Session', '2nd Session').replace('At the Second Session', '2nd Session'))
                        except AttributeError:
                            print('hr-session')
                            continue
                    elem.clear
    remove_files(xml_files)
    remove_files(zip_files)


def read_xml_sconres(xml_files, type):
    xml_files = glob.glob('BILLS-115sconres*.xml')
    zip_files = glob.glob('BILLS-115-?-sconres.zip')
    global number
    global session
    global stage
    global text
    for x in xml_files:
        with open(x, 'r', encoding='utf8') as sconres_xml:
            for event, elem in ET.iterparse(sconres_xml):
                if elem.tag == 'resolution' and event == 'end':
                    try:
                        stage.append(elem.get('resolution-stage').title().replace('-', ' '))
                    except AttributeError:
                        print('sconres-stage')
                        continue
                elif elem.tag == 'amendment-doc' and event == 'end':
                    try:
                        stage.append(elem.get('amend-type').title().replace('-', ' '))
                    except AttributeError:
                        print('sconres-stage')
                        continue
                elif elem.tag == 'legis-num' or elem.tag == 'form' and event == 'end':
                    if elem.tag == 'legis-num':
                        try:
                            number.append(elem.text.title())
                        except AttributeError:
                            print('sconres-number')
                            continue
                elif elem.tag == 'legis-num' or elem.tag == 'engrossed-amendment-form' and event == 'end':
                    if elem.tag == 'legis-num':
                        try:
                            number.append(elem.text.title())
                        except AttributeError:
                            print('sconres-number')
                            continue
                elif elem.tag == 'session' or elem.tag == 'form' and event == 'end':
                    if elem.tag == 'session':
                        try:
                            session.append(elem.text.replace(
                                'At the First Session', '1st Session').replace('2d Session', '2nd Session').replace('At the Second Session', '2nd Session'))
                        except AttributeError:
                            print('sconres-session')
                            continue
                elif elem.tag == 'session' or elem.tag == 'engrossed-amendment-form' and event == 'end':
                    if elem.tag == 'session':
                        try:
                            session.append(elem.text.replace(
                                'At the First Session', '1st Session').replace('2d Session', '2nd Session').replace('At the Second Session', '2nd Session'))
                        except AttributeError:
                            print('sconres-session')
                            continue
                    elem.clear
    remove_files(xml_files)
    remove_files(zip_files)


def read_xml_sjres(xml_files, type):
    xml_files = glob.glob('BILLS-115sjres*.xml')
    zip_files = glob.glob('BILLS-115-?-sjres.zip')
    global number
    global session
    global stage
    global text
    for x in xml_files:
        with open(x, 'r', encoding='utf8') as sjres_xml:
            for event, elem in ET.iterparse(sjres_xml):
                if elem.tag == 'resolution' and event == 'end':
                    try:
                        stage.append(elem.get('resolution-stage').title().replace('-', ' '))
                    except AttributeError:
                        print('sjres-stage')
                        continue
                elif elem.tag == 'amendment-doc' and event == 'end':
                    try:
                        stage.append(elem.get('amend-type').title().replace('-', ' '))
                    except AttributeError:
                        print('sjres-stage')
                        continue
                elif elem.tag == 'legis-num' or elem.tag == 'form' and event == 'end':
                    if elem.tag == 'legis-num':
                        try:
                            number.append(elem.text.title())
                        except AttributeError:
                            print('sjres-number')
                            continue
                elif elem.tag == 'legis-num' or elem.tag == 'engrossed-amendment-form' and event == 'end':
                    if elem.tag == 'legis-num':
                        try:
                            number.append(elem.text.title())
                        except AttributeError:
                            print('sjres-number')
                            continue
                elif elem.tag == 'session' or elem.tag == 'form' and event == 'end':
                    if elem.tag == 'session':
                        try:
                            session.append(elem.text.replace(
                                'At the First Session', '1st Session').replace('2d Session', '2nd Session').replace('At the Second Session', '2nd Session'))
                        except AttributeError:
                            print('sjres-session')
                            continue
                elif elem.tag == 'session' or elem.tag == 'engrossed-amendment-form' and event == 'end':
                    if elem.tag == 'session':
                        try:
                            session.append(elem.text.replace(
                                'At the First Session', '1st Session').replace('2d Session', '2nd Session').replace('At the Second Session', '2nd Session'))
                        except AttributeError:
                            print('sjres-session')
                            continue
                    elem.clear
    remove_files(xml_files)
    remove_files(zip_files)


def read_xml_sres(xml_files, type):
    xml_files = glob.glob('BILLS-115sres*.xml')
    zip_files = glob.glob('BILLS-115-?-sres.zip')
    global number
    global session
    global stage
    global text
    for x in xml_files:
        with open(x, 'r', encoding='utf8') as sres_xml:
            for event, elem in ET.iterparse(sres_xml):
                if elem.tag == 'resolution' and event == 'end':
                    try:
                        stage.append(elem.get('resolution-stage').title().replace('-', ' '))
                    except AttributeError:
                        print('sres-stage')
                        continue
                elif elem.tag == 'amendment-doc' and event == 'end':
                    try:
                        stage.append(elem.get('amend-type').title().replace('-', ' '))
                    except AttributeError:
                        print('sres-stage')
                        continue
                elif elem.tag == 'legis-num' or elem.tag == 'form' and event == 'end':
                    if elem.tag == 'legis-num':
                        try:
                            number.append(elem.text.title())
                        except AttributeError:
                            print('sres-number')
                            continue
                elif elem.tag == 'legis-num' or elem.tag == 'engrossed-amendment-form' and event == 'end':
                    if elem.tag == 'legis-num':
                        try:
                            number.append(elem.text.title())
                        except AttributeError:
                            print('sres-number')
                            continue
                elif elem.tag == 'session' or elem.tag == 'form' and event == 'end':
                    if elem.tag == 'session':
                        try:
                            session.append(elem.text.replace(
                                'At the First Session', '1st Session').replace('2d Session', '2nd Session').replace('At the Second Session', '2nd Session'))
                        except AttributeError:
                            print('sres-session')
                            continue
                elif elem.tag == 'session' or elem.tag == 'engrossed-amendment-form' and event == 'end':
                    if elem.tag == 'session':
                        try:
                            session.append(elem.text.replace(
                                'At the First Session', '1st Session').replace('2d Session', '2nd Session').replace('At the Second Session', '2nd Session'))
                        except AttributeError:
                            print('sres-session')
                            continue
                    elem.clear
    remove_files(xml_files)
    remove_files(zip_files)


def read_xml_s(xml_files, type):
    xml_files = glob.glob('BILLS-115s*.xml')
    zip_files = glob.glob('BILLS-115-?-s.zip')
    global number
    global session
    global stage
    global text
    for x in xml_files:
        with open(x, 'r', encoding='utf8') as s_xml:
            for event, elem in ET.iterparse(s_xml):
                if elem.tag == 'bill' and event == 'end':
                    try:
                        stage.append(elem.get('bill-stage').title().replace('-', ' '))
                    except AttributeError:
                        print('s-stage')
                        continue
                elif elem.tag == 'amendment-doc' and event == 'end':
                    try:
                        stage.append(elem.get('amend-type').title().replace('-', ' '))
                    except AttributeError:
                        print('s-stage')
                        continue
                elif elem.tag == 'legis-num' or elem.tag == 'form' and event == 'end':
                    if elem.tag == 'legis-num':
                        try:
                            number.append(elem.text.title())
                        except AttributeError:
                            print('s-number')
                            continue
                elif elem.tag == 'legis-num' or elem.tag == 'engrossed-amendment-form' and event == 'end':
                    if elem.tag == 'legis-num':
                        try:
                            number.append(elem.text.title())
                        except AttributeError:
                            print('s-number')
                            continue
                elif elem.tag == 'session' or elem.tag == 'form' and event == 'end':
                    if elem.tag == 'session':
                        try:
                            session.append(elem.text.replace(
                                'At the First Session', '1st Session').replace('2d Session', '2nd Session').replace('At the Second Session', '2nd Session'))
                        except AttributeError:
                            print('s-session')
                            continue
                elif elem.tag == 'session' or elem.tag == 'engrossed-amendment-form' and event == 'end':
                    if elem.tag == 'session':
                        try:
                            session.append(elem.text.replace(
                                'At the First Session', '1st Session').replace('2d Session', '2nd Session').replace('At the Second Session', '2nd Session'))
                        except AttributeError:
                            print('s-session')
                            continue
                    elem.clear
    remove_files(xml_files)
    remove_files(zip_files)


def remove_files(file):
    for x in file:
        os.remove(x)


def push_to_db(whatever):
    success = bool
    if success:
        return 1
    else:
        return 0


def csv_file(???):
    with open('BILLS.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Number', 'Session', 'Stage'])
        writer.writerows(number, session, stage)


if __name__ == '__main__':
    main(sys.argv)

# for n, value in enumerate(number, 1):
#     print(n, value)
# for n, value in enumerate(session, 1):
#     print(n, value)
# for n, value in enumerate(stage, 1):
#     print(n, value)
# BILLS_dict = dict(zip(number, stage))
# for key, value in sorted(BILLS_dict.items()):
#     print(key, value)
# print(len(number))
# print(len(session))
# print(len(stage))
print(dir(number))
