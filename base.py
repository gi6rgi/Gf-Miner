# reverse za 300
# /web/likes/{тут айдишник какой-то хз}/like/
# User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0
# ["data"]["user"]["edge_owner_to_timeline_media"]["edges"]

import requests
import json
from time import sleep


class InstaClient:

    def __init__(self, sessionid, CSRF, user_agent):
        self.sessionid = sessionid
        self.CSRF = CSRF
        self.user_agent = user_agent

    def _get_user_id(self, username: str) -> str:
        # I'm about to find better way to get this id.
        url = f'http://instagram.com/{username}'
        r = requests.get(url, headers=self.user_agent, cookies=self.sessionid).text

        try:
            result = r.split('profilePage_')[1]
        except IndexError:
            return "Wrong username"
        user_id = result.split('"')[0]

        return user_id

    def _get_posts_id(self, username: str) -> list:
        user_id = self._get_user_id(username)
        url = f'https://www.instagram.com/graphql/query/?query_hash=003056d32c2554def87228bc3fd9668a&variables={{"id":"{user_id}","first":12,"after":""}}'
        posts_id_raw_data = requests.get(url).text
        posts_id_json = json.loads(posts_id_raw_data)
        try:
            posts_id_data = posts_id_json["data"]["user"]["edge_owner_to_timeline_media"]["edges"]
        except TypeError:
            return None

        posts_id = []
        for post in posts_id_data:
            posts_id.append(post["node"]["id"])

        return posts_id

    def like_posts(self, usernames: list, posts_to_like: int, step: int):
        """
        Requires a list of Insta users;
        posts_to_like - amount of posts to like;
        step - likes interval.
        """
        for username in usernames:
            posts_id = self._get_posts_id(username)

            if posts_id:
                for post in posts_id[::step][:posts_to_like]:
                    url = f'https://instagram.com/web/likes/{post}/like/'
                    requests.post(url, headers=self.CSRF, cookies=self.sessionid)
