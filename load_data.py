import requests
import pandas as pd
from bs4 import BeautifulSoup
import json

api_key = "reSfKMMzJnXCzj5P_1TGJxx7kaxc4wyaJeO8dWFjSqr1l5ZoKCy1t16yp_frAjilTea-vavOKIodvRstANMOuTAvgLbNefYmZSW5mxZRxqWXEE-FueQByzJiM9JBY3Yx"
http_header = {'Authorization': 'Bearer '+api_key}
url = 'https://api.yelp.com/v3/businesses/search'

scrape_url = "https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population"
soup = BeautifulSoup(requests.get(scrape_url).text)

city_table = soup.find_all('table',class_="wikitable sortable")[0]
header = city_table.find("tr")
data_header = []
for items in header:
    try:
        data_header.append(items.get_text())
    except:
        continue

html_data = city_table.find_all("tr")[1:]
cities = []
for element in html_data:
    sub_data = []
    for sub_element in element:
        try:
            sub_data.append(sub_element.get_text())
        except:
            continue
    cities.append(sub_data[3].replace('\n',''))

all_cities_data = []
f = open('city_data.json','w')
for city in cities:
    try:
        parameter = {'location': city,'attributes':'hot_and_new','limit':1,'sort_by':'rating'}
        city_data = json.loads(requests.get(url,headers = http_header,params=parameter).text)
        all_cities_data.append(city_data)
        print(json.dumps(city_data),file=f)
    except:
        print(city, 'loading failed')
f.close()


