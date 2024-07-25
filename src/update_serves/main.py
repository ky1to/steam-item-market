from interface.interface import Interface
from schemas.schemas import SItemAdd, SItemPrice, SItem
from datetime import datetime
from LxmlSoup import LxmlSoup
from termcolor import colored
import requests
import argparse
import asyncio
import random
import time
import json
import re

def html2content_arr(arr):
    aut = [] 
    for item in arr:
        aut.append(item.text())
    return aut

def search_lots(data):
    soup = LxmlSoup(data)
    orders = soup.find_all("span", class_="market_commodity_orders_header_promote")
    return html2content_arr(orders)

def search_table_lots(data):
    soup = LxmlSoup(data)
    orders = soup.find_all("td")
    return html2content_arr(orders)

def get_links(page_number: int, id_game: int):
    
    hrefs = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
        'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Prototype-Version': '1.7',
        'Connection': 'keep-alive',
        'Referer': f'https://steamcommunity.com/market/search?appid={id_game}',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }

    params = {
        'query': '',
        'start': f'{page_number-1}0',
        'count': '10',
        'search_descriptions': '0',
        'sort_column': 'popular',
        'sort_dir': 'desc',
        'appid': str(id_game),
    }

    response = requests.get('https://steamcommunity.com/market/search/render/', params=params, headers=headers)
    if response.status_code == 200:
        soup = LxmlSoup(response.text)
        links = soup.find_all('a')
        for i in range(len(links)):
            href = str(links[i].get('href'))
            href = href.replace(r"\/", "/").replace('\"', '').replace("\\", "")
            hrefs.append(href)

        return hrefs
    elif response.status_code == 429:
        print(colored(f'Error get page steam 429', 'red'))
        time.sleep(20)
        return get_links(page_number, id_game)
    else:
        print(colored(f'Error get page steam {response.status_code}', 'red'))

def get_price_data_item(path: str, item_nameid: str, id_game: int):
    try:
        headers = {
            'User-Agent': '',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8,en-US;q=0.5,en;q=0.3',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Referer': path,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'If-Modified-Since': '',
            'Referer': f'https://steamcommunity.com/market/search?appid={id_game}',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }

        params = {
            'country': 'US',
            'language': 'english',
            'currency': '1',
            'item_nameid': item_nameid,
            'two_factor': '0',
        }

        response = requests.get('https://steamcommunity.com/market/itemordershistogram', params=params, headers=headers)
        
        if response.status_code == 200:
            data = json.loads(response.text)
            return data     
        else:
            print(colored(f'Error get price steam {response.status_code}', 'red'))
            time.sleep(10)
            return get_price_data_item(path, item_nameid, id_game) 
    except:
        time.sleep(10)
        return get_price_data_item(path, item_nameid, id_game)

def get_data_html_item(path: str):
    try:
        response = requests.get(path)
        soup = LxmlSoup(response.text)

        pattern = r' <span style=\\"color: #ffdba5\\">(.*?)<\\/span>'
        disc = re.findall(pattern, response.text)
        if disc == []:
            disc = None
        else:
            disc = disc[0]
        data = {}
        data["game"] = soup.find_all('div', class_="market_listing_nav")[0].find_all("a")[0].text()
        data["item_nameid"] = re.search(r"Market_LoadOrderSpread\( (?P<item_id>\d+) \)", response.text).group("item_id")
        data["img_link"] = soup.find_all('div', class_="market_listing_largeimage")[0].find_all('img')[0].get('src').replace("/360fx360f", "")
        data["disc"] = disc
        time.sleep(3)
        return data

    except:
        print(data)
        print(colored(f'Error get html steam {response.status_code}', 'red'))
        time.sleep(10)
        return get_data_html_item(path)

async def update_base(number: int):
    for i in range(1, number):
        game_id = 252490
        hrefs = get_links(i, game_id) # this code Rust game  (252490)
        for href in hrefs:
            if len(await Interface.name_get_item(href.replace(f"https://steamcommunity.com/market/listings/{game_id}/", "").replace("%20", " ").replace("%27", "'"))) > 0:
                print(colored('Its already in the json', 'green'))
            else:
                print(colored(f"New item {href}", 'blue'))
                data_html = get_data_html_item(href)
                await Interface.add_one(SItemAdd(
                    name = href.replace(f"https://steamcommunity.com/market/listings/{game_id}/", "").replace("%20", " ").replace("%27", "'"),
                    game = data_html["game"],
                    item_nameid = data_html["item_nameid"],
                    link = href,
                    img_link = data_html["img_link"],
                    disc = data_html["disc"],
                ))
                print(colored(f"finished adding item", 'blue'))
        time.sleep(3)
        print(f"page {i}")

async def add_item_history(item_db, game_id):
    try:
        data = get_price_data_item(item_db.link, item_db.item_nameid, game_id)
        sell_data = search_lots(data["sell_order_summary"])
        buy_data = search_lots(data["buy_order_summary"])
        await Interface.add_one_history(SItemPrice(
            name = item_db.name,
            timestamp = datetime.now(),
            price_buy = round(float(buy_data[1].replace("$", "").replace(",", "")), 2),
            price_sell = round(float(sell_data[1].replace("$", "").replace(",", "")), 2),
            price_profit = round(float(float(sell_data[1].replace("$", "").replace(",", "")))*87/100 -   float(buy_data[1].replace("$", "").replace(",", "")), 2),
            sell_lots = int(sell_data[0]),
            buy_lots = int(buy_data[0]),
        ))
        print(f"{item_db.name}")
    except: 
        time.sleep(0.3)
        await add_item_history(item_db, game_id)

async def update_price():
    game_id = 252490
    while True:
        for i in range(1, 415, 1):
            data_db = await Interface.find_item("", "", i)
            for j in range(10):
                time.sleep(0.6)
                await add_item_history(SItem.from_orm(data_db[j]), game_id)

print("Start serves")
#loop.run_until_complete(update_base(415))
asyncio.run(update_price())