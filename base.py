# reverse za 300
# /web/likes/{тут айдишник какой-то хз}/like/
# User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0
# ["config"]["ProfilePage"]["user"]["edge_owner_to_timeline_media"]

import requests
import json
# for tests
from config import SESSIONID, CSRF


class Base:

    def __init__(self, sessionid, CSRF):
        self.sessionid = sessionid
        self.CSRF = CSRF

    def _get_posts_id(self, username: str) -> list:
        res = requests.get(f'https://instagram.com/{username}', cookies=self.sessionid).text
        raw_user_data = res.split('<script type="text/javascript">')[-4].split(';</script>')[0].split('window._sharedData = ')[-1]
        json_user_data = json.loads(raw_user_data)
        posts_id_data = json_user_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]

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
