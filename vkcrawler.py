import requests
from bs4 import BeautifulSoup
import re
from time import sleep
import json


class VkCrawler:

    def __init__(self, remixsid, access_token):
        self.remixsid = remixsid
        self.access_token = access_token

    def get_users_id_from_group(self, group_id: int, age_from: int, age_to: int, amount: int) -> list:
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
            res = requests.get(url, cookies=self.remixsid)
            soup = BeautifulSoup (res.text, "lxml")
            users_data_raw = soup.find_all("a", class_="simple_fit_item search_item")

            for user in users_data_raw:
                users_id.append(user["href"][1:])

            offset += 30

        return users_id

    # For the sake of Jouny!
    def _get_chunk_of_users(self, usernames: list) -> list:
        left_offset = 0
        right_offset = 100

        while True:
            yield usernames[left_offset:right_offset]
            left_offset += 100
            right_offset += 100

    def get_instagram_links_vk_api(self, usernames: list) -> list:
        instagram_links = []
        chunk_of_users = self._get_chunk_of_users(usernames)

        for user_vk_ids in chunk_of_users:
            if not user_vk_ids:
                return instagram_links
                
            users_string = ''
            for user in user_vk_ids:
                users_string += user + ','

            api_uri = f'https://api.vk.com/method/users.get?user_ids={users_string}&fields=connections&v=5.52&access_token={self.access_token}'
            users_data = requests.get(api_uri).text
            users_data_parsed = json.loads(users_data)

            for user in users_data_parsed["response"]:
                try:
                    instagram_links.append(user["instagram"])
                except KeyError:
                    pass
