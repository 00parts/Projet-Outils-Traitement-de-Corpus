import pandas as pd
import argparse
from textaugment import Translate

"""Augmentation de données

Ce script prend en entrée un dataset sous forme csv et en augmente les données grâce à la technique de la rétro-traduction.
Ce script traduit chaque review en anglais, puis de nouveau en français, et ajoute cette nouvelle review au DataFrame avec la même note que la review de base.

Ce script utilise les bibliothèques pandas, argparse et textaugment.

Crédits pour la librairie textaugment :

@inproceedings{marivate2020improving,
  title={Improving short text classification through global augmentation methods},
  author={Marivate, Vukosi and Sefara, Tshephisho},
  booktitle={International Cross-Domain Conference for Machine Learning and Knowledge Extraction},
  pages={385--399},
  year={2020},
  organization={Springer}
}


Ce script comporte une fonction :

    * augment - retourne le dataset avec les nouvelles données synthétiques

"""


def augment(data: pd.DataFrame):
    """
    Ajoute des données synthétiques à un corpus de données

    Parameters
    ---
    data : DataFrame
    Le dataset dont on souhaite augmenter les données

    Returns
    ---
    data : DataFrame
    Le dataset avec les nouvelles données synthétiques
    """
    
    t = Translate(src="fr", to="en")

    reviews = data['reviews']

    for i in range(len(reviews)):
        new_text = t.augment(data['reviews'][i])
        data.loc[len(data)] = [new_text, data['notes'][i] ]

    return data   


if __name__ == "__main__" :

    my_parser = argparse.ArgumentParser()
    my_parser.add_argument("data", help="Le fichier csv contenant le jeu de données")
    my_args = my_parser.parse_args()

    data = my_args.data
    data = pd.read_csv(data)

    data_augmented = augment(data)
    data_augmented.to_csv('../../data_augmented.csv', index=False)  






