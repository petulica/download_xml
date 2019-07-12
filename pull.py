import requests

request_base = 'http://api.openaire.eu/search/publications?'
params = ['hasProject=true', 'fromDateAccepted=2014-02-01', 'toDateAccepted=2014-02-28', 'size=1000']
page = 1

while True:
    request = request_base + "&".join(params) + "&page=" + str(page)
    page = page + 1
    print("Harvesting " + request)
    content = requests.get(request)
    if 'noRecordsMatch' in content.text:
        print ('NO more RECORDS')
        break
    with open("openaire_unor14_" + str(page) + ".xml", mode="a", encoding='utf-8') as file:
        print("Writing into file")
        file.write(content.text)
