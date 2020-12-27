import requests
import json
from time import sleep


class InstaClient:

    def __init__(self, sessionid, token, user_agent):
        self.sessionid = sessionid
        self.token = token
        self.url = 'https://instagram.com'
        self.headers = token.update(user_agent)

    def _get_user_id(self, username: str) -> str:
        uri = f'{self.url}/web/search/topsearch/?context=blended&query={username}'
        user_data_raw = requests.get(uri, headers=self.headers, cookies=self.sessionid).text
        user_data_json = json.loads(user_data_raw)
        
        try:
            user_id = user_data_json["users"][0]["user"]["pk"]
        except IndexError:
            return ''
        
        return user_id

    def _get_posts_id(self, username: str) -> list:
        user_id = self._get_user_id(username)
        uri = f'{self.url}/graphql/query/?query_hash=003056d32c2554def87228bc3fd9668a&variables={{"id":"{user_id}","first":12}}'
        posts_data_raw = requests.get(uri, headers=self.headers, cookies=self.sessionid).text
        posts_data_json = json.loads(posts_data_raw)
        try:
            posts_data_parsed = posts_data_json["data"]["user"]["edge_owner_to_timeline_media"]["edges"]
        except IndexError:
            return []

        posts_id = []
        for post in posts_data_parsed:
            posts_id.append(post["node"]["id"])
        
        return posts_id

    def like_posts(self, usernames: list, posts_to_like: int, step: int):
        """
        Requires list of instagram users;
        Number of posts to like for each user;
        Step between posts at user acc.
        """
        for username in usernames:
            posts_id = self._get_posts_id(username)

            for post in posts_id[::step][:posts_to_like]:
                uri = f'{self.url}/web/likes/{post}/like/'
                requests.post(uri, headers=self.headers, cookies=self.sessionid)
                sleep(2)
            
            sleep(5)
