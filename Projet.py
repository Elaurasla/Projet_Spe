# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 15:16:42 2023

@author: Viper
""" 
import pickle


# =============== Extraction de données Reddit et Arxiv =============
"""
# =============== REDDIT ===============
import praw

 # réccupération de documents reddit
# Reddit

reddit = praw.Reddit(client_id='3W45Yb6_QSc9TkeSFGzc2A', client_secret='AnCzvEYnv1EpHbMysuhgl4rTCQ4_dg', user_agent='Abdourah')

# Requète
limit = 100
hot_posts = reddit.subreddit('all').hot(limit=limit)

# Recuperation du texte
docs = []
docs_bruts = []
afficher_cles = False
for i, post in enumerate(hot_posts):
    if i%10==0: print("Reddit:", i, "/", limit)
    
    if afficher_cles:  # Pour connaitre les différentes variables et leur contenu
        for k, v in post.__dict__.items():
            pass
            print(k, ":", v)

    if post.selftext != "":  # Osef des posts sans texte
        pass
        #print(post.selftext)
    docs.append(post.selftext.replace("\n", " "))
    docs_bruts.append(("Reddit", post))

print(docs,"\n")


# =============== ArXiv ===============
# Libraries
import urllib, urllib.request, _collections
import xmltodict

# Paramètres
query_terms = ["IA", "art"]
max_results = 50

# RequÃªte
url = f'http://export.arxiv.org/api/query?search_query=all:{"+".join(query_terms)}&start=0&max_results={max_results}'
data = urllib.request.urlopen(url)

# Format dict (OrderedDict)
data = xmltodict.parse(data.read().decode('utf-8'))


# Ajout résumés à la liste
for i, entry in enumerate(data["feed"]["entry"]):
    if i%10==0: print("ArXiv:", i, "/", limit)
    docs.append(entry["summary"].replace("\n", ""))
    docs_bruts.append(("ArXiv", entry))
    
    
# =============== Exploitation ===============
print(f"# docs avec doublons : {len(docs)}")
docs = list(set(docs))
print(f"# docs sans doublons : {len(docs)}")

# on enlève les documents qui font moins de 100 mots
for i, doc in enumerate(docs):
    print(f"Document {i}\t# caracteres : {len(doc)}\t# mots : {len(doc.split(' '))}\t# phrases : {len(doc.split('.'))}")
    if len(doc)<100:
        docs.remove(doc)

longueChaineDeCaracteres = " ".join(docs)
#il faudra l'enregistrer



# creation d'objets documents ou placer les textes

from Classes import Document

import datetime
collection = []
for nature, doc in docs_bruts:
    if nature == "ArXiv":  # Les fichiers de ArXiv ou de Reddit sont pas formates de la meme maniere a ce stade.

        titre = doc["title"].replace('\n', '')  # On enleve les retours a la ligne
        try:
            authors = ", ".join([a["name"] for a in doc["author"]])  # On fait une liste d'auteurs, separes par une virgule
        except:
            authors = doc["author"]["name"]  # Si l'auteur est seul, pas besoin de liste
        summary = doc["summary"].replace("\n", "")  # On enleve les retours a la ligne
        date = datetime.datetime.strptime(doc["published"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d")  # Formatage de la date en annee/mois/jour avec librairie datetime

        doc_classe = Document(titre, authors, date, doc["id"], summary)  # Creation du Document
        collection.append(doc_classe)  # Ajout du Document a la liste.

    elif nature == "Reddit":
        titre = doc.title.replace("\n", '')
        auteur = str(doc.author)
        date = datetime.datetime.fromtimestamp(doc.created).strftime("%Y/%m/%d")
        url = "https://www.reddit.com/"+doc.permalink
        texte = doc.selftext.replace("\n", "")

        doc_classe = Document(titre, auteur, date, url, texte)

        collection.append(doc_classe)
        

# =============== Creation des corpus de documents ===============
# Creation de l'index de documents
id2doc = {}

for key, doc in enumerate(collection):
    id2doc[key] = doc

from Classes import Author

authors = {}
aut2id = {}
num_auteurs_vus = 0

for doc in collection:
    if doc.auteur not in aut2id:
        num_auteurs_vus += 1
        authors[num_auteurs_vus] = Author(doc.auteur)
        aut2id[doc.auteur] = num_auteurs_vus

    authors[aut2id[doc.auteur]].add(doc.texte)

#creation d'un corpus de doc et auteur
import Corpus
corpus = Corpus.Corpus("Corpus")

# Construction du corpus a partir des documents
for doc in collection:
    corpus.add(doc)
corpus.show(tri="abc")


# =============== SAUVEGARDE ===============


# Ouverture d'un fichier, puis ecriture avec pickle
with open("corpus.pkl", "wb") as f:
    pickle.dump(corpus, f)
    
# Supression de la variable "corpus"
del corpus
    
with open("chaine_longue.pkl", "wb") as f:
    pickle.dump(longueChaineDeCaracteres, f)

"""


# =============== Charger les documents enregistrés ===============

# Ouverture du fichier corpus
with open("corpus.pkl", "rb") as f:
    corpus = pickle.load(f)

# La variable est reapparue
print(corpus)

# Ouverture du fichier contenant une longue chaine
with open("chaine_longue.pkl", "rb") as f:
    chaineLongue = pickle.load(f)



# =============== Chargement graphique des documents ===============


# =============== Analyse des textes ===============


# =============== Moteur de recherche ===============
# mise en accès graphique