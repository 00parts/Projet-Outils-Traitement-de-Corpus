from transformers import AutoModelForSequenceClassification, Trainer, AutoTokenizer, TrainingArguments
from datasets import load_dataset
import argparse
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
import numpy as np
import matplotlib.pyplot as plt

""" Evaluate model

Ce script prend en argument un fichier csv contenant les données sur lesquelles on souhaite évaluer un modèle. 
Il calcule l'accuracy et la f-mesure et génère une matrice de confusion.
Ce script utilise les bibliothèques transformers, datasets, argparse, sklearn, numpy et matplotlib

Ce script comporte  une fonction :
    evaluate_model - évalue un modèle sur un sous-corpus de test

"""


def evaluate_model(dataset) :
    
    """
    Evalue un modèle qu'on a train sur un jeu de données test

    Parameters
    ---
    dataset : str
    Le chemin vers le fichier contenant nos données

    """

    #Le dossier contenant le modèle qu'on a généré grâce au script model_train.py
    model_dir = "../bin/model"
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(model_dir)

    #On charge notre jeu de données et on le split de la même manière que pour train le modèle (grâce au seed)
    #sauf qu'ici on utilisera que le jeu de test qu'on n'avait pas utilisé avant
    dataset = load_dataset("csv", data_files=dataset)["train"]
    train_valtest = dataset.train_test_split(test_size = 0.2, seed=42)
    valtest = train_valtest["test"].train_test_split(test_size=0.5, seed=42)

    train_dataset = train_valtest['train']
    val_dataset = valtest['train']
    test_dataset = valtest['test']

    #On tokenize les reviews du jeu de données test et on ajoute les labels qui sont les notes (décalées de 1 vers la gauche encore une fois)
    def preprocess_function(dataset):
        return tokenizer(dataset["reviews"], truncation=True, padding="max_length", max_length=128)

    test_dataset = test_dataset.map(preprocess_function)

    def add_labels(dataset):
        dataset["labels"] = dataset["notes"] - 1
        return dataset

    test_dataset = test_dataset.map(add_labels)

    #On initialise le trainer et ses arguments, avec le dataset d'évaluation étant le sous-corpus test qui représente 10% du corpus total
    args = TrainingArguments(
        output_dir="./tmp", 
        per_device_eval_batch_size=1
        )
    
    trainer = Trainer(
    model=model,
    args=args,
    eval_dataset= test_dataset
    )


    #On affiche les résultats et on calcule l'accuracy et la f-mesure
    eval_result = trainer.evaluate(test_dataset)
    print("Résultats bruts :", eval_result)

    predictions = trainer.predict(test_dataset)
    y_pred = np.argmax(predictions.predictions, axis=1)
    y_true = predictions.label_ids

    acc = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average="weighted")

    print(f"Accuracy : {acc:.2%}")
    print(f"F-mesure : {f1:.2%}")

    #Avant de faire la matrice de confusion on redécale les notes vers la droite (on les remet de 1 à 5)
    y_pred_notes = y_pred + 1
    y_true_notes = test_dataset["labels"]
    y_true_notes = [label + 1 for label in y_true_notes]

    #On créé la matrice de confusion et on l'affiche
    matrice_confusion = confusion_matrix(y_true_notes, y_pred_notes)
    disp = ConfusionMatrixDisplay(confusion_matrix=matrice_confusion, display_labels=[1, 2, 3, 4, 5])
    disp.plot(cmap="Blues", values_format="d")
    plt.title("Matrice de confusion")
    plt.show()



if __name__ == "__main__" :
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument("data", help="Le fichier csv contenant le jeu de données")
    my_args = my_parser.parse_args()

    evaluate_model(my_args.data)
