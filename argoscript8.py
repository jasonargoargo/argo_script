#!/jasonargo/anaconda3/bin/python
import urllib.request as req
import zipfile
import xml.etree.ElementTree as ET
import sys
import os
import glob
from pymongo import MongoClient


client = MongoClient('localhost:27017')
db = client.argodb


def main(main):
    congress = '115'
    sessions = ['1', '2']
    types = ['hconres', 'hjres']
    for session in sessions:
        urls = '/' + 'BILLS' + '/' + congress + '/' + session
        zips = 'BILLS' + '-' + congress + '-' + session
        for type in types:
            BILLS_urls = urls + '/' + type + '/'
            BILLS_zips = zips + '-' + type + '.zip'
            retrieve_urls(urls=BILLS_urls, zipfiles=BILLS_zips)
            BILLSTATUS_urls = '/' + 'BILLSTATUS' + '/' + congress + '/' + type + '/'
            BILLSTATUS_zips = 'BILLSTATUS' + '-' + congress + '-' + type + '.zip'
            retrieve_urls(urls=BILLSTATUS_urls, zipfiles=BILLSTATUS_zips)


def retrieve_urls(urls, zipfiles):
    try:
        req.urlretrieve('https://www.govinfo.gov/bulkdata' + urls + zipfiles, filename=zipfiles)
        split_zips(zipfiles)
    except req.URLError as e:
        print('%s: %s' % ('retrieve_urls error', e))
        raise


def split_zips(zipfiles):
    hconres_BILLS_zips = []
    hjres_BILLS_zips = []
    hres_BILLS_zips = []
    hr_BILLS_zips = []
    sconres_BILLS_zips = []
    sjres_BILLS_zips = []
    sres_BILLS_zips = []
    s_BILLS_zips = []
    hconres_BILLSTATUS_zips = []
    hjres_BILLSTATUS_zips = []
    hres_BILLSTATUS_zips = []
    hr_BILLSTATUS_zips = []
    sconres_BILLSTATUS_zips = []
    sjres_BILLSTATUS_zips = []
    sres_BILLSTATUS_zips = []
    s_BILLSTATUS_zips = []
    if zipfiles in 'BILLS-115-1-hconres.zip':
        hconres_BILLS_zips.append('BILLS-115-1-hconres.zip')
        parse_hconres_BILLS(hconres_BILLS_zips)
    elif zipfiles in 'BILLS-115-2-hconres.zip':
        hconres_BILLS_zips.append('BILLS-115-2-hconres.zip')
        parse_hconres_BILLS(hconres_BILLS_zips)
    elif zipfiles in 'BILLS-115-1-hjres.zip':
        hjres_BILLS_zips.append('BILLS-115-1-hjres.zip')
        parse_hjres_BILLS(hjres_BILLS_zips)
    elif zipfiles in 'BILLS-115-2-hjres.zip':
        hjres_BILLS_zips.append('BILLS-115-2-hjres.zip')
        parse_hjres_BILLS(hjres_BILLS_zips)
    # elif zipfiles in 'BILLS-115-1-hres.zip':
    #     hres_BILLS_zips.append('BILLS-115-1-hres.zip')
    #     parse_hres_BILLS(hres_BILLS_zips)
    # elif zipfiles in 'BILLS-115-2-hres.zip':
    #     hres_BILLS_zips.append('BILLS-115-2-hres.zip')
    #     parse_hres_BILLS(hres_BILLS_zips)
    # elif zipfiles in 'BILLS-115-1-hr.zip':
    #     hr_BILLS_zips.append('BILLS-115-1-hr.zip')
    #     parse_hr_BILLS(hr_BILLS_zips)
    # elif zipfiles in 'BILLS-115-2-hr.zip':
    #     hr_BILLS_zips.append('BILLS-115-2-hr.zip')
    #     parse_hr_BILLS(hr_BILLS_zips)
    # elif zipfiles in 'BILLS-115-1-sconres.zip':
    #     sconres_BILLS_zips.append('BILLS-115-1-sconres.zip')
    #     parse_sconres_BILLS(sconres_BILLS_zips)
    # elif zipfiles in 'BILLS-115-2-sconres.zip':
    #     sconres_BILLS_zips.append('BILLS-115-2-sconres.zip')
    #     parse_sconres_BILLS(sconres_BILLS_zips)
    # elif zipfiles in 'BILLS-115-1-sjres.zip':
    #     sjres_BILLS_zips.append('BILLS-115-1-sjres.zip')
    #     parse_sjres_BILLS(sjres_BILLS_zips)
    # elif zipfiles in 'BILLS-115-2-sjres.zip':
    #     sjres_BILLS_zips.append('BILLS-115-2-sjres.zip')
    #     parse_sjres_BILLS(sjres_BILLS_zips)
    # elif zipfiles in 'BILLS-115-1-sres.zip':
    #     sres_BILLS_zips.append('BILLS-115-1-sres.zip')
    #     parse_sres_BILLS(sres_BILLS_zips)
    # elif zipfiles in 'BILLS-115-2-sres.zip':
    #     sres_BILLS_zips.append('BILLS-115-2-sres.zip')
    #     parse_sres_BILLS(sres_BILLS_zips)
    # elif zipfiles in 'BILLS-115-1-s.zip':
    #     s_BILLS_zips.append('BILLS-115-1-s.zip')
    #     parse_s_BILLS(s_BILLS_zips)
    # elif zipfiles in 'BILLS-115-2-s.zip':
    #     s_BILLS_zips.append('BILLS-115-2-s.zip')
    #     parse_s_BILLS(s_BILLS_zips)
    # elif zipfiles in 'BILLSTATUS-115-hconres.zip':
    #     hconres_BILLSTATUS_zips.append('BILLSTATUS-115-hconres.zip')
    #     parse_hconres_BILLSTATUS(hconres_BILLSTATUS_zips)
    # elif zipfiles in 'BILLSTATUS-115-hjres.zip':
    #     hjres_BILLSTATUS_zips.append('BILLSTATUS-115-hjres.zip')
    #     parse_hjres_BILLSTATUS(hjres_BILLSTATUS_zips)
    # if zipfiles in 'BILLSTATUS-115-hres.zip':
    #     hres_BILLSTATUS_zips.append('BILLSTATUS-115-hres.zip')
    #     parse_hres_BILLSTATUS(hres_BILLSTATUS_zips)
    # elif zipfiles in 'BILLSTATUS-115-hr.zip':
    #     hr_BILLSTATUS_zips.append('BILLSTATUS-115-hr.zip')
    #     parse_hr_BILLSTATUS(hr_BILLSTATUS_zips)
    # if zipfiles in 'BILLSTATUS-115-sconres.zip':
    #     sconres_BILLSTATUS_zips.append('BILLSTATUS-115-sconres.zip')
    #     parse_sconres_BILLSTATUS(sconres_BILLSTATUS_zips)
    # elif zipfiles in 'BILLSTATUS-115-sjres.zip':
    #     sjres_BILLSTATUS_zips.append('BILLSTATUS-115-sjres.zip')
    #     parse_sjres_BILLSTATUS(sjres_BILLSTATUS_zips)
    # if zipfiles in 'BILLSTATUS-115-sres.zip':
    #     sres_BILLSTATUS_zips.append('BILLSTATUS-115-sres.zip')
    #     parse_sres_BILLSTATUS(sres_BILLSTATUS_zips)
    # elif zipfiles in 'BILLSTATUS-115-s.zip':
    #     s_BILLSTATUS_zips.append('BILLSTATUS-115-s.zip')
    #     parse_hjres_BILLSTATUS(s_BILLSTATUS_zips)
    else:
        print('%s: %s' % ('Unused zips', zipfiles))
    zipfiles = []


def parse_hconres_BILLS(hconres_BILLS_zips):
    number = []
    session = []
    stage = []
    # text = []
    for h in hconres_BILLS_zips:
        with zipfile.ZipFile(h, 'r') as raw_zip:
            raw_zip.extractall()
            hconres_xmls = glob.glob('BILLS-115hconres*.xml')
            for x in hconres_xmls:
                with open(x, 'r', encoding='utf8') as hconres_file:
                    for event, elem in ET.iterparse(hconres_file):
                        if elem.tag == 'resolution':
                            try:
                                stage.append(elem.get('resolution-stage').title().replace('-', ' '))
                                elem.clear()
                            except AttributeError as e:
                                print('%s: %s' % ('hconres-stage', e))
                                continue
                        elif elem.tag == 'amendment-doc':
                            try:
                                stage.append(elem.get('amend-type').title().replace('-', ' '))
                                elem.clear()
                            except AttributeError as e:
                                print('%s: %s' % ('hconres-amdt-stage', e))
                                continue
                        elif elem.tag == 'legis-num' or elem.tag == 'form':
                            if elem.tag == 'legis-num':
                                try:
                                    number.append(elem.text.title())
                                    elem.clear()
                                except AttributeError as e:
                                    print('%s: %s' % ('hconres-number', e))
                                    continue
                        elif elem.tag == 'legis-num' or elem.tag == 'engrossed-amendment-form':
                            if elem.tag == 'legis-num':
                                try:
                                    number.append(elem.text.title())
                                    elem.clear()
                                except AttributeError as e:
                                    print('%s: %s' % ('hconres-amdt-number', e))
                                    continue
                        elif elem.tag == 'session' or elem.tag == 'form':
                            if elem.tag == 'session':
                                try:
                                    session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
                                    elem.clear()
                                except AttributeError as e:
                                    print('%s: %s' % ('hconres-session', e))
                                    continue
                        elif elem.tag == 'session' or elem.tag == 'engrossed-amendment-form':
                            if elem.tag == 'session':
                                try:
                                    session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
                                    elem.clear()
                                except AttributeError as e:
                                    print('%s: %s' % ('hconres-amdt-session', e))
                                    continue
                        try:
                            db.BILLS.insert(
                                {
                                    'number': number,
                                    'session': session,
                                    'stage': stage,
                                })
                            print('Inserted data successfully')
                        except Exception as e:
                            print(str(e))
                    # with open(x, 'r', encoding='utf8') as fulltext:
                    #     read_text = fulltext.read()
                    #     root = ET.fromstring(read_text)
                    #     split_text = [line.split('\n') for line in root.itertext()]
                    #     text.append(split_text)
                    #     return text
            remove_files(hconres_xmls)
    remove_files(hconres_BILLS_zips)


def parse_hjres_BILLS(hjres_BILLS_zips):
    number = []
    session = []
    stage = []
    # text = []
    for h in hjres_BILLS_zips:
        with zipfile.ZipFile(h, 'r') as raw_zip:
            raw_zip.extractall()
            hjres_xmls = glob.glob('BILLS-115hjres*.xml')
            for x in hjres_xmls:
                with open(x, 'r', encoding='utf8') as hjres_file:
                    for event, elem in ET.iterparse(hjres_file):
                        if elem.tag == 'resolution':
                            try:
                                stage.append(elem.get('resolution-stage').title().replace('-', ' '))
                                elem.clear()
                            except AttributeError as e:
                                print('%s: %s' % ('hjres-stage', e))
                                continue
                        elif elem.tag == 'amendment-doc':
                            try:
                                stage.append(elem.get('amend-type').title().replace('-', ' '))
                                elem.clear()
                            except AttributeError as e:
                                print('%s: %s' % ('hjres-amdt-stage', e))
                                continue
                        elif elem.tag == 'legis-num' or elem.tag == 'form':
                            if elem.tag == 'legis-num':
                                try:
                                    number.append(elem.text.title())
                                    elem.clear()
                                except AttributeError as e:
                                    print('%s: %s' % ('hjres-number', e))
                                    continue
                        elif elem.tag == 'legis-num' or elem.tag == 'engrossed-amendment-form':
                            if elem.tag == 'legis-num':
                                try:
                                    number.append(elem.text.title())
                                    elem.clear()
                                except AttributeError as e:
                                    print('%s: %s' % ('hjres-amdt-number', e))
                                    continue
                        elif elem.tag == 'session' or elem.tag == 'form':
                            if elem.tag == 'session':
                                try:
                                    session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
                                    elem.clear()
                                except AttributeError as e:
                                    print('%s: %s' % ('hjres-session', e))
                                    continue
                        elif elem.tag == 'session' or elem.tag == 'engrossed-amendment-form':
                            if elem.tag == 'session':
                                try:
                                    session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
                                    elem.clear()
                                except AttributeError as e:
                                    print('%s: %s' % ('hjres-amdt-session', e))
                                    continue
                        try:
                            db.BILLS.insert(
                                {
                                    'number': number,
                                    'session': session,
                                    'stage': stage,
                                })
                            print('Inserted data successfully')
                        except Exception as e:
                            print(str(e))
                # with open(x, 'r', encoding='utf8') as fulltext:
                #     read_text = fulltext.read()
                #     root = ET.fromstring(read_text)
                #     split_text = [line.split('\n') for line in root.itertext()]
                #     text.append(split_text)
                #     return text
            remove_files(hjres_xmls)
    remove_files(hjres_BILLS_zips)


# def parse_hres_BILLS(hres_BILLS_zips):
#     number = []
#     session = []
#     stage = []
#     text = []
#     for h in hres_BILLS_zips:
#         with zipfile.ZipFile(h, 'r') as raw_zip:
#             raw_zip.extractall()
#             hres_xmls = glob.glob('BILLS-115hres*.xml')
#             for x in hres_xmls:
#                 with open(x, 'r', encoding='utf8') as hres_file:
#                     for event, elem in ET.iterparse(hres_file):
#                         if elem.tag == 'resolution':
#                             try:
#                                 stage.append(elem.get('resolution-stage').title().replace('-', ' '))
#                                 elem.clear()
#                             except AttributeError as e:
#                                 print('%s: %s' % ('hres-stage', e))
#                                 continue
#                         elif elem.tag == 'amendment-doc':
#                             try:
#                                 stage.append(elem.get('amend-type').title().replace('-', ' '))
#                                 elem.clear()
#                             except AttributeError as e:
#                                 print('%s: %s' % ('hres-amdt-stage', e))
#                                 continue
#                         elif elem.tag == 'legis-num' or elem.tag == 'form':
#                             if elem.tag == 'legis-num':
#                                 try:
#                                     number.append(elem.text.title())
#                                     elem.clear()
#                                 except AttributeError as e:
#                                     print('%s: %s' % ('hres-number', e))
#                                     continue
#                         elif elem.tag == 'legis-num' or elem.tag == 'engrossed-amendment-form':
#                             if elem.tag == 'legis-num':
#                                 try:
#                                     number.append(elem.text.title())
#                                     elem.clear()
#                                 except AttributeError as e:
#                                     print('%s: %s' % ('hres-amdt-number', e))
#                                     continue
#                         elif elem.tag == 'session' or elem.tag == 'form':
#                             if elem.tag == 'session':
#                                 try:
#                                     session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
#                                     elem.clear()
#                                 except AttributeError as e:
#                                     print('%s: %s' % ('hres-session', e))
#                                     continue
#                         elif elem.tag == 'session' or elem.tag == 'engrossed-amendment-form':
#                             if elem.tag == 'session':
#                                 try:
#                                     session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
#                                     elem.clear()
#                                 except AttributeError as e:
#                                     print('%s: %s' % ('hres-amdt-session', e))
#                                     continue
#                 with open(x, 'r', encoding='utf8') as fulltext:
#                     read_text = fulltext.read()
#                     root = ET.fromstring(read_text)
#                     split_text = [line.split('\n') for line in root.itertext()]
#                     text.append(split_text)
#             remove_files(hres_xmls)
#     remove_files(hres_BILLS_zips)
#     csv_file(number, session, stage, text)


# def parse_hr_BILLS(hr_BILLS_zips):
#     number = []
#     session = []
#     stage = []
#     text = []
#     for h in hr_BILLS_zips:
#         with zipfile.ZipFile(h, 'r') as raw_zip:
#             raw_zip.extractall()
#             hr_xmls = glob.glob('BILLS-115hr*.xml')
#             for x in hr_xmls:
#                 with open(x, 'r', encoding='utf8') as hr_file:
#                     for event, elem in ET.iterparse(hr_file):
#                         if elem.tag == 'bill':
#                             try:
#                                 stage.append(elem.get('bill-stage').title().replace('-', ' '))
#                                 elem.clear()
#                             except AttributeError as e:
#                                 print('%s: %s' % ('hr-stage', e))
#                                 continue
#                         elif elem.tag == 'amendment-doc':
#                             try:
#                                 stage.append(elem.get('amend-type').title().replace('-', ' '))
#                                 elem.clear()
#                             except AttributeError as e:
#                                 print('%s: %s' % ('hr-amdt-stage', e))
#                                 continue
#                         elif elem.tag == 'legis-num' or elem.tag == 'form':
#                             if elem.tag == 'legis-num':
#                                 try:
#                                     number.append(elem.text.title())
#                                     elem.clear()
#                                 except AttributeError as e:
#                                     print('%s: %s' % ('hr-number', e))
#                                     continue
#                         elif elem.tag == 'legis-num' or elem.tag == 'engrossed-amendment-form':
#                             if elem.tag == 'legis-num':
#                                 try:
#                                     number.append(elem.text.title())
#                                     elem.clear()
#                                 except AttributeError as e:
#                                     print('%s: %s' % ('hr-amdt-number', e))
#                                     continue
#                         elif elem.tag == 'session' or elem.tag == 'form':
#                             if elem.tag == 'session':
#                                 try:
#                                     session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
#                                     elem.clear()
#                                 except AttributeError as e:
#                                     print('%s: %s' % ('hr-session', e))
#                                     continue
#                         elif elem.tag == 'session' or elem.tag == 'engrossed-amendment-form':
#                             if elem.tag == 'session':
#                                 try:
#                                     session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
#                                     elem.clear()
#                                 except AttributeError as e:
#                                     print('%s: %s' % ('hr-amdt-session', e))
#                                     continue
#                 with open(x, 'r', encoding='utf8') as fulltext:
#                     read_text = fulltext.read()
#                     root = ET.fromstring(read_text)
#                     split_text = [line.split('\n') for line in root.itertext()]
#                     text.append(split_text)
#             remove_files(hr_xmls)
#     remove_files(hr_BILLS_zips)
#     csv_file(number, session, stage, text)


# def parse_sconres_BILLS(sconres_BILLS_zips):
#     number = []
#     session = []
#     stage = []
#     text = []
#     for s in sconres_BILLS_zips:
#         with zipfile.ZipFile(s, 'r') as raw_zip:
#             raw_zip.extractall()
#             sconres_xmls = glob.glob('BILLS-115sconres*.xml')
#             for x in sconres_xmls:
#                 with open(x, 'r', encoding='utf8') as sconres_file:
#                     for event, elem in ET.iterparse(sconres_file):
#                         if elem.tag == 'resolution':
#                             try:
#                                 stage.append(elem.get('resolution-stage').title().replace('-', ' '))
#                                 elem.clear()
#                             except AttributeError as e:
#                                 print('%s: %s' % ('sconres-stage', e))
#                                 continue
#                         elif elem.tag == 'amendment-doc':
#                             try:
#                                 stage.append(elem.get('amend-type').title().replace('-', ' '))
#                                 elem.clear()
#                             except AttributeError as e:
#                                 print('%s: %s' % ('sconres-amdt-stage', e))
#                                 continue
#                         elif elem.tag == 'legis-num' or elem.tag == 'form':
#                             if elem.tag == 'legis-num':
#                                 try:
#                                     number.append(elem.text.title())
#                                     elem.clear()
#                                 except AttributeError as e:
#                                     print('%s: %s' % ('sconres-number', e))
#                                     continue
#                         elif elem.tag == 'legis-num' or elem.tag == 'engrossed-amendment-form':
#                             if elem.tag == 'legis-num':
#                                 try:
#                                     number.append(elem.text.title())
#                                     elem.clear()
#                                 except AttributeError as e:
#                                     print('%s: %s' % ('sconres-amdt-number', e))
#                                     continue
#                         elif elem.tag == 'session' or elem.tag == 'form':
#                             if elem.tag == 'session':
#                                 try:
#                                     session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
#                                     elem.clear()
#                                 except AttributeError as e:
#                                     print('%s: %s' % ('sconres-session', e))
#                                     continue
#                         elif elem.tag == 'session' or elem.tag == 'engrossed-amendment-form':
#                             if elem.tag == 'session':
#                                 try:
#                                     session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
#                                     elem.clear()
#                                 except AttributeError as e:
#                                     print('%s: %s' % ('sconres-amdt-session', e))
#                                     continue
#                 with open(x, 'r', encoding='utf8') as fulltext:
#                     read_text = fulltext.read()
#                     root = ET.fromstring(read_text)
#                     split_text = [line.split('\n') for line in root.itertext()]
#                     text.append(split_text)
#             remove_files(sconres_xmls)
#     remove_files(sconres_BILLS_zips)
#     csv_file(number, session, stage, text)


# def parse_sjres_BILLS(sjres_BILLS_zips):
#     number = []
#     session = []
#     stage = []
#     text = []
#     for s in sjres_BILLS_zips:
#         with zipfile.ZipFile(s, 'r') as raw_zip:
#             raw_zip.extractall()
#             sjres_xmls = glob.glob('BILLS-115sjres*.xml')
#             for x in sjres_xmls:
#                 with open(x, 'r', encoding='utf8') as sjres_file:
#                     for event, elem in ET.iterparse(sjres_file):
#                         if elem.tag == 'resolution':
#                             try:
#                                 stage.append(elem.get('resolution-stage').title().replace('-', ' '))
#                                 elem.clear()
#                             except AttributeError as e:
#                                 print('%s: %s' % ('sjres-stage', e))
#                                 continue
#                         elif elem.tag == 'amendment-doc':
#                             try:
#                                 stage.append(elem.get('amend-type').title().replace('-', ' '))
#                                 elem.clear()
#                             except AttributeError as e:
#                                 print('%s: %s' % ('sjres-amdt-stage', e))
#                                 continue
#                         elif elem.tag == 'legis-num' or elem.tag == 'form':
#                             if elem.tag == 'legis-num':
#                                 try:
#                                     number.append(elem.text.title())
#                                     elem.clear()
#                                 except AttributeError as e:
#                                     print('%s: %s' % ('sjres-number', e))
#                                     continue
#                         elif elem.tag == 'legis-num' or elem.tag == 'engrossed-amendment-form':
#                             if elem.tag == 'legis-num':
#                                 try:
#                                     number.append(elem.text.title())
#                                     elem.clear()
#                                 except AttributeError as e:
#                                     print('%s: %s' % ('sjres-amdt-number', e))
#                                     continue
#                         elif elem.tag == 'session' or elem.tag == 'form':
#                             if elem.tag == 'session':
#                                 try:
#                                     session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
#                                     elem.clear()
#                                 except AttributeError as e:
#                                     print('%s: %s' % ('sjres-session', e))
#                                     continue
#                         elif elem.tag == 'session' or elem.tag == 'engrossed-amendment-form':
#                             if elem.tag == 'session':
#                                 try:
#                                     session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
#                                     elem.clear()
#                                 except AttributeError as e:
#                                     print('%s: %s' % ('sjres-amdt-session', e))
#                                     continue
#                 with open(x, 'r', encoding='utf8') as fulltext:
#                     read_text = fulltext.read()
#                     root = ET.fromstring(read_text)
#                     split_text = [line.split('\n') for line in root.itertext()]
#                     text.append(split_text)
#             remove_files(sjres_xmls)
#     remove_files(sjres_BILLS_zips)
#     csv_file(number, session, stage, text)


# def parse_sres_BILLS(sres_BILLS_zips):
#     number = []
#     session = []
#     stage = []
#     text = []
#     for s in sres_BILLS_zips:
#         with zipfile.ZipFile(s, 'r') as raw_zip:
#             raw_zip.extractall()
#             sres_xmls = glob.glob('BILLS-115sres*.xml')
#             for x in sres_xmls:
#                 with open(x, 'r', encoding='utf8') as sres_file:
#                     for event, elem in ET.iterparse(sres_file):
#                         if elem.tag == 'resolution':
#                             try:
#                                 stage.append(elem.get('resolution-stage').title().replace('-', ' '))
#                                 elem.clear()
#                             except AttributeError as e:
#                                 print('%s: %s' % ('sres-stage', e))
#                                 continue
#                         elif elem.tag == 'amendment-doc':
#                             try:
#                                 stage.append(elem.get('amend-type').title().replace('-', ' '))
#                                 elem.clear()
#                             except AttributeError as e:
#                                 print('%s: %s' % ('sres-amdt-stage', e))
#                                 continue
#                         elif elem.tag == 'legis-num' or elem.tag == 'form':
#                             if elem.tag == 'legis-num':
#                                 try:
#                                     number.append(elem.text.title())
#                                     elem.clear()
#                                 except AttributeError as e:
#                                     print('%s: %s' % ('sres-number', e))
#                                     continue
#                         elif elem.tag == 'legis-num' or elem.tag == 'engrossed-amendment-form':
#                             if elem.tag == 'legis-num':
#                                 try:
#                                     number.append(elem.text.title())
#                                     elem.clear()
#                                 except AttributeError as e:
#                                     print('%s: %s' % ('sres-amdt-number', e))
#                                     continue
#                         elif elem.tag == 'session' or elem.tag == 'form':
#                             if elem.tag == 'session':
#                                 try:
#                                     session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
#                                     elem.clear()
#                                 except AttributeError as e:
#                                     print('%s: %s' % ('sres-session', e))
#                                     continue
#                         elif elem.tag == 'session' or elem.tag == 'engrossed-amendment-form':
#                             if elem.tag == 'session':
#                                 try:
#                                     session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
#                                     elem.clear()
#                                 except AttributeError as e:
#                                     print('%s: %s' % ('sres-amdt-session', e))
#                                     continue
#                 with open(x, 'r', encoding='utf8') as fulltext:
#                     read_text = fulltext.read()
#                     root = ET.fromstring(read_text)
#                     split_text = [line.split('\n') for line in root.itertext()]
#                     text.append(split_text)
#             remove_files(sres_xmls)
#     remove_files(sres_BILLS_zips)
#     csv_file(number, session, stage, text)


# def parse_s_BILLS(s_BILLS_zips):
#     number = []
#     session = []
#     stage = []
#     text = []
#     for s in s_BILLS_zips:
#         with zipfile.ZipFile(s, 'r') as raw_zip:
#             raw_zip.extractall()
#             s_xmls = glob.glob('BILLS-115s*.xml')
#             for x in s_xmls:
#                 with open(x, 'r', encoding='utf8') as s_file:
#                     for event, elem in ET.iterparse(s_file):
#                         if elem.tag == 'bill':
#                             try:
#                                 stage.append(elem.get('bill-stage').title().replace('-', ' '))
#                                 elem.clear()
#                             except AttributeError as e:
#                                 print('%s: %s' % ('s-stage', e))
#                                 continue
#                         elif elem.tag == 'amendment-doc':
#                             try:
#                                 stage.append(elem.get('amend-type').title().replace('-', ' '))
#                                 elem.clear()
#                             except AttributeError as e:
#                                 print('%s: %s' % ('s-amdt-stage', e))
#                                 continue
#                         elif elem.tag == 'legis-num' or elem.tag == 'form':
#                             if elem.tag == 'legis-num':
#                                 try:
#                                     number.append(elem.text.title())
#                                     elem.clear()
#                                 except AttributeError as e:
#                                     print('%s: %s' % ('s-number', e))
#                                     continue
#                         elif elem.tag == 'legis-num' or elem.tag == 'engrossed-amendment-form':
#                             if elem.tag == 'legis-num':
#                                 try:
#                                     number.append(elem.text.title())
#                                     elem.clear()
#                                 except AttributeError as e:
#                                     print('%s: %s' % ('s-amdt-number', e))
#                                     continue
#                         elif elem.tag == 'session' or elem.tag == 'form':
#                             if elem.tag == 'session':
#                                 try:
#                                     session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
#                                     elem.clear()
#                                 except AttributeError as e:
#                                     print('%s: %s' % ('s-session', e))
#                                     continue
#                         elif elem.tag == 'session' or elem.tag == 'engrossed-amendment-form':
#                             if elem.tag == 'session':
#                                 try:
#                                     session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
#                                     elem.clear()
#                                 except AttributeError as e:
#                                     print('%s: %s' % ('s-amdt-session', e))
#                                     continue
#                 with open(x, 'r', encoding='utf8') as fulltext:
#                     read_text = fulltext.read()
#                     root = ET.fromstring(read_text)
#                     split_text = [line.split('\n') for line in root.itertext()]
#                     text.append(split_text)
#             remove_files(s_xmls)
#     remove_files(s_BILLS_zips)
#     csv_file(number, session, stage, text)


# def parse_hconres_BILLSTATUS(hconres_BILLSTATUS_zips):
#     sponsor = []
#     cosponsor = []
#     for h in hconres_BILLSTATUS_zips:
#         with zipfile.ZipFile(h, 'r') as raw_zip:
#             raw_zip.extractall()
#             hconres_xmls = glob.glob('BILLSTATUS-115hconres*.xml')
#             for x in hconres_xmls:
#                 with open(x, 'r', encoding='utf8') as hconres_file:
#                     for event, elem in ET.iterparse(hconres_file):
#                         if elem.tag == 'sponsors' or elem.tag == 'bioguideID':
#                             if elem.tag == 'bioguideID':
#                                 try:
#                                     sponsor.append(elem.text)
#                                     return sponsor
#                                     elem.clear()
#                                 except AttributeError as e:
#                                     print('%s: %s' % ('hconres-sponsor', e))
#                                     continue
#             remove_files(hconres_xmls)
#     remove_files(hconres_BILLSTATUS_zips)
    # push_to_argodb(sponsor, cosponsor)


# def parse_hjres_BILLSTATUS(hjres_BILLSTATUS_zips):
#     sponsor = []
#     cosponsor = []
#     for h in hjres_BILLSTATUS_zips:
#         with zipfile.ZipFile(h, 'r') as raw_zip:
#             raw_zip.extractall()
#             hjres_xmls = glob.glob('BILLSTATUS-115hjres*.xml')
#             for x in hjres_xmls:
#                 with open(x, 'r', encoding='utf8') as hjres_file:
#                     for event, elem in ET.iterparse(hjres_file):
#                         if elem.tag == 'sponsors' or elem.tag == 'bioguideID':
#                             if elem.tag == 'bioguideID':
#                                 try:
#                                     sponsor.append(elem.text)
#                                     return sponsor
#                                     elem.clear
#                                 except AttributeError as e:
#                                     print('%s: %s' % ('hjres-sponsor', e))
#                                     continue
#             remove_files(hjres_xmls)
#     remove_files(hjres_BILLSTATUS_zips)
    # push_to_argodb(sponsor, cosponsor)


def parse_hres_BILLSTATUS(hres_BILLSTATUS_zips):
    pass


def parse_hr_BILLSTATUS(hr_BILLSTATUS_zips):
    pass


def parse_sconres_BILLSTATUS(sconres_BILLSTATUS_zips):
    pass


def parse_sjres_BILLSTATUS(sjres_BILLSTATUS_zips):
    pass


def parse_sres_BILLSTATUS(sres_BILLSTATUS_zips):
    pass


def parse_s_BILLSTATUS(s_BILLSTATUS_zips):
    pass


def remove_files(file):
    for x in file:
        os.remove(x)


if __name__ == '__main__':
    main(sys.argv)
    # push_to_argodb(number, session, stage)
