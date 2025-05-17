# Projet dans le cadre du cours Outils de Traitement de Corpus

## Présentation du projet

Ce projet a pour but de nous familiariser avec les outils de constitution et de traitement de corpus, ce qui comprend le crawling et le scraping des données, ainsi que leur nettoyage, entre autres. Ce projet comporte 6 étapes :

1. Descriptions des besoins du projet (et étude de cas d'un corpus préexistant)
2. Web crawling et scraping
3. Visualisation des données et statistiques sur le corpus
4. Augmentation des données
5. Adaptation d'un modèle transformer adapté à notre tâche sur nos données
6. Evaluation du modèle avec mesures intrinsèques et extrinsèques


L'étape 1 sera développée ci-dessous, tandis que le reste des étapes se reposant sur des scripts, ces derniers se trouveront dans le dossier src de ce dépôt. (Des liens cliquables sont également disponibles dans la liste ci-dessus et amènent directement au script concerné).

## Description des besoins du projet

Ce projet traite de la polarité des émotions dans des évaluations de films. Ce projet s'inscrit donc dans une tâche de classification de document, et plus particulièrement d'analyse de sentiment. Les données exploitées sont donc des données textuelles, récupérées sur le site d'Allociné (https://www.allocine.fr/). Ce corpus est constitué de reviews du film "Minecraft, le film" (2025). Ce corpus a été choisi car les avis sur ce film sont assez divisés, avec autant de critiques négatives que positives, ce qui permet un corpus avec une grande diversité de données. Ces données sont en libre accès, et le scraping des reviews Allociné autorisé selon le fichier robots.txt.

## Etude de cas d'un corpus préexistant : CoNLL 2003

1) Quelle type de tâche propose CoNLL 2003 ?

CoNLL 2003 propose la reconnaissance d’entités nommées indépendamment de la langue (personnes, lieux, organisations, et autres).

2) Quel type de données ya t-il dans CoNLL 2003 ?

Le dataset est composé de 8 fichiers couvrant 2 langues : l’anglais et l’allemand. Les données en anglais viennent du Reuters Corpus qui contient des actualités datant de 96 à 97. Les données en allemand viennent du ECI Multilingual Text Corpus, plus particulièrement du journal allemand Frankfurter Rundshau avec des articles datant de 92.

3) A quel besoin répond CoNLL 2003 ?

Il permet d’entraîner des modèles de reconnaissance d’entités nommées utilisant de l’apprentissage profond.

4) Quels types de modèles ont été entraînés sur CoNLL 2003 ?

ACE, LUKE, FLERT, ASP


5) Le corpus est-il monolingue ou multilingue ?

C’est un corpus multilingue anglais/allemand.
