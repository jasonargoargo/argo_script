import zipfile
import urllib.request as req
from lxml import etree
import io
import sys
import csv


FILENAME = ('BILLS-115-2-hconres.zip')


def retrieve_urls(filename):
    try:
        data = req.urlretrieve(
            # these urls refer only to "Congressional Bills" "115th" "2nd"
            'https://www.govinfo.gov/bulkdata/BILLS/115/2/hconres/BILLS-115-2-hconres.zip',
            filename=filename)
    except req.URLError as e:
        raise  # flags any URLError errors to user upstream


def read_xml(xml_document):
    # these variables refer only to "Congressional Bills" "115th" "2nd"
    # r = xml_document.xpath('//text()')
    # legis_num = r.xml_document.xpath('//legis-num').text
    # purpose = r.xml_document.xpath('//official-title').text
    # full_text = r.xml.document.xpath('')
    # push_to_db(legis_num, purpose)
    return


# def push_to_db(legis_num, purpose, full_text):
    # success = bool
    # if success:
    # return 1
    # else:
    # return 0


def main(anything_i_pass_to_this_program):
    # with open(anything_i_pass_to_this_program[1], 'r') as f:
        # for line in f:
            # print("links to download: ", line)
    with zipfile.ZipFile(FILENAME, 'r') as my_zip_file:
        print(my_zip_file.namelist())
        # for i, xml_file in enumerate(my_zip_file.namelist()):
        #    dd = io.TextIOWrapper(my_zip_file.open(xml_file))
        #    print(i)
        #    file = dd.read()
        #    print(type(file))
        #    xml_document = etree.fromstring(file)
        #    read_xml(xml_document)
        #    print(type(xml_document))
    # print(anything_i_pass_to_this_program)


# if __name__ == "__main__":
    # main(sys.argv)
retrieve_urls(FILENAME)
