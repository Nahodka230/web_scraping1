import requests
import bs4
import fake_headers
import json


headers = fake_headers.Headers(browser = 'firefox', os = 'win')
headers_dict = headers.generate()
response = requests.get('https://spb.hh.ru/search/vacancy?text=python+Django+Flask&salary=&ored_clusters=true&area=2&area=1',headers = headers_dict)
main_html_data = response.text
main_html = bs4.BeautifulSoup(main_html_data,'lxml')
vacancy_tags = main_html.find_all('div', class_= "vacancy-serp-item__layout")
hh_data = {}
filename = "hh.json"
with open(filename, "w", encoding = "utf-8") as file:
    for vacancy_tag in vacancy_tags:
        hh_data["name_vacancy"] = vacancy_tag.find('a', class_= "serp-item__title").get_text()
        hh_data["link"] = vacancy_tag.find('a', class_ = "serp-item__title").get('href')
        if vacancy_tag.find('span', class_ = "bloko-header-section-2") is not None:
            hh_data["salary"] = vacancy_tag.find('span', class_ = "bloko-header-section-2").get_text()
        hh_data["company"] = vacancy_tag.find('a', class_ = "bloko-link bloko-link_kind-tertiary").get_text()
        hh_data["city"] = list(vacancy_tag.find(class_="vacancy-serp-item__info").children)[1].text
        json.dump(hh_data, file, ensure_ascii=False,  indent=4)
