import scrapy
from scrapy.http import HtmlResponse
import re
import json
from urllib.parse import urlencode
from copy import deepcopy
from les8.instaparser.items import InstaparserItem
from pprint import pprint

class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']

    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'ninadze_k'
    inst_password = '#PWD_INSTAGRAM_BROWSER:10:1611954604:AQhQANy8ZuoO7NGnPlVnGelGnDCHge/pvzJQE0Fw+HFb+I41XvpkmaMeRRyLBCZGlyAN9RDnUSUHiCQxMmwSZPO7LYUdBTg2QHzF1up2hjunYgB+/7kMdrFdDliTxG8XSAraBO4tVI508vkw8DQ='
    parse_users = ['chainmaster.msk', '3x9.ru']
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    follow_hash = ['5aefa9893005572d237da5068082d8d5', '3dec7e2c57367ef3da3d987d89f9dbc8']
    f_type = ['Подписчики', 'Подписки']
    key_word = ['edge_followed_by', 'edge_follow']

    def parse(self, response:HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.user_login,
            formdata={'username': self.inst_login, 'enc_password': self.inst_password},
            headers={'X-CSRFToken': csrf_token}
        )

    def user_login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data['authenticated']:
            for i in range(2):  # Перебор двух пользователей
                for j in range(2):  # Перебор двух разделов - подпискии и подписчики:
                    yield response.follow(
                        f'/{self.parse_users[i]}',
                        callback=self.user_data_parse,
                        cb_kwargs={'username': self.parse_users[i], 'follow_hash': self.follow_hash[j], 'f_type': self.f_type[j], 'key_word': self.key_word[j]}
                )

    def user_data_parse(self, response: HtmlResponse, username, follow_hash, f_type, key_word):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'id': user_id, 'first': 12}
        url_follow = f'{self.graphql_url}query_hash={follow_hash}&{urlencode(variables)}'
        yield response.follow(
            url_follow,
            callback=self.user_follow_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'f_type': f_type,
                       'key_word': key_word,
                       'variables': deepcopy(variables)
                       }
        )

    def user_follow_parse(self, response:HtmlResponse, username, user_id, f_type, variables, key_word):
        j_data = response.json()
        pprint(j_data)
        page_info = j_data.get('data').get('user').get(key_word).get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')

            url_follow = f'{self.graphql_url}query_hash={self.follow_hash}&{urlencode(variables)}'
            yield response.follow(
                url_follow,
                callback=self.user_follow_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'f_type': f_type,
                           'key_word': key_word,
                           'variables': deepcopy(variables)}
            )

        followings = j_data.get('data').get('user').get(key_word).get('edges')
        for following in followings:
            item = InstaparserItem(
                user_id=following.get('node').get('id'),
                username=following.get('node').get('username'),
                photo_url=following.get('node').get('profile_pic_url'),
                follow_url=username,
                f_type=f_type
            )

            yield item


    # #Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')


    # # Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')