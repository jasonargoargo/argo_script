import xml.etree.ElementTree as ET
import sys
import os
import glob
import time
import csv


def main(anything):
    number = []
    text = []
    hconres_xmls = glob.glob('hconres*.xml')
    for x in hconres_xmls:
        with open(x, 'r', encoding='utf8') as hconres_file:
            for event, elem in ET.iterparse(hconres_file):
                if elem.tag == 'legis-num' or elem.tag == 'form':
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
                elif elem.tag == 'resolution-body':
                    if elem.text is not None and elem.tail is not None:  # does not get all True values
                        try:
                            text.append(elem.text)
                            text.append(elem.tail)
                        except AttributeError as e:
                            print('%s: %s' % ('hconres-text-session', e))
                            continue
    remove_files(hconres_xmls)
    csv_file(number, text)


def remove_files(file):
    for x in file:
        os.remove(x)


def csv_file(number, text):
    title = 'BILLS' + time.strftime('%Y%m%d') + '.csv'
    with open(title, 'a', newline='') as csvfile:
        try:
            writer = csv.writer(csvfile)
            writer.writerows(zip(number, text))
        except Exception as e:
            print(e)
        finally:
            number = []
            text = []


if __name__ == '__main__':
    main(sys.argv)
