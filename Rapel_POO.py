#import pandas as pd  # (import facultatif ici, mais ajouté pour suivre ton exemple)


############### les classes #################

# %%
class Chien:
    pass
# `pass` pour dire que la classe ne fait encore aucune action

# %%


############### Object (Instance) #################

# %%
mon_chien = Chien()
type(mon_chien)
# Cela affiche : <class '__main__.Chien'>

# %%


############### les Attributs : ce sont les infos propres à chaque objet #################

# __init__ est une méthode spéciale appelée lors de la création d'un objet.
# nom, race et age sont des attributs que l'on donne à chaque objet Chien

# %%
class Chien:
    def __init__(self, nom, race, age):
        self.nom = nom
        self.race = race
        self.age = age

# %%
mon_chien = Chien("Milou", "Chien baoulé", 3)
print(mon_chien.nom)    # Affiche: Milou
print(mon_chien.race)   # Affiche: Chien baoulé
print(mon_chien.age)    # Affiche: 3

# %%


############### Les Méthodes (Actions que l'objet peut effectuer) #################

# Une méthode est une fonction propre à une classe.
# Exemple : aboyer, se présenter, manger, dormir, jouer

# %%
class Chien:
    def __init__(self, nom, race, age):
        self.nom = nom
        self.race = race
        self.age = age
        self.energie = 100  # Valeur par défaut

    def aboyer(self):
        return f"{self.nom} aboie : Ouaf Ouaf !"

    def se_presenter(self):
        return f"Je suis {self.nom}, un {self.race}, j'ai {self.age} an(s)."

    def manger(self):
        self.energie += 10
        if self.energie > 100:
            self.energie = 100
        return f"{self.nom} a mangé. Énergie : {self.energie}"

    def dormir(self):
        self.energie = 100
        return f"{self.nom} a dormi. Énergie restaurée à {self.energie}."

    def jouer(self):
        if self.energie >= 30:
            self.energie -= 30
            return f"{self.nom} joue ! Il lui reste {self.energie} d'énergie."
        else:
            return f"{self.nom} est trop fatigué pour jouer."

    def anniversaire(self):
        self.age += 1
        return f"{self.nom} fête son anniversaire ! Il a maintenant {self.age} an(s)."

# %%
mon_chien = Chien("Milou", "Chien baoulé", 3)
print(mon_chien.se_presenter())     # Présentation
print(mon_chien.aboyer())           # Aboiement
print(mon_chien.jouer())            # Il joue
print(mon_chien.manger())           # Il mange
print(mon_chien.jouer())            # Il rejoue
print(mon_chien.dormir())           # Il se repose
print(mon_chien.anniversaire())     # Joyeux anniversaire !

# %%
