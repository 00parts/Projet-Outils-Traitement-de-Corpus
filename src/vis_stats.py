import pandas as pd
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from nltk.corpus import stopwords

"""Visualisation et stats

Ce script prend en argument un fichier csv sur lequel on souhaite réaliser des statistiques. 
Ce script génère des visualisations grâce à matplotlib qu'on peut sauvegarder.

Ce script utilise les bibliothèques pandas, argparse, matplotlib, seaborn, collections et nltk

Ce script comporte  une fonction :
    stats - permet de calculer des moyennes sur le corpus, ainsi que d'autres diverses visualisations

"""


def stats(data: pd.DataFrame) :

    """
    Réalise différentes statistiques et visualisations sur un jeu de données de type DataFrame

    Parameters
    ---
    data : Dataframe
    Le jeu de données sur lequel on souhaite réaliser des statistiques
    
    """

    # On transforme le texte des reviews en une liste de mots
    data['reviews'] = data['reviews'].str.lower().replace(r'[^\w\s]', " ", regex=True).str.split()

    # On calcule la moyenne de la longueur des textes et la moyenne des notes (on en profite pour convertir les notes en float, qui étaient des str jusqu'ici)
    nombre_mots = data['reviews'].apply(len)
    moyenne_mots = nombre_mots.mean()
    data['notes'] = data['notes'].str.replace(",", ".").apply(float)
    notes_mean = data['notes'].mean(axis=0)

    # On écrit ces informations dans un fichier txt, et on calcule aussi le nombre de reviews par note
    with open("../figures/moyenne_compte_par_notes.txt", "w") as f:
        f.write(f"La longueur moyenne des reviews est de {moyenne_mots} mots\n\n")
        f.write(f"La note moyenne donnée par les utilisateurs est de {notes_mean} étoiles\n\n")
        f.write(f"Voici le nombre de reviews par note : \n\n {data.groupby(['notes']).count()}")
   

    # On fait la visualisation du nombre de reviews par note
    plt.figure(figsize=(8,6))
    sns.barplot(data=data.groupby(['notes']).count(), x='notes', y='reviews')
    plt.title("Nombre de reviews par note")
    plt.xlabel("Note")
    plt.ylabel("Nombre de reviews")
    plt.show()


    # A partir d'ici on fait la visualisation de la loi de Zipf sur notre corpus
    
    #On ajoute toutes les listes de mots dans une grande liste aplatie, en retirant au passage les stopwords
    stop_words = set(stopwords.words('french'))

    all_words = []
    for text in data["reviews"] :
        all_words.extend(text)

    all_words_no_stopwords = []
    for word in all_words :
        if word not in stop_words:
            all_words_no_stopwords.append(word)

    # On compte les occurrences de chaque mot et on les trie par ordre du plus fréquent au moins fréquent
    word_count = Counter(all_words_no_stopwords)
    sorted_counts = word_count.most_common()

    # On créé les variables frequencies qui comporte les fréquences et ranks qui comporte les rangs (1 : le plus fréquent, jusqu'au dernier nombre : le moins fréquent)
    frequencies = [count for word, count in sorted_counts]
    ranks = range(1, len(frequencies) + 1)


    # On créé la visualisation
    plt.plot(ranks,frequencies)
    plt.xlabel('Rank(r)')
    plt.ylabel('Frequency(f)')
    plt.title("Zipf's law")
    plt.show()
    
    # On modifie la colonne "reviews", au lieu de la liste de mots, on a le nombre de mots
    data['reviews'] = data['reviews'].apply(len)

    # On fait la visualisation de la longueur des textes selon la note sous la forme d'un boxplot qui nous permet de voir les outliers
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='notes', y='reviews', data=data)
    plt.title("Longueur des textes selon la note")
    plt.xlabel("Note")
    plt.ylabel("Longueur du texte (en mots)")
    plt.show()


    # On calcule la moyenne de longueur des textes pour chaque note et on en fait la visualisation
    mean_lengths = data.groupby('notes')['reviews'].mean().reset_index()

    plt.figure(figsize=(8, 6))
    sns.barplot(x='notes', y='reviews', data=mean_lengths)
    plt.title("Longueur moyenne des textes selon la note")
    plt.xlabel("Note")
    plt.ylabel("Longueur moyenne du texte")
    plt.show()



if __name__ == "__main__" :
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument("data", help="Fichier csv sur lequel réaliser des statistiques")
    my_args = my_parser.parse_args()

    data = my_args.data
    data = pd.read_csv(data)

    stats(data)
