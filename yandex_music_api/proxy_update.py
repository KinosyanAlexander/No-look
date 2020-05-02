import requests
import time

def get_proxies():
    url = 'https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=500&country=RU'
    
    resp = requests.get(url)
    
    proxies = resp.text
    proxies = list(map(lambda x: x.strip(), proxies.split('\n')))
    
    return proxies

def make_proxy_list():
    print('------------proxy_update---------------')
    proxies = get_proxies()
    
    with open('yandex_music_api\\proxies.txt', 'w') as f:
        for i in proxies:
            print(i, file=f)
    
    with open('yandex_music_api\\last_time_update.txt', 'w') as f:
        print(str(time.time()), file=f)

    print('--------------------proxy_update_end------------------------------')

