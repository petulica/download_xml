import requests

request_base = 'http://api.openaire.eu/search/publications?'
params = ['hasProject=true', 'fromDateAccepted=2014-01-01', 'toDateAccepted=2014-01-02', 'size=100', 'hasECFunding=false', 'sortBy=dateofcollection,descending']

page = 1

while True:
    request = request_base + "&".join(params) + "&page=" + str(page)
    page = page + 1
    print("Harvesting " + request)
    content = requests.get(request)

    with open("01_14_des_ecF" + str(page) + ".xml", mode="a", encoding='utf-8') as file:
        print("Writing into file")
        file.write(content.text)
    if page == 103:
        break
