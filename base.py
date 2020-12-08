# reverse za 300
# /web/likes/{тут айдишник какой-то хз}/like/
# User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0
# ["data"]["user"]["edge_owner_to_timeline_media"]["edges"]

import requests
import json
# for tests
from config import SESSIONID, CSRF


class Base:

    def __init__(self, sessionid, CSRF):
        self.sessionid = sessionid
        self.CSRF = CSRF

    def _get_user_id(self, username: str) -> str:
        pass

    def _get_posts_id(self, username: str) -> list:
        user_id = self._get_user_id(username)
        url = f'https://www.instagram.com/graphql/query/?query_hash=003056d32c2554def87228bc3fd9668a&variables={{"id":"{user_id}","first":12,"after":""}}'
        posts_id_raw_data = requests.get(url).text
        posts_id_json = json.loads(posts_id_raw_data)
        posts_id_data = posts_id_json["data"]["user"]["edge_owner_to_timeline_media"]["edges"]
    
        posts_id = []
        for post in posts_id_data:
            posts_id.append(post["node"]["id"])

        return posts_id

    def like_posts(self, usernames: list, posts_to_like: int, step: int):
        for username in usernames:
            posts_id = self._get_posts_id(username)

            for post in posts_id[::step][:posts_to_like]:
                url = f'https://instagram.com/web/likes/{post}/like/'
                requests.post(url, headers=self.CSRF, cookies=self.sessionid)

"""
some tests
"""
test = Base(SESSIONID, CSRF)
test.like_posts(["tihomeowrov"], 5, 1)
