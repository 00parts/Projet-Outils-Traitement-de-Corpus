import pandas as pd
import argparse

"""Harmoniser les classes

Ce script prend en argument un fichier csv qu'on souhaite modifier. 
Ce script sert à adapter les classes en vue d'utiliser certains modèles (ici, le script transforme les float en int et retire les 0)
Ce script utilise les bibliothèques pandas et argparse

Ce script comporte deux fonctions :

    harmonize - permet de transformer les float en int dans le dataframe et drop les lignes qui ont une note de 0 afin de garder 5 classes (1, 2, 3, 4, 5)
    remove_decimal : permet de transformer un float en int 


"""


def harmonize(data) :

    """Harmonise les classes dans un dataframe

    Parameters
    ----------
    data : str 
        Le chemin vers le fichier csv contenant les données

    Returns
    -------
    data : DataFrame
        Le dataframe modifié
    """

    data = pd.read_csv(data)
    
    #On remplace les virgules par des points pour pouvoir convertir ces chiffres en float
    data['notes'] = data['notes'].str.replace(",", ".").apply(float)


    def remove_decimal(x) :
        """Retire les décimales d'un chiffre et le transforme en int

        Parameters
        ----------
        x: int, float
            Le nombre qu'on souhaite transformer en int

        Returns
        -------
        x : int
            Le nombre transformé en int
        """

        #Si x est un int ou un float, et que x modulo 1 = 0,5, on convertit x en int
        if isinstance(x, (int, float)) and x % 1 == 0.5:
            return int(x)
        #Si x est un float, mais qui ne finit pas par 0.5 (par exemple 2.0), on le convertit en int
        return int(x) if isinstance(x, float) else x
    
    #On applique cette fonction à toutes les lignes pour la colonne "notes"
    data['notes'] = data['notes'].apply(remove_decimal)

    #On retire les lignes dont la note est de 0 afin de conserver 5 classes
    data.drop(data[data['notes'] == 0].index, inplace = True)

    return data


if __name__ == "__main__" :

    my_parser = argparse.ArgumentParser()
    my_parser.add_argument("data", help="Le fichier csv contenant le jeu de données")
    my_args = my_parser.parse_args()

    data = harmonize(my_args.data)

    data.to_csv('../../data_harmonized.csv', index=False)  
