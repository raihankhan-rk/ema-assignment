import pandas as pd
import requests
from bs4 import BeautifulSoup

dict_df = pd.read_json('query.json')

data = []

for i in range(len(dict_df['query'])):
    print(i)
    query = dict_df['query'][i]
    search_query = query.replace(" ", "+")
    response = requests.get(f"https://www.google.com/search?q={search_query}")
    soup = BeautifulSoup(response.content, "html.parser")
    h3 = soup.findAll('h3')
    titles = []
    for _ in h3:
        div_tags = _.find('div')
        titles.append(div_tags.text)
    titles = titles[:5]
    for title in titles:
        data.append([query, title, dict_df['user'][i], dict_df['time'][i], dict_df['location'][i]])
df = pd.DataFrame(data, columns=['query', 'title', 'user', 'time', 'location'])
print(df)
        