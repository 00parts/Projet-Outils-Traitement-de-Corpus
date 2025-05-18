from transformers import AutoModelForSequenceClassification, Trainer, AutoTokenizer, TrainingArguments
from datasets import load_dataset
import argparse
from sklearn.metrics import accuracy_score, f1_score
import numpy as np

"""Model train

Ce script prend en argument un fichier csv contenant les données sur lesquelles on souhaite train un modèle. Il génère un modèle finetuné sauvegardé sur l'ordinateur.
Ce script utilise les bibliothèques transformers, datasets, argparse, sklearn et numpy

Ce script comporte  une fonction :
    train_model - train un modèle huggingface sur nos données, et sauvegarde ce modèle sur l'ordinateur

"""


def train_model(data) :

    """
    Train un modèle huggingface sur nos données

    Parameters
    ---
    data : str
    Le chemin vers le fichier contenant nos données

    """
    
    #Le modèle sur lequel on s'appuie (utilise 5 classes, et est entraîné aussi sur des reviews allociné)
    model_name = "cmarkea/distilcamembert-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    #On charge nos données
    dataset = load_dataset("csv", data_files={data})['train']

    #On découpe notre corpus en 3 : 80% de train, 10% de validation et 10% de test 
    # seed = 42 afin de pouvoir reproduire le découpage pour l'évaluation sur le sous-corpus test qu'on n'utilise pas ici
    train_valtest = dataset.train_test_split(test_size = 0.2, seed=42)
    valtest = train_valtest["test"].train_test_split(test_size=0.5, seed=42)

    train_dataset = train_valtest['train']
    val_dataset = valtest['train']
    test_dataset = valtest['test']

    #On tokenize les reviews dans nos données, et on le fait pour les 3 sous-corpus
    def preprocess_function(dataset):
        return tokenizer(dataset["reviews"], truncation=True, padding="max_length", max_length=128)

    train_dataset = train_dataset.map(preprocess_function, batched=True)
    val_dataset = val_dataset.map(preprocess_function, batched=True)
    test_dataset = test_dataset.map(preprocess_function, batched=True)

    #On ajoute les labels qui sont les notes
    #On retire 1à chaque note pour décaler les notes vers la gauche (0 à 4 au lieu de 1 à 5, sinon ça bloque au niveau de la cross-entropie)
    def add_labels(dataset):
        dataset["labels"] = dataset["notes"] - 1
        return dataset

    train_dataset = train_dataset.map(add_labels)
    val_dataset = val_dataset.map(add_labels)
    test_dataset = test_dataset.map(add_labels)

    #Les calculs d'accuracy et de f1 pour le sous-corpus val à chaque tour d'epoch
    def compute_metrics(eval_pred):
        predictions, labels = eval_pred
        preds = np.argmax(predictions, axis=1)
        return {
            "accuracy": accuracy_score(labels, preds),
            "f1": f1_score(labels, preds, average="weighted")
        }

    #Training args pour le trainer contenant le nombre d'epochs, le nombre de batchs
    #Il va train le modèle 3 fois sur le corpus train et évaluer à chaque fois le modèle sur le corpus val
    training_args = TrainingArguments(
        output_dir="../results",
        eval_strategy="epoch",
        save_strategy="epoch",
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        num_train_epochs=3,
        learning_rate=2e-5,
    )

    #On initialise le trainer avec le modèle, les trainings args, nos sous-corpus train et val et la fonction pour afficher les scores
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics
    )

    #On lance le train et on sauvegarde les modèles
    trainer.train()

    trainer.save_model("../bin/model")
    tokenizer.save_pretrained("../bin/model")


if __name__ == "__main__" :
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument("data", help="Le fichier csv contenant le jeu de données")
    my_args = my_parser.parse_args()

    train_model(my_args.data)

