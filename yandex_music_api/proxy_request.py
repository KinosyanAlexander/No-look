#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  proxy_request.py
#  
#  Copyright 2020 kinos <kinos@DESKTOP-7650S1U>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import requests
import time
from yandex_music_api.proxy_update import make_proxy_list
from random import choice

def get(url, **kwargs):
    with open('yandex_music_api\\last_time_update.txt') as f:
        if time.time() - float(f.read()) >= 5 * 60:
            make_proxy_list()
    
    def get_proxies_from_list():
        with open('yandex_music_api\\proxies.txt') as f:
            all_proxies = f.read().split('\n')
        return all_proxies
    
    all_proxies = get_proxies_from_list()
    
    while True:
        try:
            proxy = choice(all_proxies)
            # print(f'socks4://{proxy}')
            
            proxies = {
                'https': f'socks4://{proxy.strip()}'
            }
            
            response = requests.get(url, proxies=proxies, timeout=1.5)
            print(url)
            break
        except Exception as e:
            print(e.__class__.__name__)
            try:
                all_proxies.remove(proxy)
            except ValueError:
                make_proxy_list()
                all_proxies = get_proxies_from_list()



    with open('yandex_music_api\\proxies.txt', 'w') as f:
        for i in all_proxies:
            print(i, file=f)
    
    return response
    
