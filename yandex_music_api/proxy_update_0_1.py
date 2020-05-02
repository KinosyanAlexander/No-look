#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  proxy_update.py
#  
#  Copyright 2020 kinos <kinos@DESKTOP-7650S1U>
import schedule
from lxml import html
import re
import json
import time
import requests
from pprint import pprint


def clean_proxies(filename):
    r = time.time()
    data = open(filename, encoding='utf-8').read().split()
    print(data)
    clean_data = []
    for i in data:
        proxy = 'https://' + i
        try:
            req = requests.get('https://api.music.yandex.net',
                               timeout=10,
                               proxies={'https': proxy})
        except Exception as e:
            print(999)
            print(e.__class__.__name__, proxy)
        else:
            print('add')
            clean_data.append(i)
    print('len2', len(clean_data))
    with open(filename, 'w', encoding='utf-8') as f:
        for i in clean_data:
            print(i, file=f)
    print(time.time() - r)


'''
def get_proxies():
    url = 'https://proxygather.com/proxylist/country?c=Russia'
    
    ports_dict = {
                  '1F90': '8080',
                  '50': '80',
                  'C38': '3128'
                  }
    #print(1)
    asr = time.time()
    req = requests.get(url, timeout=1)
    #print(2)
    print(time.time() - asr)
    
    tree = html.fromstring(req.text)
    xpath = tree.xpath('//script[@type="text/javascript"]')
    xpath = map(lambda x: x.text_content(), xpath)
    xpath = filter(lambda x: re.findall('gp\.insertPrx', x), xpath)
    xpath = map(lambda x: re.sub('gp\.insertPrx\(', '', x), xpath)
    xpath = map(lambda x: re.sub('}.+', '}', x), xpath)
    xpath = map(lambda x: re.sub('[\n\r\t]', '', x).strip(), xpath)
    proxies = map(lambda x: json.loads(x), xpath)    #pprint.pprint(proxies)
    proxies = filter(lambda x: int(x['PROXY_TIME']) < 400, proxies)
    #pprint.pprint(list(proxies))
    proxies = filter(lambda x: x['PROXY_PORT'] in ports_dict.keys(), proxies)
    proxy_ip = list(map(lambda x: x['PROXY_IP'] + ':' + ports_dict[x['PROXY_PORT']], proxies))
    
    with open('proxies.txt', 'w', encoding='utf-8') as f:
        for i in proxy_ip:
            print(i, file=f)
    
    print('len1', len(proxy_ip))
    #clean_proxies('proxies.txt')
    
    return proxy_ip
'''


def get_proxies():
    
    dict_port = {
    '(Zero9EightZero^ThreeSixOne)': '8',
    '(Zero2ThreeOne^Three2Zero)': '1',
    '(Two1ZeroTwo^Two9Nine)': '0',
    '(EightOneNineSix^Two3Four)': '9',
    '(EightTwoFourNine^Eight8Five)': '4',
    '(Six8SevenFive^Four8Eight)': '3',
    '(Five5SixThree^Two1Seven)': '2',
    '(ZeroZeroTwoEight^TwoFourSix)': '6',
    '(Three1FiveSeven^FourFourThree)': '5',
    '(Zero0OneFour^Eight6Two)': '7'
    }

    print(1)
    req = requests.post('http://spys.one/proxys/RU/', data={'xpp': 3, 'xf5': 2}, headers={'Content-Type': 'text/plain'}, proxies={'https': 'socks4://185.26.219.34:61640'})
    print(2)
    #pprint(req.text)

    tree = html.fromstring(req.text)
    xpath = tree.xpath('//td[1]/font[@class="spy14"]')
    xpath = map(lambda x: x.text_content(), xpath)
    xpath = map(lambda x: x.split('document.write("<font class=spy2>:<\/font>"+'), xpath)
    #pprint(xpath)
    k = set()
    for i in xpath:
        t = i[1][:-1].split('+')
        for y in t:
            k.add(y)
    pprint(k)
    print(len(k))
#        except KeyError:
#            pprint(i[1][:-1].split('+'))
    #xpath = map(lambda x: [x[0], ''.join(list(map(lambda x: dict_port[x], x[1].split('+'))))], xpath)
    socks = map(lambda x: 'socks5://' + ':'.join(x), xpath)
    
    return list(socks)

#print(get_proxies())
    

get_proxies()

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
browser = webdriver.Chrome()
browser.set_page_load_timeout(30)
try:
    browser.get('https://yandex.ru')
except TimeoutException:
    print("can't load page")
browser.quit()


'''
p_element = driver.find_element_by_id(id_='intro-text')
print(p_element.text)
'''
# result:
'Yay! Supports javascript'

#get_proxies()
'''
clean_proxies('proxies.txt')




get_proxies()
'''
schedule.every(1).minutes.do(get_proxies)

while True:
    schedule.run_pending()

if __name__ == '__main__':
    get_proxies()
    with open('proxies.txt', encoding='utf-8') as f:
        print(f.read())
