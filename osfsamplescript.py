import urllib.request as req
import zipfile
import xml.etree.ElementTree as ET
import sys
import os
import glob
import time
import csv


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
    hconres_BILLSTATUS_zips = []
    hjres_BILLSTATUS_zips = []
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
    elif zipfiles in 'BILLSTATUS-115-hconres.zip':
        hconres_BILLSTATUS_zips.append('BILLSTATUS-115-hconres.zip')
        parse_hconres_BILLSTATUS(hconres_BILLSTATUS_zips)
    elif zipfiles in 'BILLSTATUS-115-hjres.zip':
        hjres_BILLSTATUS_zips.append('BILLSTATUS-115-hjres.zip')
        parse_hjres_BILLSTATUS(hjres_BILLSTATUS_zips)
    else:
        print('%s: %s' % ('Unused zips', zipfiles))
    zipfiles = []


def parse_hconres_BILLS(hconres_BILLS_zips):
    number = []
    for h in hconres_BILLS_zips:
        with zipfile.ZipFile(h, 'r') as raw_zip:
            raw_zip.extractall()
            hconres_xmls = glob.glob('BILLS-115hconres*.xml')
            for x in hconres_xmls:
                with open(x, 'r', encoding='utf8') as hconres_file:
                    for event, elem in ET.iterparse(hconres_file):
                        if elem.tag == 'legis-num' or elem.tag == 'form':
                            if elem.tag == 'legis-num':
                                try:
                                    number.append(elem.text.title())
                                    return number
                                    elem.clear()
                                except AttributeError as e:
                                    print('%s: %s' % ('hconres-number', e))
                                    continue
                        elif elem.tag == 'legis-num' or elem.tag == 'engrossed-amendment-form':
                            if elem.tag == 'legis-num':
                                try:
                                    number.append(elem.text.title())
                                    return number
                                    elem.clear()
                                except AttributeError as e:
                                    print('%s: %s' % ('hconres-amdt-number', e))
                                    continue
            remove_files(hconres_xmls)
    remove_files(hconres_BILLS_zips)


def parse_hjres_BILLS(hjres_BILLS_zips):
    number = []
    for h in hjres_BILLS_zips:
        with zipfile.ZipFile(h, 'r') as raw_zip:
            raw_zip.extractall()
            hjres_xmls = glob.glob('BILLS-115hjres*.xml')
            for x in hjres_xmls:
                with open(x, 'r', encoding='utf8') as hjres_file:
                    for event, elem in ET.iterparse(hjres_file):
                        if elem.tag == 'legis-num' or elem.tag == 'form':
                            if elem.tag == 'legis-num':
                                try:
                                    number.append(elem.text.title())
                                    return number
                                    elem.clear()
                                except AttributeError as e:
                                    print('%s: %s' % ('hjres-number', e))
                                    continue
                        elif elem.tag == 'legis-num' or elem.tag == 'engrossed-amendment-form':
                            if elem.tag == 'legis-num':
                                try:
                                    number.append(elem.text.title())
                                    return number
                                    elem.clear()
                                except AttributeError as e:
                                    print('%s: %s' % ('hjres-amdt-number', e))
                                    continue
            remove_files(hjres_xmls)
    remove_files(hjres_BILLS_zips)


def parse_hconres_BILLSTATUS(hconres_BILLSTATUS_zips):
    sponsor = []
    for h in hconres_BILLSTATUS_zips:
        with zipfile.ZipFile(h, 'r') as raw_zip:
            raw_zip.extractall()
            hconres_xmls = glob.glob('BILLSTATUS-115hconres*.xml')
            for x in hconres_xmls:
                with open(x, 'r', encoding='utf8') as hconres_file:
                    for event, elem in ET.iterparse(hconres_file):
                        if elem.tag == 'sponsors' or elem.tag == 'bioguideID':
                            if elem.tag == 'bioguideID':
                                try:
                                    sponsor.append(elem.text)
                                    return sponsor
                                    elem.clear()
                                except AttributeError as e:
                                    print('%s: %s' % ('hconres-sponsor', e))
                                    continue
            remove_files(hconres_xmls)
    remove_files(hconres_BILLSTATUS_zips)


def parse_hjres_BILLSTATUS(hjres_BILLSTATUS_zips):
    sponsor = []
    for h in hjres_BILLSTATUS_zips:
        with zipfile.ZipFile(h, 'r') as raw_zip:
            raw_zip.extractall()
            hjres_xmls = glob.glob('BILLSTATUS-115hjres*.xml')
            for x in hjres_xmls:
                with open(x, 'r', encoding='utf8') as hjres_file:
                    for event, elem in ET.iterparse(hjres_file):
                        if elem.tag == 'sponsors' or elem.tag == 'bioguideID':
                            if elem.tag == 'bioguideID':
                                try:
                                    sponsor.append(elem.text)
                                    return sponsor
                                    elem.clear
                                except AttributeError as e:
                                    print('%s: %s' % ('hjres-sponsor', e))
                                    continue
            remove_files(hjres_xmls)
    remove_files(hjres_BILLSTATUS_zips)


def remove_files(file):
    for x in file:
        os.remove(x)


def csv_file(*args):
    lists = []
    for a in args:
        lists += a
    print(lists)


csv_file(parse_hconres_BILLS(), parse_hjres_BILLS(), parse_hconres_BILLSTATUS(), parse_hjres_BILLSTATUS())


# def csv_file(*args):
#     title = 'data' + time.strftime('%Y%m%d') + '.csv'
#     with open(title, 'a', newline='') as csvfile:
#         try:
#             writer = csv.writer(csvfile)
#             writer.writerows(zip(number, session, stage, sponsor, text))
#         except Exception as e:
#             print('%s: %s' % ('csv Exception', e))
#         finally:
#             number = []
#             session = []
#             stage = []
#             sponsor = []
#             text = []


if __name__ == '__main__':
    main(sys.argv)
