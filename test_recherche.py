from tkinter import *
import requests

root = Tk()

# Création de la fenêtre principale
root.title("Moteur de recherche d'articles Reddit et Arxiv")
root.geometry("700x400")

#Bouton de saisi
search_entry=Entry(root, width=35)
search_entry.pack()

#Bouton de recherches
recherche= Button(root, text="Rechercher", background="#6ec471")
#recherche['font'] = f_button
recherche.pack()

# Classe représentant un article
class Article:
    def __init__(self, title, source):
        self.title = title
        self.source = source

# Fonction de recherche des articles
def search_articles(query):
    # Requête de l'API de Reddit et récupération des résultats
    reddit_url = "https://www.reddit.com/search.json?q=" + query
    reddit_results = requests.get(reddit_url).json()["data"]["children"]

    # Requête de l'API d'Arxiv et récupération des résultats
    arxiv_url = "http://export.arxiv.org/api/query?search_query=" + query
    arxiv_results = requests.get(arxiv_url).json()["feed"]["entry"]

    # Création de la liste des articles trouvés
    articles = []
    for result in reddit_results:
        articles.append(Article(result["data"]["title"], "Reddit"))
    for result in arxiv_results:
        articles.append(Article(result["title"]["$t"], "Arxiv"))

    return articles

# Fonction de traitement de la recherche
def search():
    # Récupération de la requête de recherche
    query = search_entry.get()

    # Recherche des articles
    articles = search_articles(query)

    # Affichage des résultats de la recherche
    for article in articles:
        article_label = Label(root, text=article.title + " (" + article.source + ")")
        article_label.pack()

recherche.config(command=search)


root.mainloop()