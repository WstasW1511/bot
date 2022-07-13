import requests
from bs4 import BeautifulSoup
import time

news = []
links = []
number = 1


def start(number):
    url = 'https://tengrinews.kz/'
    response = requests.get(url)
    print(response.status_code)
    time.sleep(1)
    soup = BeautifulSoup(response.text, 'lxml')
    all = soup.find_all('a', class_='tn-tape-title')
    print(len(all))
    for i in all:
        news.append(str(number) + "-" + i.text)
        link = i.get('href')
        if link.startswith('https:'):
            pass
        else:
            link = "https://tengrinews.kz"+link
        links.append(link)
        number += 1
