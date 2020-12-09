# /search?c[section]=people&c[group]=127149194&c[name]=1&c[country]=0&c[sex]=1&c[age_from]=19&c[age_to]=21&c[status]=0&offset=30

import requests
from bs4 import BeautifulSoup
from config import REMIXSID


def get_users_id_from_group(group_id=127149194, age_from=19, age_to=21, amount=200) -> list:
    """
    Чтобы узнать возраст даже тех тян, у кого он скрыт (а скрыт почти у всех), пришлось сделать пока что так;
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
            print("added: ", user["href"][1:])

        offset += 30
    
    return users_id


def get_instagram_links(users_id: list) -> list:
    pass
