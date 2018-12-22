"""
pour le moment : demander une nouvelle couche et afficher les couches crées
et calculer la contrainte totale à une profondeur donnée
"""





class Sol (object):
  def __init__(self):
    self.couches = []
    self.nom_couche = 'undefined'
    self.poids_volumique = None
    self.epaisseur = None
    self.toit_de_couche = None
    self.base_de_couche = None

  def get_nouvelle_couche(self):
    # ici je demande le nom de la couche, son poids volumique et son epaisseur
    # je calcule la profondeur du toit et du mur de la couche
    # j'ajoute la couche à la liste des couches
    self.nom_couche = input("Nom de la couche : ")
    self.poids_volumique = float(input("Poids volumique: "))
    self.epaisseur = float(input("Epaisseur: "))
    if len(self.couches) > 0:
      self.toit_de_couche = self.couches[len(self.couches) - 1]["bas_de_couche"]
    else:
      self.toit_de_couche = 0
    self.base_de_couche = self.toit_de_couche + self.epaisseur
    couche = {"nom_couche": self.nom_couche, "poids_volumique": self.poids_volumique, "epaisseur": self.epaisseur, "toit_de_couche": self.toit_de_couche, "bas_de_couche": self.base_de_couche}
    self.couches.append(couche)

  def print_couches(self):
    # simplement afficher les couches crées
    print("\nIl existe " + str(len(self.couches)) + " couches dans ce sol.")
    for i in range(len(self.couches)):
      print(str(i + 1) + ". " + self.couches[i]["nom_couche"] + ": " + str(self.couches[i]["poids_volumique"]) + " kN/m^3 dans l'intervalle [" + str(self.couches[i]["toit_de_couche"]) + ", " + str(self.couches[i]["bas_de_couche"]) + "].")

  def contraintes_a_un_point(self, profondeur):
    contraintes = 0
    for i in range(len(self.couches)):
      if profondeur < self.couches[i]["bas_de_couche"] and profondeur > self.couches[i]["toit_de_couche"]:
        print("Ce point est dans la couche : " + self.couches[i]["nom_couche"])
        # ici je vais implémanter le calcul de la contrainte
        for j in range(i + 1):
          for k in range(i):
            if j < self.couches[k]["bas_de_couche"] and j > self.couches[k]["toit_de_couche"]:
              contraintes += j * self.couches[k]["poids_volumique"]
        # la logique au dessus est fausse, je dois refaire
        print("La contrainte normale à " + str(profondeur) + "m de profondeur est " + str(contraintes) + "kPa.")
      elif profondeur < 0 or profondeur > self.couches[len(self.couches) - 1]["bas_de_couche"]:
        print("Pas de données dans ce point.")
