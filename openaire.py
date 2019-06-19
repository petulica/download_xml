"""
Script for harvesting metadata using oai-pmh protocol within defined date range.
Made by github.com/janaslo
"""
import time
import datetime
import requests

from multiprocessing import Pool
from pathlib import Path
from xml.etree import ElementTree as ET

BASE_URL = 'https://invenio.nusl.cz/oai2d'
PREFIX = 'marcxml'
SET = 'global'
PARAMS = {'verb': 'ListRecords'}

TARGET_DIR = './download_nusl'    # nastavit si svuj!


def download_page(from_=None, until=None, token=None):
    """Using given parameters download page contents, save into file and return token."""
    if token:
        params = {'resumptionToken': token}
    else:
        params = {
            'set': SET,
            'metadataPrefix': PREFIX,
            'from': from_,
            'until': until
        }
    params.update(PARAMS)
    # print('PARAMS', params)
    # If page returns undesired return code, try again in 5 sec.
    
    while not requests.get(BASE_URL, params=params).ok:
        print(page.status_code)
        print(page.text)
        print('='*50)
        print("Retrying in 5 seconds...")
        time.sleep(5)

    page = requests.get(BASE_URL, params=params)
    if 'noRecordsMatch' in page.text:
        print ('NO RECORDS', from_, until)
        return
    xml = ET.fromstring(page.text)
    token = xml.find('.//{http://www.openarchives.org/OAI/2.0/}resumptionToken')
    token_text, cursor = None, None
    if token is not None:
        token_text = token.text
        cursor = token.attrib.get('cursor', 'LAST')
    filename = f'{from_}_{until}_{cursor}.xml'
    with open(Path(TARGET_DIR, filename), 'w') as f:
        f.write(page.text)
    print('SAVED', filename)
    return token_text


def download_batch(from_, until):
    """Batch management for download_page()."""
    params = {'from_': from_, 'until': until}
    token = download_page(**params)
    while token:
        params.update(token=token)
        token = download_page(**params)



def prepare_dates(date_beg, date_end, days=3):
    """Split specified date range into time periods and return as list."""
    d_format = '%Y-%m-%d'
    date_beg, date_end = [datetime.datetime.strptime(d, d_format) for d in (date_beg, date_end)]
    dates = []
    while date_beg <= date_end:
        dates.append(date_beg.strftime(d_format)+'T00:00:00Z')
        date_beg += datetime.timedelta(days)
    ranges = []
    for i in range(len(dates)-1):
        ranges.append((dates[i], dates[i+1]))
    return ranges


if __name__ == "__main__":
    """Prepare date ranges, start batches."""
    dates = prepare_dates('2014-01-01', '2019-06-01')
    print(dates)
    pool = Pool(6, maxtasksperchild=3)
    for dr in dates:
        pool.apply_async(download_batch, args=dr)

    pool.close()
    pool.join()

