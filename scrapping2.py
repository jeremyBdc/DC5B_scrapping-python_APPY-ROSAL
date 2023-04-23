import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL du site web
url = "https://www.scrapethissite.com/pages/forms/"

def process_row(row):
    def get_value(id_class, type_=None):
        id = row.find('td', class_=id_class)
        if id:
            value = id.text.strip()
            if type_ == 'int':
                return int(value)
            elif type_ == 'float':
                return float(value.strip('%')) / 100
            return value
        return None

    return {
        'Year': get_value('year', 'int') if get_value('year') else None,
        'Team Name': get_value('name').replace('\n', '').replace('\t', '').replace('\r', ''),
        'Wins': get_value('wins', 'int'),
        'Losses': get_value('losses', 'int'),
        'Win %': get_value('percent', 'float') if get_value('percent') else None,
        'Goals For (GF)': get_value('gf', 'int'),
        'Goals Against (GA)': get_value('ga', 'int'),
    }

# Récupérer les données de chaque page
data = []
for i in range(1, 11):
    page_url = f"{url}?page={i}"
    rqst = requests.get(page_url)
    soup = BeautifulSoup(rqst.content, 'html.parser')

    for row in soup.find_all('tr', class_='team'):
        processed_row = process_row(row)
        goals_difference = processed_row['Goals For (GF)'] - processed_row['Goals Against (GA)']

        if goals_difference > 0 and processed_row['Goals Against (GA)'] < 300:
            processed_row['+ / -'] = goals_difference
            data.append(processed_row)

# Tri et création du fichier CSV
dataframe = pd.DataFrame(data)
dataframe_ = dataframe.sort_values(by='+ / -', ascending=True)
dataframe_.to_csv('hockeyteam.csv', index=False, encoding='utf-8-sig')