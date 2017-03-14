'''
Created on Feb 25, 2017

@author: xhu
'''


import requests, json
thinkpage_base_url = "https://api.thinkpage.cn/v3/"


def query_weather(location, date_range, thinkpage_api_key, lang='zh-Hans', unit='c'):
    start, days = date_range
    try:
        int(start)
    except:
        days = 3
    return get_daily_weather(location, thinkpage_api_key, start, days, lang, unit)


def get_current_weather(location, thinkpage_api_key, lang='zh-Hans', unit='c'):
    global thinkpage_base_url
    api = "weather/now.json?key={key}&location={location}&language={language}&unit={unit}"
    url = "".join([thinkpage_base_url, api])
    url = url.format(key=thinkpage_api_key, location=location, language=lang, unit=unit)
    try:
        r = requests.get(url)
        if r.status_code != 200:
            print r.reason
            return None
        content = r.text
        return json.loads(content)

    except:
        return None
    return None


def get_daily_weather(location, thinkpage_api_key, start=0, days=1, lang='zh-Hans', unit='c'):
    global thinkpage_base_url
    api = "weather/daily.json?key={key}&location={location}&language={language}&unit={unit}&start={start}&days={days}"
    url = "".join([thinkpage_base_url, api])
    url = url.format(key=thinkpage_api_key, location=location, language=lang, unit=unit, start=start, days=days)
    try:
        r = requests.get(url)
        if r.status_code != 200:
            print r.reason
            return None
        content = r.text
        return json.loads(content)

    except:
        return None
    return None
