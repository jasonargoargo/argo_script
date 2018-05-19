#!/jasonargo/anaconda3/bin/python
import urllib.request as req
import zipfile
import xml.etree.ElementTree as ET
import sys
import os
import glob
from pymongo import MongoClient
import pdb


client = MongoClient('localhost:27017')
db = client.argodb

number = []
session = []


def hconres(main):
    global number
    global session
    # pdb.set_trace()
    req.urlretrieve('https://www.govinfo.gov/bulkdata/BILLS/115/1/hconres/BILLS-115-1-hconres.zip', filename='BILLS-115-1-hconres.zip')
    with zipfile.ZipFile('BILLS-115-1-hconres.zip', 'r') as raw_zip:
        raw_zip.extractall()
        os.remove('BILLS-115-1-hconres.zip')
    req.urlretrieve('https://www.govinfo.gov/bulkdata/BILLS/115/2/hconres/BILLS-115-2-hconres.zip', filename='BILLS-115-2-hconres.zip')
    with zipfile.ZipFile('BILLS-115-2-hconres.zip', 'r') as raw_zip:
        raw_zip.extractall()
        os.remove('BILLS-115-2-hconres.zip')
    req.urlretrieve('https://www.govinfo.gov/bulkdata/BILLSTATUS/115/hconres/BILLSTATUS-115-hconres.zip', filename='BILLSTATUS-115-hconres.zip')
    with zipfile.ZipFile('BILLSTATUS-115-hconres.zip', 'r') as raw_zip:
        raw_zip.extractall()
        os.remove('BILLSTATUS-115-hconres.zip')
    hconres_xmls = glob.glob('BILLS*-115hconres*.xml')
    for x in hconres_xmls:
        with open(x, 'r', encoding='utf8') as hconres_data:
            for event, elem in ET.iterparse(hconres_data):
                if elem.tag == 'billNumber':
                    try:
                        number.append(elem.text)
                        db.Congress.insert(
                            {
                                'number': number,
                            })
                        number = []
                        elem.clear()
                    except AttributeError as e:
                        print('%s: %s' % ('hconres-number', e))
                        continue
                if elem.tag == 'form' or elem.tag == 'session':
                    if elem.tag == 'session':
                        try:
                            session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
                            db.Congress.insert(
                                {
                                    'session': session,
                                })
                            number = []
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('hconres-session', e))
                            continue
                if elem.tag == 'engrossed-amendment-form' or elem.tag == 'session':
                    if elem.tag == 'session':
                        try:
                            session.append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
                            db.Congress.insert(
                                {
                                    'session': session,
                                })
                            number = []
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('hconres-amdt-session', e))
                            continue


def remove_files(file):
    for x in file:
        os.remove(x)


if __name__ == '__main__':
    hconres(sys.argv)
