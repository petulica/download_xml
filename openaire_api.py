
import calendar
import datetime
import re
import requests


def get_dates(years):
    f = '{}-{:02d}-{:02d}'
    for y in years:
        for m in range(1, 13):
            if m == 1:
                d_start = 2
            else:
                d_start = 1
            d_end = calendar.monthrange(y, m)[1]

            yield [f.format(y, m, d) for d in (d_start, d_end)]


def download_batch(date_start, date_end):
    """Params: datestamps in format eg. '2014-01-31'
    """
    URL = 'http://api.openaire.eu/search/publications'
    PAGE_SIZE = 100
    NAME = '{}_{:02d}.xml'

    params = {
        'hasProject': 'true',
        'fromDateAccepted': date_start,
        'toDateAccepted': date_end,
        'page': 1,
        'size': PAGE_SIZE
    }
    resp = requests.get(URL, params=params)
    resp.raise_for_status()
    with open(NAME.format(date_start, 1), 'w', encoding='utf-8') as fh:
        fh.write(resp.text)
    count = re.search('<total>(\d*)', resp.text).group(1)
    count = int(count)
    pages, plus = divmod(count, PAGE_SIZE)
    if plus:
        pages += 1
    print(f'Downloading pages for month {date_start[:7]} ({pages} in total)')
    for p in range(2, pages+1):
        params['page'] = p
        resp = requests.get(URL, params=params)
        resp.raise_for_status()
        with open(NAME.format(date_start, p), 'w', encoding='utf-8') as fh:
            fh.write(resp.text)
        print (p)


if __name__ == "__main__":

    YEARS = range(2014, 2019)
    for item in get_dates(YEARS):
        download_batch(*item)
