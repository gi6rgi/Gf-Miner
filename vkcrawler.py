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
        offset = 50
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


    def get_instagram_links(self, users_id: list) -> list:
        """
        Просто вариант сбора инстаграмов без vk api.
        """
        instagram_usernames = []

        for user in users_id:
            url = f'https://m.vk.com/{user}'
            res = requests.get(url, headers=USER_AGENT, cookies=self.remixsid)
            soup = BeautifulSoup (res.text, "lxml")
            # Хз почему, но там у вк http в ссылке, на всякий случай регулярку оставил для метода тоже.
            username = soup.find('a', href=re.compile(".*://instagram.com/*"))

            if username:
                instagram_usernames.append(username.text)

            sleep(2)

        return instagram_usernames


    def get_instagram_links_vk_api(self, usernames: list) -> list:
        users_to_process = len(usernames)
        all_users_data = []

        # Временная инкостыляция.
        left_offset = -100
        right_offset = 0
        while right_offset <= users_to_process:
            print(left_offset, right_offset)
            left_offset += 100
            right_offset += 100

            users_string = ''
            for user in usernames[left_offset:right_offset]:
                users_string += user + ','

            api_uri = f'https://api.vk.com/method/users.get?user_ids={users_string}&fields=connections&v=5.52&access_token={self.access_token}'
            users_data = requests.get(api_uri).text
            users_data_parsed = json.loads(users_data)

            for user in users_data_parsed["response"]:
                try:
                    all_users_data.append(user["instagram"])
                except KeyError:
                    pass

        return all_users_data
