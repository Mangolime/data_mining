# Используем API сайта last.fm, чтобы получить список наиболее популярных исполнителей указанной страны.

import requests

country = 'spain'
api_key = '4bf15e35d1414d0f9ba2924355836ec8'

main_link = 'http://ws.audioscrobbler.com/2.0'

params = {
    'method': 'geo.gettopartists',
    'country': country,
    'api_key': api_key,
    'format': 'json'
}

response = requests.get(main_link, params=params)
if response.ok:
    topArtists = response.json()
    with open('artists.txt', 'w', encoding='UTF-8') as file:
        for artist in topArtists['topartists']['artist']:
            print(artist['name'])
            file.write(artist['name'] + '\n')
else:
    print('Status error')
