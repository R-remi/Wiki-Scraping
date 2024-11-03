import requests
from bs4 import BeautifulSoup
import json
import os

# lire premiere de stack_de_wish.json
def read_json():
    with open('stack_de_wish.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# concater les liens entre url et stack_de_wish.json
url = 'https://fr.wikipedia.org'
def concat_links():
    json_data = read_json()
    if json_data:
        concatenated_link = url + json_data[0]
        return [concatenated_link]
    else:
        print("La liste JSON est vide.")
        return []

def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Requête réussie pour {url}")
        add_to_json_visited(url)
        erase_first()
        return response.content
    else:
        print(f"Erreur  sur l'url {url} lors de la requête: {response.status_code}")
        return None

def add_to_json(liens):
    json_data = read_json()
    json_data.extend(liens)
    with open('stack_de_wish.json', 'w') as f:
        json.dump(json_data, f)

def add_to_json_visited(lien):
    file_path = 'stack_de_wish_visited.json'
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
    else:
        json_data = []

    json_data.append(lien)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4)

def erase_first():
    json_data = read_json()
    if json_data:
        json_data.pop(0)
        with open('stack_de_wish.json', 'w') as f:
            json.dump(json_data, f)
    else:
        print("La liste JSON est vide.")

def main():
    # Récupère le contenu HTML
    links = concat_links()
    if links:
        html = get_html(links[0])
    else:
        html = None

    if html:
        # Analyse le contenu HTML
        soup = BeautifulSoup(html, 'html.parser')
        # Trouve tous les éléments <a> et récupère les attributs 'href'
        liens = [a['href'] for a in soup.find_all('a', href=True)]
        # on suprimme les liens qui ne sont pas des articles wikipedia
        liens = [lien for lien in liens if lien.startswith('/wiki/')]
        # on stocke les liens dans un fichier json
        add_to_json(liens)

for i in range(25):
    main()