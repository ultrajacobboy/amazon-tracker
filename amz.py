from bs4 import BeautifulSoup
import requests
import sys
from fake_useragent import UserAgent
from os.path import abspath, dirname
import json
import time
import var
from proxy import Proxy
import random
import smtplib

script = dirname(abspath(__file__))
proxy_var = Proxy()

class Amazon:
    def __init__(self):
        pass

    def notify(self, item, price, discount_price):
        print(f"Your item, {item} is below or at price goal! ${price}")
        if var.DISCORD_WEBHOOK_URL is not None:
            data = {
                "content" : f"Your item, {item} is below or at price goal! ${price}",
                "username" : "AMZ Tracker"
            }

            headers = {
                "Content-Type": "application/json"
            }

            result = requests.post(var.DISCORD_WEBHOOK_URL, json=data, headers=headers)

    def get_price(self, link):
        try:
            new_id = 1
            with open(f'{script}\\data.json') as f:
                data = json.load(f)
                for key, value in data["links"].items():
                    new_id += 1
                f.close()
        except Exception as e:
            new_id = 1
            print(e)
        try:
            cleaned_link = link.split("ref")
            ua = UserAgent()

            hdr = {'User-Agent': ua.random,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'none',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive'}

            if var.PROXY_REQUEST:
                print("Checking for valid proxies. This may take up to five minutes...")
                working = proxy_var.quick()

                proxy = {"http": random.choice(working), "https": random.choice(working)}  
                result = requests.get(cleaned_link[0], headers=hdr, proxies=proxy)
            else:
                 result = requests.get(cleaned_link[0], headers=hdr)
        except:
            print("Invalid url")
            return

        try:
            soup = BeautifulSoup(result.text, 'lxml')
        except:
            print(result.text)
            print("Invalid url")
            print("Failed on scrape")
            return

        js_test = soup.find('span', id="priceblock_ourprice")

        if js_test is None:
            js_test = soup.find('span', id="priceblock_saleprice")
            if js_test is None:
                js_test = soup.find('span', id="priceblock_pospromoprice")
                if js_test is None:
                    print(result.text)
                    print("Invalid url")
                    print("Failed on price")
                    return
        print(f"Current price is {js_test.text}. What is the price goal?")
        goal = input("> ")
        js_test = js_test.text.replace("$", "")
        js_test = js_test.replace(",", "")
        """
            new_dict = {
                            cleaned_link[0]: 
                                {
                                    "price_goal": goal,
                                    "current": js_test,
                                    "id": str(new_id)
                                }
                        }
                        """
        with open(f'{script}\\data.json', "r") as f:
            data = json.load(f)
            f.close()
        with open(f'{script}\\data.json', "w") as f:
            data["links"][cleaned_link[0]] = {
                                "price_goal": goal,
                                "current": js_test,
                                "id": str(new_id)
                            }
            json.dump(data, f, ensure_ascii=False, indent=4)
            f.close()
            print("Success!")

    def run(self, inter):
        with open(f'{script}\\data.json') as f:
                data = json.load(f)
                f.close()
        ua = UserAgent()

        hdr = {'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}

        if var.PROXY_REQUEST:
            proxies = proxy_var.get_proxies()
            print("Checking for valid proxies. This may take up to five minutes...")
            working = proxy_var.test()
        
        for key, value in data["links"].items():
            if var.PROXY_REQUEST:
                proxy = {"http": random.choice(working), "https": random.choice(working)}  
                result = requests.get(key, headers=hdr, proxies=proxy)
            else:
                 result = requests.get(key, headers=hdr)
            soup = BeautifulSoup(result.text, 'lxml')
            js_test = soup.find('span', id="priceblock_ourprice")
            try:
                js_test = js_test.text.replace("$", "")
            except:
                print(result.text)
            if js_test is None:
                print("You're being ratelimited! Sleeping for 30 minutes.")
                time.sleep(1800)
            elif js_test <= data[key]["price_goal"]:
                self.notify(key, js_test)
            elif js_test >= data[key]["price_goal"]:
                print("Price is up...")
            else:
                pass

            time.sleep(inter * 60)

    def delete_price(self):
        flag = False
        sep = "_______________________________________"
        with open(f'{script}\\data.json') as f:
            data = json.load(f)
            f.close()
        for key, value in data["links"].items():
            print(f"{key}\nID: {value['id']}")
            print(sep)
        to_delete = input("Please input the ID of the item you want to delete from your list\n> ")
        for key, value in data["links"].items():
            if value["id"] == to_delete:
                del data["links"][key]
                with open(f'{script}\\data.json', "w") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                    print("Success!")
                    f.close()
                    flag = True
                break
            else:
                pass
        if not flag:
            print("Invalid ID")
        else:
            pass
       
