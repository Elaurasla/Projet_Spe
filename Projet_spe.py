from tkinter import *
import tkinter as tk
import tkinter.font as font
import praw
import re
import webbrowser
import arxiv
import nltk
from Corpus import Corpus
from Classes import Document, RedditDocument, ArxivDocument

from tkinter import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
import requests

#-----------Parametres de la fenetre-----------
#Création de la fenêtre
fenetre = tk.Tk()
fenetre.geometry("1000x700")
fenetre.config(background='#d9bc8d')
fenetre.minsize(480,360)

#Définir le font
f = font.Font(family='Fixedsys', size=30)
f_button =font.Font(family='System', size=20)

#Creer la frame principale
frame = Frame(fenetre,bg='#d9bc8d')
frame.pack(expand=YES)

#Titre
label_titre = tk.Label(frame, text= "Recherche d'articles", bg='#d9bc8d')
label_titre['font'] = f
label_titre.pack()

# -----------Widget du Moteur de recherche-----------
#champ de saisie
saisi=tk.Entry(fenetre, width=35)
saisi.place(x=950,y=50)

#Bouton de recherche
recherche= tk.Button(fenetre, text="Rechercher", background="#6ec471")
recherche['font'] = f_button
recherche.place(x=975,y=90)

#Bouton de sortie
bouton = Button(fenetre, text="Fermer", command= fenetre.quit, background="#c24646")
bouton['font'] = f_button
bouton.place(x=500,y=600)

#Connexion a Reddit
reddit = praw.Reddit(client_id='LUIRAKT1qtmz7zCq8j3Lpg', client_secret='-Ho4_YDmIN9s54m6JhQCYlE6NSgkug', user_agent='RedApp')
articles_reddit = []
subreddit = reddit.subreddit("science")
for submission in subreddit.hot(limit=100):
    articles_reddit.append(submission.title + " " + submission.selftext)

#Option pour filtrer les resultats par date
filtre_date = tk.IntVar()
boite_date = tk.Checkbutton(fenetre, text="Filtrer par date", variable=filtre_date, bg='#babf4e' )
boite_date.place(x=975,y=150)

#Menu deroulant
select = tk.StringVar()
options = ["Cette semaine", "Ce mois", "Cette année", "Tous"]
menu = tk.OptionMenu(fenetre, select, *options)
menu.place(x=975,y=300)

def search():
    mots = saisi.get()
    for submission in reddit.subreddit("all").search(mots, sort="relevance", limit=10):
        webbrowser.open(submission.url)

recherche.config(command=search)

#----------Comparaison du nombre d'articles venant de Reddit et d'Arvix---------------------
class App:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.create_widgets()
        self.frame.place(x=50,y=50)

    def create_widgets(self):
        self.nb_reddit_label = tk.Label(self.frame, text="Nombre d'articles de Reddit: 0")
        self.nb_reddit_label.pack()

        self.nb_arxiv_label = tk.Label(self.frame, text="Nombre d'articles d'Arvix: 0")
        self.nb_arxiv_label.pack()

        self.update_button = tk.Button(self.frame, text="Update", command=self.update_stats)
        self.update_button.pack()

    def update_stats(self):
        # On compte le nombre d'articles provenant de Reddit et d'Arxiv
        nb_reddit_articles = 0
        nb_arxiv_articles = 0
        for doc in corpus.documents:
            if doc.getType() == "Reddit":
                nb_reddit_articles += 1
            elif doc.getType() == "Arxiv":
                nb_arxiv_articles += 1

        # On met à jour les labels avec les nouvelles valeurs
        self.nb_reddit_label.config(text=f"Nombre d'articles de Reddit: {nb_reddit_articles}")
        self.nb_arxiv_label.config(text=f"Nombre d'articles d'Arvix: {nb_arxiv_articles}")


# On crée un nouveau Corpus vide
corpus = Corpus("Corpus de documents")

# On crée des objets RedditDocument et ArxivDocument
doc1 = RedditDocument("Article 1", "Author 1", "Content 1", 100)
doc2 = ArxivDocument("Article 2", "Author 2", "Content 2", ["Coauthor 1", "Coauthor 2"])
doc3 = RedditDocument("Article 3", "Author 3", "Content 3", 50)
doc4 = ArxivDocument("Article 4", "Author 4", "Content 4", ["Coauthor 3", "Coauthor 4"])

# On ajoute les documents au Corpus
corpus.add(doc1)
corpus.add(doc2)
corpus.add(doc3)
corpus.add(doc4)

# Fonction de mise à jour du graphique
def update_plot(i):
    # Récupération des données de l'article Reddit
    article_data = requests.get(saisi.get()).text

    # Calcul de la fréquence d'occurrence du mot dans l'article
    word_count = article_data.count(word_entry.get())

    # Ajout du nombre d'occurrences du mot à la liste des données du graphique
    y_vals.append(word_count)
    x_vals.append(i)

    # Mise à jour du graphique
    graph.clear()
    graph.plot(x_vals, y_vals)

# Création des widgets
word_label = Label(fenetre, text="Mot:")
word_entry = Entry(fenetre)
reddit_label = Label(fenetre, text="Article Reddit:")
reddit_entry = Entry(fenetre)

#right_frame.grid(row=0, column=1, sticky=W)

# Création du graphique
figure = Figure(figsize=(3,3))
graph = figure.add_subplot(111)
canvas = FigureCanvasTkAgg(figure, fenetre)
canvas.draw()
canvas.get_tk_widget().pack(side="bottom", anchor="se" )

# Mise à jour du graphique toutes les 1000ms
ani = animation.FuncAnimation(figure, update_plot, interval=1000)

# Ajout des widgets à la fenêtre
word_label.place(x=50, y=600)
word_entry.place(x=50, y=620)
reddit_label.place(x=50, y=640)
reddit_entry.place(x=50, y=660)


#right_frame.pack(side="right")

#Afficher la frame
frame.pack(side="left")
#right_frame.grid(row=0, column=1, sticky=W)

app = App(fenetre)
fenetre.mainloop()
