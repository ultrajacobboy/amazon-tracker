import requests
from bs4 import BeautifulSoup
import random

# https://github.com/jhnwr/rotatingproxies/blob/master/scrapeproxies.py

class Proxy:
    def __init__(self):
        pass
    #get the list of free proxies
    def get_proxies(self):
        r = requests.get('https://free-proxy-list.net/')
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('tbody')
        proxies = []
        for row in table:
            if row.find_all('td')[4].text =='elite proxy':
                proxy = ':'.join([row.find_all('td')[0].text, row.find_all('td')[1].text])
                proxies.append(proxy)
            else:
                pass
        return proxies

    def test(self):
        proxy_list = self.get_proxies()
        working = []
        for proxy in proxy_list:
            try:
                proxy = {"http": proxy, "https": proxy}
                r = requests.get("https://httpbin.org/ip", proxies=proxy, timeout=1)
                print(f"Works: {proxy}")
                working.append(proxy["http"])
            except:
                pass
        return working

    def quick(self):
        proxy_list = self.get_proxies()
        working = []
        for proxy in proxy_list:
            try:
                proxy = {"http": proxy, "https": proxy}
                r = requests.get("https://httpbin.org/ip", proxies=proxy, timeout=1)
                print(f"Works: {proxy}")
                working.append(proxy)
                return working
            except:
                pass
        return working

if __name__ == "__main__":
    this = test()
    print(this)
