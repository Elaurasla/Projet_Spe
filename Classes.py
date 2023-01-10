# Correction de G. Poux-Médard, 2021-2022

# =============== La classe Document ===============
class Document:
    # Initialisation des variables de la classe
    def __init__(self, titre="", auteur="", date="", url="", texte=""):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
        self.type = None

    def getType(self):
        return self.type
    
# =============== REPRESENTATIONS ===============
    # Fonction qui renvoie le texte a afficher lorsqu'on tape repr(classe)
    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\t"

    # Fonction qui renvoie le texte a afficher lorsqu'on tape str(classe)
    def __str__(self):
        return f"{self.titre}, par {self.auteur}"
    

class RedditDocument(Document):
    def __init__(self, titre="", auteur="", date="", url="", texte="", nbComment=0):
        super().__init__(self, auteur=auteur, date=date, url=url, texte=texte)
        self.__nbComment = nbComment
        self.type = "Reddit"

    def GetCom(self):
        return self.__nbComment

    def SetCom(self):
        return self.__nbComment

    def __str__(self):
        return f"{self.__commentaire}, par {self.__commentaire}"

class ArxivDocument(Document):
    def __init__(self, titre="", auteur="", date="", url="", texte="", CoAuteurs=""):
        super().__init__(self, auteur=auteur, date=date, url=url, texte=texte)
        self.__CoAuteurs = CoAuteurs
        self.type = "Arxiv"

    def GetCoAut(self):
        return self.__CoAuteurs

    def SetCoAut(self):
        return self.__CoAuteurs

    def __str__(self):
        return f"{self.__CoAuteurs}, par {self.__CoAuteurs}"






# =============== 2.4 : La classe Author ===============
class Author:
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = []
# =============== 2.5 : ADD ===============
    def add(self, production):
        self.ndoc += 1
        self.production.append(production)
    def __str__(self):
        return f"Auteur : {self.name}\t# productions : {self.ndoc}"