

# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import requests
from bs4 import BeautifulSoup


# retona os titulos das tabelas
def extract_titles(query):
    headers = {"User-Agent": "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 ("
                         "KHTML, like Gecko) Version/4.0 Safari/534.30"}
    page = requests.get(query, headers = headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    list_name = soup.find('div', {'class': 'toc', 'id': 'toc'}).find_all('span', {'class': 'toctext'})
    titles = [item.getText() for item in list_name]
    return titles

# retorna informacoes de filmes/series/programas dos actores
def extract_actor_info(actor):
    try:
        
        actor_name_query = actor.replace(' ', '_')
        query = f'https://en.wikipedia.org/wiki/{actor_name_query}_filmography'
        actor_tables = pd.read_html(query)
        table_titles = extract_titles(query)
        title_counter = 0
        
        for table in actor_tables:
            
            if table.shape[0] > 5:
        
                os.makedirs(f'actors_info/{actor}', exist_ok = True)
                table.to_csv(f'actors_info/{actor}/{actor}_{table_titles[title_counter]}.csv')
                title_counter +=1
                
        txt = open(f'actors_info/{actor}/{actor}_movies_link.txt', 'w')
        txt.write(query)
        txt.close()
        print(f"{actor} extraído com sucesso!\n ")
        
    except Exception as e:
        
        print(f"Nao foi possível achar o autor {actor}")
        print(e)
        
def main():
    actors_csv = pd.read_csv('actors.csv')
    actors = actors_csv.Actor.unique()
    print("Extraindo informações")
    for actor in actors:
        extract_actor_info(actor)
    
if __name__ == "__main__":
    main()