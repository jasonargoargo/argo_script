#!/usr/bin/python3
import urllib.request as req
import zipfile
import xml.etree.ElementTree as ET
import sys
import os
import glob
from pymongo import MongoClient
import pymongo.errors
import pdb


client = MongoClient('localhost:27017')
db = client.argodb


def hconres(main):
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
    hconres_BILLS_xmls = glob.glob('BILLS-115hconres*.xml')
    hconres_BILLSTATUS_xmls = glob.glob('BILLSTATUS-115hconres*.xml')
    for x in hconres_BILLS_xmls:
        with open(x, 'r', encoding='utf8') as hconres_data:
            #  'BILLS' GENERAL LEGISLATION DATA MONGO DOCUMENT
            filename = x.strip('.xml')
            data = {
                '_id': filename,
                'session': [],
                'pub-pri': [],
            }
            for event, elem in ET.iterparse(hconres_data):
                if elem.tag == 'form' or elem.tag == 'session':
                    if elem.tag == 'session':
                        try:
                            data['session'].append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('hconres-session', e))
                            continue
                if elem.tag == 'engrossed-amendment-form' or elem.tag == 'session':
                    if elem.tag == 'session':
                        try:
                            data['session'].append(''.join(elem.text.replace('At the First Session', '1st').replace('1st Session', '1st').replace(' 2d Session', '2nd').replace('2d Session', '2nd').replace(' 2nd Session', '2nd').replace('2d  Session', '2nd').replace('At the Second Session', '2nd')))
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('hconres-amdt-session', e))
                            continue
                if elem.tag == 'resolution':
                    try:
                        data['pub-pri'].append(elem.get('public-private').title().replace('-', ' '))
                        elem.clear()
                    except AttributeError as e:
                        print('%s: %s' % ('hconres-pub-pri', e))
                        continue
                if elem.tag == 'bill':
                    try:
                        data['pub-pri'].append(elem.get('public-private').title().replace('-', ' '))
                        elem.clear()
                    except AttributeError as e:
                        print('%s: %s' % ('hconres-pub-pri', e))
                        continue
            try:
                db.test.update_one(data, {'$set': {'_id': data['_id'], 'session': data['session'], 'pub-pri': data['pub-pri']}}, upsert=True)
            except pymongo.errors.ConnectionFailure as e:
                print(e)
        with open(x, 'r', encoding='utf8') as fulltext:
            #  LEGISLATION TEXT MONGO DOCUMENT
            filename = x.strip('.xml')
            data = {
                '_id': filename,
                'fulltext': []
            }
            read_text = fulltext.read()
            root = ET.fromstring(read_text)
            split_text = [line.split('\n') for line in root.itertext()]
            data['fulltext'].append(split_text)
            try:
                db.test.update_one(data, {'$set': {'_id': data['_id'], 'fulltext': data['fulltext']}}, upsert=True)
            except pymongo.errors.ConnectionFailure as e:
                print(e)
    for x in hconres_BILLSTATUS_xmls:
        with open(x, 'r', encoding='utf8') as hconres_data:
            #  'BILLSTATUS' GENERAL LEGISLATION DATA MONGO DOCUMENT
            filename = x.strip('.xml')
            data = {
                '_id': filename,
                'num': [],
                'title': [],
                'type': [],
                'sponsor_bioguideID': [],
                'cosponsor_bioguideID': [],
                'amdt_num': [],
                'amdt_title': [],
                'amdt_congress': [],
                'amdt_type': [],
                'amdt_date': [],
                'amdt_sponsor_bioguideID': [],
                'amdt_cosponsor_bioguideID': [],
                'amdt_vote': [],
                'amended_amdt': [],
                'policy_areas': [],
                'action_text': [],
                'action_date': [],
                'action_time': [],
                'action_type': []
            }
            for event, elem in ET.iterparse(hconres_data):
                if elem.tag == 'billNumber':
                    try:
                        data['num'].append(elem.text)
                        elem.clear()
                    except AttributeError as e:
                        print('%s: %s' % ('hconres-number', e))
                        continue
                if elem.tag == 'title':
                    try:
                        data['title'].append(elem.text)
                        elem.clear()
                    except AttributeError as e:
                        print('%s: %s' % ('hconres-title', e))
                        continue
                if elem.tag == 'billType':
                    try:
                        data['type'].append(elem.text)
                        elem.clear()
                    except AttributeError as e:
                        print('%s: %s' % ('hconres-type', e))
                        continue
                if elem.tag == 'sponsors' or elem.tag == 'bioguideID':
                    if elem.tag == 'bioguideID':
                        try:
                            data['sponsor_bioguideID'].append(elem.text)
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('sponsor-bioguideID', e))
                            continue
                if elem.tag == 'cosponsors' or elem.tag == 'bioguideID':
                    if elem.tag == 'bioguideID':
                        try:
                            data['cosponsor_bioguideID'].append(elem.text)
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('cosponsor-bioguideID', e))
                            continue
                if elem.tag == 'committeeReports' or elem.tag == 'committeeReport' or elem.tag == 'citation':
                    if elem.tag == 'citation':
                        try:
                            data['cmte_reports'].append(elem.text)
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('cmte-reports', e))
                            continue
            try:
                db.test.update_one(data, {'$set': {'_id': data['_id'], 'num': data['num'], 'title': data['title'], 'type': data['type'], 'sponsor_bioguideID': data['sponsor_bioguideID'], 'cosponsor_bioguideID': data['cosponsor_bioguideID'], 'cmte_reports': data['cmte_reports']}}, upsert=True)
            except pymongo.errors.ConnectionFailure as e:
                print(e)
        with open(x, 'r', encoding='utf8') as hconres_data:
            #  COMMITTEES MONGO DOCUMENT
            filename = x.strip('.xml')
            data = {
                '_id': filename,
                'summary_action': [],
                'summary_action_date': [],
                'summary_text': []
            }
            for event, elem in ET.iterparse(hconres_data):
                if elem.tag == 'summaries' or elem.tag == 'billSummaries' or elem.tag == 'item' or elem.tag == 'actionDesc':
                    if elem.tag == 'actionDesc':
                        try:
                            data['summary_action'].append(elem.text)
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('summary-action', e))
                            continue
                if elem.tag == 'summaries' or elem.tag == 'billSummaries' or elem.tag == 'item' or elem.tag == 'actionDate':
                    if elem.tag == 'actionDate':
                        try:
                            data['summary_action_date'].append(elem.text)
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('summary-action-date', e))
                            continue
                if elem.tag == 'summaries' or elem.tag == 'billSummaries' or elem.tag == 'item' or elem.tag == 'text':
                    if elem.tag == 'text':
                        try:
                            data['summary_text'].append(''.join(elem.text.replace('&quot;', '"').replace('<![CDATA[', '').replace('<p>', '').replace('</p>', '').replace(']]', '')))
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('summary-text', e))
                            continue
            try:
                db.test.update_one(data, {'$set': {'_id': data['_id']}}, upsert=True)
            except pymongo.errors.ConnectionFailure as e:
                print(e)
        with open(x, 'r', encoding='utf8') as hconres_data:
            #  COMMITTEES MONGO DOCUMENT
            filename = x.strip('.xml')
            data = {
                '_id': filename,
                'cmte_name': [],
                'cmte_chamber': [],
                'cmte_type': [],
                'cmte_action': [],
                'cmte_action_date': [],
                'subcmte_name': [],
                'subcmte_chamber': [],
                'subcmte_type': [],
                'subcmte_action': [],
                'subcmte_action_date': []
            }
            for event, elem in ET.iterparse(hconres_data):
                if elem.tag == 'committees' or elem.tag == 'billCommittees' or elem.tag == 'item' or elem.tag == 'name':
                    if elem.tag == 'name':
                        try:
                            data['cmte_name'].append(elem.text)
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('cmte-name', e))
                            continue
                if elem.tag == 'committees' or elem.tag == 'billCommittees' or elem.tag == 'item' or elem.tag == 'chamber':
                    if elem.tag == 'chamber':
                        try:
                            data['chamber'].append(elem.text)
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('cmte-chamber', e))
                            continue
                if elem.tag == 'committees' or elem.tag == 'billCommittees' or elem.tag == 'item' or elem.tag == 'type':
                    if elem.tag == 'type':
                        try:
                            data['cmte_type'].append(elem.text)
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('cmte-type', e))
                            continue
                if elem.tag == 'committees' or elem.tag == 'billCommittees' or elem.tag == 'item' or elem.tag == 'activities' or elem.tag == 'name':
                    if elem.tag == 'name':
                        try:
                            data['cmte_action'].append(elem.text)
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('cmte-action', e))
                            continue
                if elem.tag == 'committees' or elem.tag == 'billCommittees' or elem.tag == 'item' or elem.tag == 'activities' or elem.tag == 'date':
                    if elem.tag == 'date':
                        try:
                            data['cmte_action_date'].append(elem.text)
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('cmte-action-date', e))
                            continue
                if elem.tag == 'committees' or elem.tag == 'billCommittees' or elem.tag == 'item' or elem.tag == 'subcommittees' or elem.tag == 'name':
                    if elem.tag == 'name':
                        try:
                            data['subcmte_name'].append(elem.text)
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('subcmte-name', e))
                            continue
                if elem.tag == 'committees' or elem.tag == 'billCommittees' or elem.tag == 'item' or elem.tag == 'subcommittees' or elem.tag == 'activities' or elem.tag == 'name':
                    if elem.tag == 'name':
                        try:
                            data['subcmte_action'].append(elem.text)
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('subcmte-action', e))
                            continue
                if elem.tag == 'committees' or elem.tag == 'billCommittees' or elem.tag == 'item' or elem.tag == 'subcommittees' or elem.tag == 'activities' or elem.tag == 'date':
                    if elem.tag == 'date':
                        try:
                            data['subcmte_action_date'].append(elem.text)
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('subcmte-action-date', e))
                            continue
            try:
                db.test.update_one(data, {'$set': {'_id': data['_id'], 'cmte_name': data['cmte_name'], 'cmte_chamber': data['cmte_chamber'], 'cmte_type': data['cmte_type'], 'cmte_action': data['cmte_action'], 'cmte_action_date': data['cmte_action_date'], 'subcmte_name': data['subcmte_name'], 'subcmte_action': data['subcmte_action'], 'subcmte_action_date': data['subcmte_action_date']}}, upsert=True)
            except pymongo.errors.ConnectionFailure as e:
                print(e)
        with open(x, 'r', encoding='utf8') as hconres_data:
            #  RECORDED VOTES MONGO DOCUMENT
            filename = x.strip('.xml')
            data = {
                '_id': filename,
                'recorded_vote_name': [],
                'recorded_vote_chamber': [],
                'recorded_vote_congress': [],
                'recorded_vote_roll_number': [],
                'recorded_vote_session': [],
                'recorded_vote_date': [],
                'recorded_vote_url': []
            }
            for event, elem in ET.iterparse(hconres_data):
                if elem.tag == 'recordedVotes' or elem.tag == 'recordedVote' or elem.tag == 'fullActionName':
                    if elem.tag == 'fullActionName':
                        try:
                            data['recorded_vote_name'].append(elem.text)
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('recorded-vote-name', e))
                            continue
                if elem.tag == 'recordedVotes' or elem.tag == 'recordedVote' or elem.tag == 'chamber':
                    if elem.tag == 'chamber':
                        try:
                            data['recorded_vote_chamber'].append(elem.text)
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('recorded-vote-chamber', e))
                            continue
                if elem.tag == 'recordedVotes' or elem.tag == 'recordedVote' or elem.tag == 'congress':
                    if elem.tag == 'congress':
                        try:
                            data['recorded_vote_congress'].append(elem.text)
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('recorded-vote-congress', e))
                            continue
                if elem.tag == 'recordedVotes' or elem.tag == 'recordedVote' or elem.tag == 'rollNumber':
                    if elem.tag == 'rollNumber':
                        try:
                            data['recorded_vote_roll_number'].append(elem.text)
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('recorded-vote-roll-number', e))
                            continue
                if elem.tag == 'recordedVotes' or elem.tag == 'recordedVote' or elem.tag == 'sessionNumber':
                    if elem.tag == 'sessionNumber':
                        try:
                            data['recorded_vote_session'].append(elem.text)
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('recorded-vote-session', e))
                            continue
                if elem.tag == 'recordedVotes' or elem.tag == 'recordedVote' or elem.tag == 'date':
                    if elem.tag == 'date':
                        try:
                            data['recorded_vote_date'].append(elem.text)
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('recorded-vote-date', e))
                            continue
                if elem.tag == 'recordedVotes' or elem.tag == 'recordedVote' or elem.tag == 'url':
                    if elem.tag == 'url':
                        try:
                            data['recorded_vote_url'].append(elem.text)
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('recorded-vote-url', e))
                            continue
            try:
                db.test.update_one(data, {'$set': {'recorded_vote_name': data['recorded_vote_name'], 'recorded_vote_chamber': data['recorded_vote_chamber'], 'recorded_vote_congress': data['recorded_vote_congress'], 'recorded_vote_roll_number': data['recorded_vote_roll_number'], 'recorded_vote_session': data['recorded_vote_session'], 'recorded_vote_date': data['recorded_vote_date'], 'recorded_vote_url': data['recorded_vote_url']}}, upsert=True)
            except pymongo.errors.ConnectionFailure as e:
                print(e)
        with open(x, 'r', encoding='utf8') as hconres_data:
            #  CBO COST ESTIMATES MONGO DOCUMENT
            filename = x.strip('.xml')
            data = {
                '_id': filename,
                'CBO_cost_estimate_title': [],
                'CBO_cost_estimate_date': [],
                'CBO_cost_estimate_url': []
            }
            for event, elem in ET.iterparse(hconres_data):
                if elem.tag == 'cboCostEstimates' or elem.tag == 'item' or elem.tag == 'title':
                    if elem.tag == 'title':
                        try:
                            data['CBO_cost_estimate_title'].append(elem.text)
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('cbo-cost-estimate-title', e))
                            continue
                    if elem.tag == 'cboCostEstimates' or elem.tag == 'item' or elem.tag == 'pubDate':
                        if elem.tag == 'pubDate':
                            try:
                                data['CBO_cost_estimate_date'].append(elem.text)
                                elem.clear()
                            except AttributeError as e:
                                print('%s: %s' % ('cbo-cost-estimate-date', e))
                                continue
                    if elem.tag == 'cboCostEstimates' or elem.tag == 'item' or elem.tag == 'url':
                        if elem.tag == 'url':
                            try:
                                data['CBO_cost_estimate_url'].append(elem.text)
                                elem.clear()
                            except AttributeError as e:
                                print('%s: %s' % ('cbo-cost-estimate-url', e))
                                continue
            try:
                db.test.update_one(data, {'$set': {'_id': data['_id'], 'CBO_cost_estimate_title': data['CBO_cost_estimate_title'], 'CBO_cost_estimate_date': data['CBO_cost_estimate_date'], 'CBO_cost_estimate_url': data['CBO_cost_estimate_url']}}, upsert=True)
            except pymongo.errors.ConnectionFailure as e:
                print(e)
        with open(x, 'r', encoding='utf8') as hconres_data:
            #  CBO RELATED BILLS MONGO DOCUMENT
            filename = x.strip('.xml')
            data = {
                '_id': filename,
                'related_bill_latest_title': [],
                'related_bill_type': [],
                'related_bill_num': [],
                'related_bill_congress': [],
                'related_bill_status': [],
                'related_bill_status_date': []
            }
            for event, elem in ET.iterparse(hconres_data):
                if elem.tag == 'relatedBills' or elem.tag == 'item' or elem.tag == 'latestTitle':
                    if elem.tag == 'latestTitle':
                        try:
                            data['related_bill_latest_title'].append(elem.text)
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('related-bill-latest-title', e))
                            continue
                if elem.tag == 'relatedBills' or elem.tag == 'item' or elem.tag == 'type':
                    if elem.tag == 'type':
                        try:
                            data['related_bill_type'].append(elem.text)
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('related-bill-type', e))
                            continue
                if elem.tag == 'relatedBills' or elem.tag == 'item' or elem.tag == 'number':
                    if elem.tag == 'number':
                        try:
                            data['related_bill_num'].append(elem.text)
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('related-bill-num', e))
                            continue
                if elem.tag == 'relatedBills' or elem.tag == 'item' or elem.tag == 'congress':
                    if elem.tag == 'congress':
                        try:
                            data['related_bill_congress'].append(elem.text)
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('related-bill-congress', e))
                            continue
                if elem.tag == 'relatedBills' or elem.tag == 'item' or elem.tag == 'latestAction' or elem.tag == 'text':
                    if elem.tag == 'text':
                        try:
                            data['related_bill_status'].append(elem.text)
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('related-bill-status', e))
                            continue
                if elem.tag == 'relatedBills' or elem.tag == 'item' or elem.tag == 'latestAction' or elem.tag == 'actionDate':
                    if elem.tag == 'actionDate':
                        try:
                            data['related_bill_status_date'].append(elem.text)
                            elem.clear()
                        except AttributeError as e:
                            print('%s: %s' % ('related-bill-status-date', e))
                            continue
            try:
                db.test.update_one(data, {'$set': {'_id': data['_id'], 'related_bill_latest_title': data['related_bill_latest_title'], 'related_bill_type': data['related_bill_type'], 'related_bill_num': data['related_bill_num'], 'related_bill_congress': data['related_bill_congress'], 'related_bill_status': data['related_bill_status'], 'related_bill_date': data['related_bill_date']}}, upsert=True)
            except pymongo.errors.ConnectionFailure as e:
                print(e)


def remove_files(file):
    for x in file:
        os.remove(x)


if __name__ == '__main__':
    hconres(sys.argv)
