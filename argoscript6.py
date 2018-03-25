#!/jasonargo/anaconda3/bin/python
import urllib.request as req
import zipfile
import xml.etree.ElementTree as ET
import sys
import os
import glob
import itertools
import datetime
import time
import csv


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
            retrieve_urls(path_to_file=step_2, zipfiles=zip_2)


def retrieve_urls(path_to_file, zipfiles):
    try:
        data = req.urlretrieve('https://www.govinfo.gov/bulkdata' + path_to_file + zipfiles,
                               filename=zipfiles)
        split_zips(zipfiles)
    except req.URLError as e:
        raise


def split_zips(zipfiles):
    hconres_zips = []
    hjres_zips = []
    hres_zips = []
    hr_zips = []
    sconres_zips = []
    sjres_zips = []
    sres_zips = []
    s_zips = []
    if zipfiles in 'BILLS-115-1-hconres.zip':
        hconres_zips.append('BILLS-115-1-hconres.zip')
        parse_hconres(hconres_zips)
    elif zipfiles in 'BILLS-115-2-hconres.zip':
        hconres_zips.append('BILLS-115-2-hconres.zip')
        parse_hconres(hconres_zips)
    elif zipfiles in 'BILLS-115-1-hjres.zip':
        hjres_zips.append('BILLS-115-1-hjres.zip')
        parse_hjres(hjres_zips)
    elif zipfiles in 'BILLS-115-2-hjres.zip':
        hjres_zips.append('BILLS-115-2-hjres.zip')
        parse_hjres(hjres_zips)
    elif zipfiles in 'BILLS-115-1-hres.zip':
        hres_zips.append('BILLS-115-1-hres.zip')
        parse_hres(hres_zips)
    elif zipfiles in 'BILLS-115-2-hres.zip':
        hres_zips.append('BILLS-115-2-hres.zip')
        parse_hres(hres_zips)
    elif zipfiles in 'BILLS-115-1-hr.zip':
        hr_zips.append('BILLS-115-1-hr.zip')
        parse_hr(hr_zips)
    elif zipfiles in 'BILLS-115-2-hr.zip':
        hr_zips.append('BILLS-115-2-hr.zip')
        parse_hr(hr_zips)
    elif zipfiles in 'BILLS-115-1-sconres.zip':
        sconres_zips.append('BILLS-115-1-sconres.zip')
        parse_sconres(sconres_zips)
    elif zipfiles in 'BILLS-115-2-sconres.zip':
        sconres_zips.append('BILLS-115-2-sconres.zip')
        parse_sconres(sconres_zips)
    elif zipfiles in 'BILLS-115-1-sjres.zip':
        sjres_zips.append('BILLS-115-1-sjres.zip')
        parse_sjres(sjres_zips)
    elif zipfiles in 'BILLS-115-2-sjres.zip':
        sjres_zips.append('BILLS-115-2-sjres.zip')
        parse_sjres(sjres_zips)
    elif zipfiles in 'BILLS-115-1-sres.zip':
        sres_zips.append('BILLS-115-1-sres.zip')
        parse_sres(sres_zips)
    elif zipfiles in 'BILLS-115-2-sres.zip':
        sres_zips.append('BILLS-115-2-sres.zip')
        parse_sres(sres_zips)
    elif zipfiles in 'BILLS-115-1-s.zip':
        s_zips.append('BILLS-115-1-s.zip')
        parse_s(s_zips)
    elif zipfiles in 'BILLS-115-2-s.zip':
        s_zips.append('BILLS-115-2-s.zip')
        parse_s(s_zips)
    else:
        print('%s: %s' % ('Unused zips', zipfiles))
    zipfiles = []


def parse_hconres(hconres_zips):
    number = []
    session = []
    stage = []
    text = []
    for h in hconres_zips:
        with zipfile.ZipFile(h, 'r') as raw_zip:
            raw_zip.extractall()
            hconres_xmls = glob.glob('BILLS-115hconres*.xml')
            for x in hconres_xmls:
                with open(x, 'r', encoding='utf8') as hconres_file:
                    for event, elem in ET.iterparse(hconres_file):
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
                                    session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
                                except AttributeError:
                                    print('hconres-session')
                                    continue
                        elif elem.tag == 'session' or elem.tag == 'engrossed-amendment-form' and event == 'end':
                            if elem.tag == 'session':
                                try:
                                    session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
                                except AttributeError:
                                    print('hconres-session')
                                    continue
                            elem.clear
            remove_files(hconres_xmls)
    remove_files(hconres_zips)
    csv_file(number, session, stage)


def parse_hjres(hjres_zips):
    number = []
    session = []
    stage = []
    text = []
    for h in hjres_zips:
        with zipfile.ZipFile(h, 'r') as raw_zip:
            raw_zip.extractall()
            hjres_xmls = glob.glob('BILLS-115hjres*.xml')
            for x in hjres_xmls:
                with open(x, 'r', encoding='utf8') as hjres_file:
                    for event, elem in ET.iterparse(hjres_file):
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
                                    session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
                                except AttributeError:
                                    print('hjres-session')
                                    continue
                        elif elem.tag == 'session' or elem.tag == 'engrossed-amendment-form' and event == 'end':
                            if elem.tag == 'session':
                                try:
                                    session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
                                except AttributeError:
                                    print('hjres-session')
                                    continue
                            elem.clear
            remove_files(hjres_xmls)
    remove_files(hjres_zips)
    csv_file(number, session, stage)


def parse_hres(hres_zips):
    number = []
    session = []
    stage = []
    text = []
    for h in hres_zips:
        with zipfile.ZipFile(h, 'r') as raw_zip:
            raw_zip.extractall()
            hres_xmls = glob.glob('BILLS-115hres*.xml')
            for x in hres_xmls:
                with open(x, 'r', encoding='utf8') as hres_file:
                    for event, elem in ET.iterparse(hres_file):
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
                                    session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
                                except AttributeError:
                                    print('hres-session')
                                    continue
                        elif elem.tag == 'session' or elem.tag == 'engrossed-amendment-form' and event == 'end':
                            if elem.tag == 'session':
                                try:
                                    session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
                                except AttributeError:
                                    print('hres-session')
                                    continue
                            elem.clear
            remove_files(hres_xmls)
    remove_files(hres_zips)
    csv_file(number, session, stage)


def parse_hr(hr_zips):
    number = []
    session = []
    stage = []
    text = []
    for h in hr_zips:
        with zipfile.ZipFile(h, 'r') as raw_zip:
            raw_zip.extractall()
            hr_xmls = glob.glob('BILLS-115hr*.xml')
            for x in hr_xmls:
                with open(x, 'r', encoding='utf8') as hr_file:
                    for event, elem in ET.iterparse(hr_file):
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
                                    session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
                                except AttributeError:
                                    print('hr-session')
                                    continue
                        elif elem.tag == 'session' or elem.tag == 'engrossed-amendment-form' and event == 'end':
                            if elem.tag == 'session':
                                try:
                                    session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
                                except AttributeError:
                                    print('hr-session')
                                    continue
                            elem.clear
            remove_files(hr_xmls)
    remove_files(hr_zips)
    csv_file(number, session, stage)


def parse_sconres(sconres_zips):
    number = []
    session = []
    stage = []
    text = []
    for s in sconres_zips:
        with zipfile.ZipFile(s, 'r') as raw_zip:
            raw_zip.extractall()
            sconres_xmls = glob.glob('BILLS-115sconres*.xml')
            for x in sconres_xmls:
                with open(x, 'r', encoding='utf8') as sconres_file:
                    for event, elem in ET.iterparse(sconres_file):
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
                                    session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
                                except AttributeError:
                                    print('sconres-session')
                                    continue
                        elif elem.tag == 'session' or elem.tag == 'engrossed-amendment-form' and event == 'end':
                            if elem.tag == 'session':
                                try:
                                    session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
                                except AttributeError:
                                    print('sconres-session')
                                    continue
                            elem.clear
            remove_files(sconres_xmls)
    remove_files(sconres_zips)
    csv_file(number, session, stage)


def parse_sjres(sjres_zips):
    number = []
    session = []
    stage = []
    text = []
    for s in sjres_zips:
        with zipfile.ZipFile(s, 'r') as raw_zip:
            raw_zip.extractall()
            sjres_xmls = glob.glob('BILLS-115sjres*.xml')
            for x in sjres_xmls:
                with open(x, 'r', encoding='utf8') as sjres_file:
                    for event, elem in ET.iterparse(sjres_file):
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
                                    session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
                                except AttributeError:
                                    print('sjres-session')
                                    continue
                        elif elem.tag == 'session' or elem.tag == 'engrossed-amendment-form' and event == 'end':
                            if elem.tag == 'session':
                                try:
                                    session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
                                except AttributeError:
                                    print('sjres-session')
                                    continue
                            elem.clear
            remove_files(sjres_xmls)
    remove_files(sjres_zips)
    csv_file(number, session, stage)


def parse_sres(sres_zips):
    number = []
    session = []
    stage = []
    text = []
    for s in sres_zips:
        with zipfile.ZipFile(s, 'r') as raw_zip:
            raw_zip.extractall()
            sres_xmls = glob.glob('BILLS-115sres*.xml')
            for x in sres_xmls:
                with open(x, 'r', encoding='utf8') as sres_file:
                    for event, elem in ET.iterparse(sres_file):
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
                                    session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
                                except AttributeError:
                                    print('sres-session')
                                    continue
                        elif elem.tag == 'session' or elem.tag == 'engrossed-amendment-form' and event == 'end':
                            if elem.tag == 'session':
                                try:
                                    session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
                                except AttributeError:
                                    print('sres-session')
                                    continue
                            elem.clear
            remove_files(sres_xmls)
    remove_files(sres_zips)
    csv_file(number, session, stage)


def parse_s(s_zips):
    number = []
    session = []
    stage = []
    text = []
    for s in s_zips:
        with zipfile.ZipFile(s, 'r') as raw_zip:
            raw_zip.extractall()
            s_xmls = glob.glob('BILLS-115s*.xml')
            for x in s_xmls:
                with open(x, 'r', encoding='utf8') as s_file:
                    for event, elem in ET.iterparse(s_file):
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
                                    session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
                                except AttributeError:
                                    print('s-session')
                                    continue
                        elif elem.tag == 'session' or elem.tag == 'engrossed-amendment-form' and event == 'end':
                            if elem.tag == 'session':
                                try:
                                    session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
                                except AttributeError:
                                    print('s-session')
                                    continue
                            elem.clear
            remove_files(s_xmls)
    remove_files(s_zips)
    csv_file(number, session, stage)


def remove_files(file):
    for x in file:
        os.remove(x)


def csv_file(number, session, stage):
    title = 'BILLS' + time.strftime('%Y%m%d') + '.csv'
    with open(title, 'a', newline='') as csvfile:
        try:
            writer = csv.writer(csvfile)
            writer.writerows(zip(number, session, stage))
        except Exception as e:
            print(e)
        finally:
            number = []
            session = []
            stage = []


# def push_to_db(whatever):
#     success = bool
#     if success:
#         return 1
#     else:
#         return 0


if __name__ == '__main__':
    main(sys.argv)

# for n, value in enumerate(number, 1):
#     print(n, value)
# for n, value in enumerate(session, 1):
#     print(n, value)
# for n, value in enumerate(stage, 1):
#     print(n, value)
# BILLS_list = zip(number, session, stage)
# for b in BILLS_list:
#     print(b)
# print(len(number))
# print(len(session))
# print(len(stage))
