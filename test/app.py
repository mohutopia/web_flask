import Liquefaction, Portance, Semelle, Sol





def liquefaction():
  print('''
  Pour calculer le facteur de sécurité vis-à-vis de la liquéfaction des sables, on commence par calculer le CSR, puis le CRR (tout dépend du type d'essai). Ensuite le calcul des corrections MSF et Ks ce qui mènera finalement au calcul du facteur de sécurité et le potentiel de liquéfaction.\n
  ''')
  acceleration_max = float(input("Acceleration max : "))
  contrainte_effective_initiale = float(input("Contrainte effective initiale [KN/m^3] : "))
  contrainte_totale_initiale = float(input("Contrainte totale initiale [KN/m^3] : "))
  profondeur = float(input("Profondeur [m] : "))
  magnitude = float(input("Magnitude : "))
  densite_relative = float(input("Densité relative : "))

  test_method = int(input("""\n
    Pour calcul du CRR, entrez ... 
      0   pour essai CPT
      1   pour essai SPT
      2   pour essai Vs
  """))
  test_class = ''
  if test_method == 0:
    test_method = 'cpt'
    print("\nOn utilise un essai CPT. Entrez les valeurs de qc et fs dans la profondeur " + str(profondeur) + "m choisie.")
    qc = float(input("qc: "))
    fs = float(input("fs: "))
    cpt = Liquefaction.CPT(qc, fs, contrainte_effective_initiale, contrainte_totale_initiale)
    test_class = cpt
    print("Resultat qc1ncs = " + str(cpt.qc1ncs()) + "\n")
  elif test_method == 1:
    test_method = 'spt'
    print("\nOn utilise un essai SPT. Entrez le nombre de coups N et % des fines FC dans la profondeur " + str(profondeur) + "m choisie.")
    N = float(input("N: "))
    FC = float(input("FC: "))
    spt = Liquefaction.SPT(N, contrainte_effective_initiale, FC)
    test_class = spt
    print("Resultat N160cs = " + str(spt.N160cs()) + "\n")
  elif test_method == 2:
    test_method = 'vs'
    print("\nOn utilise la méthode Downhole. Entrez la vitesse sismique Vs et % des fines FC dans la profondeur " + str(profondeur) + "m choisie.")
    vitesse_sismique = float(input("Vs: "))
    FC = float(input("FC: "))
    vs = Liquefaction.Vs(vitesse_sismique, contrainte_effective_initiale, FC)
    test_class = vs
    print("Resultat Vs1 = " + str(vs.Vs1()) + "\n")

  FS = Liquefaction.Facteur_de_Securite(acceleration_max, contrainte_effective_initiale, contrainte_totale_initiale, profondeur, test_method, test_class, magnitude, densite_relative)
  FS.result_FS()





def portance():
  # pour le moment, calculer la pression limite - labo
  print(
    """
  Dans un premier temps, l'ingénieur géotechnicien, cherchera a fonder son ouvrage superficiellement, pour des raisons de coût évidentes. Il devra, alors, se préoccuper en tout premier lieu de la capacité portante de sa fondation, c'est-à-dire vérifier que les couches de sol superficielles peuvent effectivement supporter la charge transmise. Si le résultat des calculs est concluant, notamment s'il n'aboutit pas à une aire de la fondation prohibitive, il doit alors s'assure que son tassement sous les charges de fonctionnement prévues est dans les limites admissibles.
  La Portance et le Tassement sont ainsi les deux éléments fondamentaux qu'il y a lieu de considérer systématiquement lors du calcul des fondations superficielles.
  """
  )

  semelle = Semelle.Semelle(1.5, 8, 1.5)
  cohesion = 0.51
  angle_de_frottement = 10
  poids_volumique = 22

  calcul_portance = Portance.PortanceLaboratoire(cohesion, angle_de_frottement, semelle, poids_volumique, 'undrained')
  print("Pression limite: " + str(calcul_portance.pression_limite()) + " bars.")





def couches_sol():
  # ajouter des couches et calculer la contrainte totale à une profondeur donnée
  sol = Sol.Sol()
  condition = True
  while condition:
    option = input("Nouvelle Couche? y / n : ")
    if option == 'y':
      sol.get_nouvelle_couche()
    if option == 'n':
      condition = False
  sol.print_couches()
  prof = float(input("\nVous voulez calculer la contrainte totale à quelle profondeur? "))
  sol.contraintes_a_un_point(prof)






option = int(input("Calculer : 0 portance ; 1 liquéfaction ; 2 couches ... "))
if option == 0:
  portance()
elif option == 1:
  liquefaction()
elif option == 2:
  couches_sol()
else:
  print("Wrong input. Bye.")
