import requests
import json
from bs4 import BeautifulSoup
import csv

csv_file = open('OnderzoekersHU.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Naam','Lectoraat', 'telefoon nummer','e-mail adres'])

baseurl = "https://www.hu.nl"
url = 'https://www.hu.nl/api/search/researchers'
json_data = {"siteUrl": "https://www.hu.nl", "page": '1'}

response = requests.post(url, json=json_data)
response_data = response.json()

pages = response_data['pagination']
lastpage_list = pages[-1]

print('The api responded with {0} pages'.format(lastpage_list))

for page in range(1, lastpage_list+1):
    json_data = {"siteUrl": "https://www.hu.nl", "page": page}
    response = requests.post(url, json=json_data)
    response_data = response.json()
    for data in response_data['results']:
        print("                                                   ")
        print("---------------------------------------------------")
        Name = data['name']
        print(Name)
        url1 = data['url']
        baseSource = requests.get(baseurl + url1).text
        baseSoup = BeautifulSoup(baseSource, 'lxml')
        links = baseSoup.find_all(class_='person-sidebar__links__item')
        Lectoraat = ""
        EMail = ""
        Telefoon = ""

        for link in links:
            label = link.find(class_='person-sidebar__links__item__title')
            if (label.text == "Lectoraat"):
                Lectoraat = link.find(class_='person-sidebar__links__item__link').text
                print('Lectoraat: {}'.format(Lectoraat))
            elif (label.text == "Email"):
                EMail = link.find(class_='person-sidebar__links__item__link').text
                print('Email: {}'.format(EMail))
            elif (label.text == "Telefoon"):
                Telefoon = link.find(class_='person-sidebar__links__item__link').text
                print('Telefoon: {}'.format(Telefoon))
        csv_writer.writerow([Name, Lectoraat, Telefoon, EMail])

csv_file.close()
