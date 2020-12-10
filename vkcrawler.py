# /search?c[section]=people&c[group]=127149194&c[name]=1&c[country]=0&c[sex]=1&c[age_from]=19&c[age_to]=21&c[status]=0&offset=30

import requests
from bs4 import BeautifulSoup
from config import REMIXSID, USER_AGENT, ACCESS_TOKEN
import re
from time import sleep
import json


def get_users_id_from_group(group_id=127149194, age_from=19, age_to=21, amount=200) -> list:
    """
    Чтобы узнать возраст даже тех девушек, у кого он скрыт (а скрыт почти у всех), пришлось сделать пока что так;
    Метод сугубо научного тыка показал, что кука remixsid - та самая, которая проверяется при выдаче пользователей;
    Джоуни, прости меня за эту ебанину, но она работает)
    P.S. можно потом с палкой и вайршарком расковырять какие запросы уходят с пролижения мобилы, там то точно REST и красиво.
    """
    offset = 0
    users_id = []

    while offset <= amount:
        url = f'https://m.vk.com/search?c[section]=people&c[group]={group_id}&c[name]=1&c[country]=0&c[sex]=1&c[age_from]={age_from}&c[age_to]={age_to}&c[status]=0&offset={offset}'
        res = requests.get(url, cookies=REMIXSID)
        soup = BeautifulSoup (res.text, "lxml")
        users_data_raw = soup.find_all("a", class_="simple_fit_item search_item")

        for user in users_data_raw:
            users_id.append(user["href"][1:])

        offset += 30
    
    return users_id


def get_instagram_links(users_id: list) -> list:
    """
    Просто вариант сбора инстаграмов без vk api.
    """
    instagram_usernames = []

    for user in users_id:
        url = f'https://m.vk.com/{user}'
        res = requests.get(url, headers=USER_AGENT, cookies=REMIXSID)
        soup = BeautifulSoup (res.text, "lxml")
        # Хз почему, но там у вк http в ссылке, на всякий случай регулярку оставил для метода тоже.
        username = soup.find('a', href=re.compile(".*://instagram.com/*"))

        if username:
            instagram_usernames.append(username.text)

        sleep(2)

    return instagram_usernames


def get_instagram_links_vk_api(usernames: list) -> list:
    users_string = ''
    for user in usernames:
        users_string += user + ','

    api_uri = f'https://api.vk.com/method/users.get?user_ids={users_string}&fields=connections&v=5.52&access_token={ACCESS_TOKEN}'
    users_data = requests.get(api_uri).text
    users_data_parsed = json.loads(users_data)

    instagram_links = []
    for user in users_data_parsed["response"]:
        try:
            instagram_links.append(user["instagram"])
        except KeyError:
            pass
    
    return instagram_links
