import requests
import json
from bs4 import BeautifulSoup


class VkCrawler:

    def __init__(self, remixsid, access_token):
        self.remixsid = remixsid
        self.access_token = access_token

    def get_users_id_from_group(self, group_id: int, age_from: int, age_to: int, amount: int) -> list:
        offset = 0
        users_id = []

        while offset <= amount:
            uri = f'https://m.vk.com/search?c[age_from]={age_from}&c[age_to]={age_to}' \
                f'&c[city]=2&c[country]=1&c[group]={group_id}&c[name]=1&c[per_page]=40&c' \
                f'[photo]=1&c[section]=people&c[sex]=1&offset={offset}'

            res = requests.get(uri, cookies=self.remixsid)
            soup = BeautifulSoup(res.text, "lxml")
            users_data_raw = soup.find_all("a", class_="simple_fit_item search_item")
            for user in users_data_raw:
                users_id.append(user["href"][1:])
            
            offset += 30

        return users_id

    def _get_chunk_of_users(self, usernames: list) -> list:
        left_offset = 0
        right_offset = 100

        while right_offset <= len(usernames):
            left_offset += 100
            right_offset += 100
            yield usernames[left_offset:right_offset]

    def get_instagram_links_vk_api(self, usernames: list) -> list:
        instagram_links = []
        chunk_of_users = self._get_chunk_of_users(usernames)

        for user_vk_ids in chunk_of_users:                   
            users_string = ''
            for user_id in user_vk_ids:
                users_string += user_id + ','   

            uri = f'https://api.vk.com/method/users.get?user_ids={users_string}&fields=connections' \
                  f'&v=5.52&access_token={self.access_token}'
            users_data = requests.get(uri).text
            users_data_json = json.loads(users_data)

            for user in users_data_json["response"]:
                try:
                    instagram_links.append(user["instagram"])
                except KeyError:
                    pass
        
        return instagram_links
 