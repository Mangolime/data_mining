import requests
import json

main_link = 'https://api.github.com'
user = 'Mangolime'
relative_link = '/users/Mangolime/repos'
response = requests.get(main_link + '/users/' + user + '/repos')
if response.ok:
    repos = response.json()
    for repo in repos:
        print(repo['name'])
    with open('repos.json', 'w', encoding='UTF-8') as file:
        json.dump(repos, file, ensure_ascii=False)
else:
    print('Status error')
