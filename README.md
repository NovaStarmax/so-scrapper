# 📊 SO-Scrapper

Un projet de scraping de Stack Overflow pour extraire, stocker et analyser les dernières tendances en **Data Science**. Le projet combine **scraping manuel**, **appel API**, **MongoDB**, **data mining**, **visualisation**, et **tests automatisés**.

---

## 🚀 Objectif

Ce projet a pour but de :
- Récupérer des données depuis Stack Overflow (scrapping manuel avec BeautifulSoup + API officielle),
- Stocker les données dans une base MongoDB locale,
- Nettoyer et analyser les textes,
- Visualiser les grandes tendances liées à la Data Science.

---

## 🏗️ Arborescence du projet

```
so-scrapper/
│
├── eda/                        # Notebooks d'analyse
│   ├── datascience.ipynb       # Analyses des posts API
│   ├── newest.ipynb            # Analyses des posts scrappés
│   └── text_mining.py          # Classe de traitement NLP
│
├── handle_io/
│   ├── api.json                # Données API localement stockées
│   ├── scrapper.json           # Données Scrapper localement stockées
│   └── sync_db.py              # Fonction de synchronisation JSON <-> MongoDB
│
├── src/
│   ├── api.py                  # Récupération via API StackOverflow
│   ├── database.py             # Connexion MongoDB + fonctions DB
│   └── scrapper.py             # Scraping manuel avec BeautifulSoup
│
├── tests/                      # Tests Pytest (API & Scrapper)
│   ├── test_api.py
│   └── test_scrapper.py
│
├── main.py                     # Script de synchronisation entre MongoDB et JSON
├── setup.py                    # Script de setup initial (DB, index, nltk)
├── .env                        # Variables d'environnement (Mongo URI, DB, etc.)
├── pyproject.toml              # Dépendances & config Pytest
├── README.md
└── uv.lock
```

---

## ⚙️ Prérequis

- Python ≥ 3.10
- [`uv`](https://github.com/astral-sh/uv) pour gérer les dépendances
- [MongoDB](https://www.mongodb.com/try/download/community) installé localement

---

## 🛠️ Installation

1. Clone le repo :
   ```bash
   git clone https://github.com/tonio/so-scrapper.git
   cd so-scrapper
   ```

2. Crée un environnement et installe les dépendances :
   ```bash
   uv sync
   # or
   uv pip install -r requirements.txt  # ou utilise pyproject.toml avec uv install
   ```

3. Remplis ton fichier `.env` :
   ```env
   CLIENT=mongodb://localhost:27017/
   DB=so_scrapper_db
   COLLECTION_API=api
   COLLECTION_SCRAPPER=scrapper
   ```

4. Lance le setup initial :
   ```bash
   uv run setup.py
   ```

   > Cela crée les collections MongoDB nécessaires, les indexes uniques sur `"link"`, synchronise les fichiers `*.json`, et télécharge les ressources NLTK (`stopwords`, `wordnet`).

---

## 📦 Commandes principales

- Scraping manuel :
  ```bash
  uv run src/scrapper.py
  ```

- Récupération via API :
  ```bash
  uv run src/api.py
  ```

- Lancer les tests :
  ```bash
  uv run pytest -m scrapper
  uv run pytest -m api
  ```

---

## 🧪 EDA et Text Mining

- L’analyse exploratoire est faite dans `eda/`
- La classe `TextMining` (`text_mining.py`) permet :
  - Nettoyage
  - Tokenisation
  - Suppression des stopwords
  - Lemmatisation
  - Extraction de mots-clés
  - Génération de nuages de mots et graphes

---

## 📌 À venir

- Export d’un dashboard interactif
- Déploiement sur un service cloud

---

## 🎓 Contexte pédagogique

Ce projet a été réalisé dans un cadre **pédagogique** et mobilise :

- 🧩 **Scraping Web** avec `BeautifulSoup` et `requests`
- 🛠️ **MongoDB** pour stocker les données
- 📊 **Exploration et visualisation** avec `matplotlib`, `seaborn`, `wordcloud`, `networkx`
- 🧪 **Tests unitaires** avec `pytest` et `pytest.mark`
- 🧠 **Text mining** et prétraitement NLP avec `NLTK`, `sklearn`
- ⚙️ Gestion de projet Python avec `uv`, `dotenv`, `pyproject.toml`