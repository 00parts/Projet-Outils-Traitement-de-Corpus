from bs4 import BeautifulSoup
import requests
import argparse
import pandas as pd

"""Crawler et scraper

Ce script crawl à partir d'une URL donnée en argument du script.
Il crawle par défaut jusqu'à une profondeur de 20, mais il est possible d'indiquer une autre valeur en second argument.
Ce script est adapté pour crawler des pages de reviews sur Allociné.
Ce script créé un fichier csv contenant les données scrapées.

Ce script utilise les bibliothèques BeautifulSoup, requests, argparse et pandas.

Ce script comporte ces deux fonctions : 

    * crawler - retourne la liste des URLs récupérées
    * scraper - retourne un DataFrame comportant deux colonnes : celle des reviews et celle des notes

"""



# "https://www.allocine.fr/film/fichefilm-227463/critiques/spectateurs/"


def crawler(target_url: str, max_crawl: int) -> list :
    """Crawl un site web à partir d'une URL donnée, et jusqu'à une certaine profondeur donnée

Parameters
----------
target_url : str
    L'url cible à partir de laquelle crawler
max_crawl: int
    La profondeur max jusqu'à laquelle crawl (par défaut 20)

Returns
-------
urls_to_visit : list
    La liste des urls qui ont été crawlées
"""
 
    # la liste contenant les urls à visiter, commençant par l'url cible

    urls_to_visit = [target_url]

    # compteur de crawls
    crawl_count = 0

    while urls_to_visit and crawl_count < max_crawl:

        # on récupère l'url à visiter de la liste
        current_url = urls_to_visit.pop()

        # on envoie une requête pour accéder au contenu de la page
        response = requests.get(current_url)
        response.raise_for_status()
        
        # on parse le code html du site
        
        soup = BeautifulSoup(response.text, "html.parser")

        # on récupère tous les liens présents sur lapage
        link_elements = soup.select("a[href]")
        for link_element in link_elements:
            url = link_element["href"]

            # si besoin on convertit les url en url absolue
            if not url.startswith("http"):
                absolute_url = requests.compat.urljoin(target_url, url)
            else:
                absolute_url = url

            # on fait en sorte que l'url commence bien par l'url cible, qu'elle n'est pas déjà présente dans la liste et qu'elle contienne "?page="
            #cette dernière condition est spécifique à mes besoins afin de ne récupérer que les pages contenant des reviews 
            if (
                absolute_url.startswith(target_url)
                and absolute_url not in urls_to_visit
                and "?page=" in absolute_url 
            ):
                urls_to_visit.append(absolute_url)

            # on incrémente le compteur
            crawl_count += 1
    
    #on rajoute l'url cible de base qui a été retirée de la liste car ne comportant pas "?page=", car c'est la première page et on en a besoin
    urls_to_visit.append(target_url)    

    # on affiche la liste
    print(urls_to_visit)

    return urls_to_visit


def scraper(urls: list) -> pd.DataFrame :
    """Scrape le contenu d'une liste de sites webs précédemment crawlés

Parameters
----------
urls : list
    Une liste contenant des URL à scraper

Returns
-------
data: DataFrame
    Les données scrapées sous forme de dataframe pandas.
"""
    # On initialise le dictionnaire qui va contenir les données, une colonne reviews contenant le texte des reviews et une colonne notes contenant les notes associées
    data = {
        'reviews': [],
        'notes': []
    }

    # On itère sur les urls, pour chaque url on parse le code html pour récupérer les reviews sur la page
    for url in urls :
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        reviews = soup.find_all("div", class_="review-card-review-holder")

        # On itère sur chaque review de la page et on y récupère le texte de la review ainsi que la note donnée par l'utilisateur
        for review in reviews :
            text_review = review.find("div", class_="content-txt review-card-content").text.strip()
            note_review = review.find("div", class_="review-card-meta")\
                .find("div", class_="stareval stareval-medium stareval-theme-default")\
                .find("span", class_="stareval-note").text

            # On ajoute ce qu'on a trouvé au dictionnaire
            data['reviews'].append(text_review)
            data['notes'].append(note_review)

    # On convertit notre dictionnaire en un objet DataFrame grâce à pandas
    data = pd.DataFrame(data)

    return data

                            
           

if __name__ == "__main__" :
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument("target", help="L'url à partir de laquelle on souhaite commencer le crawling.")
    my_parser.add_argument("max_crawl", help="Le nombre maximum de crawls à effectuer, par défaut 20.", nargs="?", default=20)
    my_args = my_parser.parse_args()

    urls = crawler(my_args.target, my_args.max_crawl)
    data = scraper(urls)

    data.to_csv('../../data.csv', index=False)  

    