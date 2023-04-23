import requests
from bs4 import BeautifulSoup

url = 'https://www.scrapethissite.com/pages/simple/'
rqst = requests.get(url)
soup = BeautifulSoup(rqst.content, 'html.parser')

pays = soup.find_all('div', {'class': 'country'})

# Récupérer les données de chaque Pays
for pays_ in pays:
    nom = pays_.find('h3').text if pays_.find('h3') is not None else ''
    population = pays_.find('span', {'class': 'country-population'}).text if pays_.find('span', {'class': 'country-population'}) is not None else ''
    capital = pays_.find('span', {'class': 'country-capital'}).text if pays_.find('span', {'class': 'country-capital'}) is not None else ''
    area = pays_.find('span', {'class': 'country-area'}).text if pays_.find('span', {'class': 'country-area'}) is not None else ''

# Nettoyer les données
    population = population.replace(',', '') if ',' in population else population
    area = area.replace(' km²', '') if ' km²' in area else area

# Afficher les données 
    print('Nom :', nom.strip())
    print('Population :', population)
    print('Capitale :', capital)
    print('Aire :', area + "km²")
    print('\n')