import requests
import re
import json
from bs4 import BeautifulSoup
from fake_headers import Headers

url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"
keywords = ['Django', 'Flask']

def get_headers():
    return Headers(browser='firefox', os='win').generate()

def get_text(url):
    response = requests.get(url, headers=get_headers()).text
    return response

def parse_page(url, keywords):
    parced_list = []
    html = get_text(url)
    soup = BeautifulSoup(html, features='lxml')
    ads = soup.find_all(class_="vacancy-serp-item__layout")
    # pprint(ads)
    for keyword in keywords:
        for ad in ads:
            pattern = f".*?{keyword}.*?"
            result = re.search(pattern, ad.text)
            if result != None:
                parced = {
                    "title": ad.find(class_="serp-item__title").text,
                    "link": ad.find("a")["href"],
                    "salary": str(ad.find(class_="vacancy-serp-item-body__main-info").find("span", {"data-qa": "vacancy-serp__vacancy-compensation"})),
                    "company": ad.find("a", {"data-qa": "vacancy-serp__vacancy-employer"}).text,
                    "city": ad.find("div", {"data-qa": "vacancy-serp__vacancy-address"}).text
                }
                parced_list.append(parced)
    return parced_list

def create_file(parced_list):
    with open('vacancies.json', 'w', encoding='utf-8') as file:
        json.dump(parced_list, file, ensure_ascii=False)

if __name__ == "__main__":
    parced_list = parse_page(url, keywords)
    create_file(parced_list)