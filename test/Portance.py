"""
Deux types de méthodes de calcul de la capacité portante sont développées dans ce qui suit : les méthodes à partir des résultats des essais de laboratoire, c'est-à-dire à partir des résultats des essais de laboratoire (cohésion / angle de frottement) et les méthodes à partir des résultats des essais in situ (pression limite du pressiomètre Ménard et résistance de point du CPT)
"""





import math






class PortanceLaboratoire(object):
 def __init__(self, cohesion, angle_de_frottement, semelle, poids_volumique, etat_du_sol):
  self.cohesion = cohesion
  self.angle_de_frottement = angle_de_frottement
  self.semelle = semelle
  self.poids_volumique = poids_volumique
  self.etat_du_sol = etat_du_sol
 
 def facteurs_q_drained(self):
  return math.exp(math.pi * math.tan(self.angle_de_frottement)) * pow(math.tan((math.pi / 4) + (self.angle_de_frottement / 2)), 2)
 def facteurs_c_drained(self):
  return (self.facteurs_q_drained() - 1) * (1 / math.tan(self.angle_de_frottement))
 def facteurs_gamma_drained(self):
  return 2 * (self.facteurs_q_drained() - 1) * math.tan(self.angle_de_frottement)
 def terme_de_surface(self):
  if self.etat_du_sol == 'undrained':
   return 0
  elif self.etat_du_sol == 'drained':
   return 0.5 * self.semelle.largeur * self.facteurs_gamma_drained() * self.poids_volumique
 
 def terme_de_cohesion(self):
  if self.etat_du_sol == 'undrained':
   return 5.14 * self.cohesion
  elif self.etat_du_sol == 'drained':
   return self.facteurs_c_drained() * self.cohesion
 
 def terme_de_surcharge(self):
  return self.poids_volumique * self.semelle.ancrage
 
 def pression_limite(self):
  return self.terme_de_cohesion() + self.terme_de_surcharge() + self.terme_de_surface()
 
 # l'influence de la forme de la fondation, de l'inclinaison et de l'excentrement de la fondation est à faire





# class PortancePressiometre(object):





# class PortanceCPT(object):
