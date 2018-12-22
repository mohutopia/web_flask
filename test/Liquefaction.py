"""
1. No wrong input error handling

2. Whenever I enter 
    qc = 6000
    fs = 200 
    sigma' = 66
    sigma = 77
   for a CPT test I get an error on FS.calcul_FS()
"""




import math





class CSR(object):
 def __init__(self, acceleration_max, contrainte_effective_initiale, contrainte_totale_initiale, profondeur):
  self.acceleration_max = acceleration_max * 9.81
  self.contrainte_effective_initiale = contrainte_effective_initiale
  self.contrainte_totale_initiale = contrainte_totale_initiale
  self.profondeur = profondeur
  self.gravite = 9.81
 
 # rd est le facteur correcteur de réduction de la contrainte à une certaine profondeur
 def facteur_rd(self):
  if self.profondeur <= 9.15 and self.profondeur > 0:
   return (1 - (0.00765 * self.profondeur))
  elif self.profondeur > 9.15 and self.profondeur <= 23:
   return (1.174 - (0.0267 * self.profondeur))
 
 # calcul final de la contrainte de cisaillement induite par le séisme
 def calcul_CSR(self):
  return (0.65 * self.facteur_rd() * (self.acceleration_max / self.gravite) * (self.contrainte_totale_initiale / self.contrainte_effective_initiale))
 
 def result_CSR(self):
  print("Le CSR est de " + str(self.calcul_CSR()))





class SPT(object):
  def __init__(self, N, contrainte_effective_initiale, FC):
    self.N = N # Nombre de coups N1 + N2 donné par l'essai SPT qui sera corrigé
    self.contrainte_effective_initiale = contrainte_effective_initiale
    self.FC = FC # FC : fines content ou % des fines

  def CN(self):
    cn = 2.2 / (1.2 + (self.contrainte_effective_initiale / 100))
    if cn > 1.7:
      cn = pow((100 / self.contrainte_effective_initiale), 0.5)
    return cn
  def CE(self):
    return 1 # correction for hammer energy
  def CB(self):
    return 1 # correction factor for borehole diameter
  def CR(self):
    return 1 # correction factor for rod length
  def CS(self):
    return 1 # correction for samplers with or without liners
  
  def N160(self):
    return (self.N * self.CN() * self.CE() * self.CB() * self.CR() * self.CS()) 
  
  def N160cs(self):
    if self.FC > 0 and self.FC < 0.05:
      a = 0
      b = 1
    elif self.FC < 0.35 and self.FC > 0.05:
      a = math.exp((1.76 - (190 / pow(self.FC, 2))))
      b = 0.99 + (pow(self.FC, 1.5) / 1000)
    elif self.FC > 0.35:
      a = 5
      b = 1.2
    return a + (b * self.N160()) # corrected N accounted for the influence of fines content





class CPT(object):
  n = 1
  def __init__(self, qc, fs, contrainte_effective_initiale, contrainte_totale_initiale):
    self.qc = qc
    self.fs = fs
    self.contrainte_effective_initiale = contrainte_effective_initiale
    self.contrainte_totale_initiale = contrainte_totale_initiale
  
  def CQ(self):
    cq = pow((100 / self.contrainte_effective_initiale), self.n)
    if cq > 1.7:
      cq = 1.7
    return cq

  def qc1n(self):
    return (self.qc * self.CQ()) / 100
  
  def Q(self):
    return ((self.qc - self.contrainte_totale_initiale) / 100) * pow((100 / self.contrainte_effective_initiale), self.n) # 100 est la pression atmosphérique Pa = 100 KPa
  
  def F(self):
    return ((self.fs / (self.qc - self.contrainte_totale_initiale)) * 100) # %

  def Ic(self):
    f = self.F()
    q = self.Q()
    return pow((pow((3.47 - math.log10(q)), 2) + pow((1.22 + math.log10(f)), 2)),0.5)

  # facteur de correction, tenant compte des caractéristiques des grains constituant le sol
  def Kc(self):
    if self.Ic() <= 1.6:
      return 1
    elif self.Ic() >= 2.6:
      # print("Facteur Ic > 2.6 : donc un sol argileux non-liquéfiable")
      return 0
    # on a supposé n = 1
    # en calculant Ic < 2.6 alors on le considère un sol granulaire
    # on recalcule Ic pour n = 0.5
    # si Ic < 2.6 alors on poursuit les calculs sinon on suppose n = 0.7
    elif self.Ic() > 1.6 and self.Ic() < 2.6:
      self.n = 0.5
      self.Q()
      self.Ic()
      if self.Ic() > 2.6:
        return 0
      elif self.Ic() < 2.6:
        return ((-0.403 * pow(self.Ic(), 4)) + (5.581 * pow(self.Ic(), 3)) - (21.63 * pow(self.Ic(), 2)) + (33.75 * self.Ic()) - 17.88)
    # elif self.Ic() < 2.6:
    #   return ((-0.403 * pow(self.Ic(), 4)) + (5.581 * pow(self.Ic(), 3)) - (21.63 * pow(self.Ic(), 2)) + (33.75 * self.Ic()) - 17.88)
    
  def qc1ncs(self):
    return self.Kc() * self.qc1n()





class Vs(object):
  def __init__(self, Vs, contrainte_effective_initiale, FC):
    self.Vs = Vs
    self.contrainte_effective_initiale = contrainte_effective_initiale
    self.FC = FC
  
  def Vs1(self):
    return self.Vs * pow((100 / self.contrainte_effective_initiale), 0.25)
  
  def Vs1c(self):
    if self.FC <= 0.05 and self.FC > 0:
      return 220
    elif self.FC >= 0.35 and self.FC < 1:
      return 200
    else:
      return 210





class CRR75(object):
  def __init__(self, test_method, test_class):
    self.test_method = test_method
    self.test_class = test_class
  
  def calcul_CRR75(self):
    if self.test_method == 'cpt':
      if self.test_class.qc1ncs() >= 50 and self.test_class.qc1ncs() < 160:
        return (93 * pow((self.test_class.qc1ncs() / 1000), 3)) + 0.08
      elif self.test_class.qc1ncs() < 50:
        return (0.833 * (self.test_class.qc1ncs() / 1000)) + 0.05
    elif self.test_method == 'spt':
      return ((1 / (34 - self.test_class.N160cs())) + (self.test_class.N160cs() / 135) + (50 / pow((10*self.test_class.N160cs() + 45), 2)) - (1 / 200))
    elif self.test_method == 'vs':
      return (0.03 * pow((self.test_class.Vs1() / 100), 2)) + (0.9 * ((1 / (self.test_class.Vs1c() - self.test_class.Vs1())) - (1 / self.test_class.Vs1c())))

  def result_CRR75(self):
    print("Le CRR est de " + str(self.calcul_CRR75()))





class Facteur_de_Securite(CSR, CRR75):
  def __init__(self, acceleration_max, contrainte_effective_initiale, contrainte_totale_initiale, profondeur, test_method, test_class, magnitude, densite_relative):
    CSR.__init__(self, acceleration_max, contrainte_effective_initiale, contrainte_totale_initiale, profondeur)
    CRR75.__init__(self, test_method, test_class)
    self.magnitude = magnitude
    self.densite_relative = densite_relative
  
  def MSF(self):
    return pow(10, 2.24) / pow(self.magnitude, 2.56)
  
  def K_sigma(self):
    if self.densite_relative == 0.4:
      f = 0.6
    elif self.densite_relative == 0.6:
      f = 0.7
    elif self.densite_relative == 0.8:
      f = 0.8
    else:
      f = 0.5
    return pow((self.contrainte_effective_initiale / 100), (f - 1))
  
  def calcul_FS(self):
    return (self.calcul_CRR75() * self.MSF() * self.K_sigma()) / self.calcul_CSR()

  def potentiel_liquefaction(self):
    z = 0
    PL = 0
    if self.calcul_FS() >= 1.25:
      Fl = 0
    elif self.calcul_FS() < 1.25:
      Fl = 1.25 - self.calcul_FS()
    for z in range(20):
      PL += (10 - 0.5 * z) * Fl
    return PL
  
  def result_FS(self):
   self.calcul_FS()
   print("\nLe facteur de sécurité vis-à-vis de la liquéfaction est de " + str(self.calcul_FS()) + ".")
   if self.potentiel_liquefaction() == 0:
     print("Selon la RPA, il n'y a pas de risque de liquéfaction.")
   elif self.potentiel_liquefaction() > 0 and self.potentiel_liquefaction() < 5:
     print("Selon la RPA, la liquéfaction est peu probable.")
   elif self.potentiel_liquefaction() > 5 and self.potentiel_liquefaction() < 15:
     print("Selon la RPA, la liquéfaction est probable.")
   elif self.potentiel_liquefaction() > 15 and self.potentiel_liquefaction() < 100:
     print("Selon la RPA, la liquéfaction est quasi certaine.")
