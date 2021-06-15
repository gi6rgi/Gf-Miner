from vkcrawler import VkCrawler
from instaclient import InstaClient


crawler = VkCrawler(
    {'remixsid': ''},
    ''    
)
liker = InstaClient(
    {'sessionid': ''},
    {
        'X-CSRFToken': '',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'
    }
)

vkusers = crawler.get_users_id_from_group('', '18', '22', 1000)
instlinks = crawler.get_instagram_links_vk_api(vkusers)
liker.like_posts(instlinks, 2, 2)
