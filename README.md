# Choose-your-opponent
Projet TDLOG/MOPSI 

Ce projet propose un nouveau modèle de compétition pour la ligue des champions.
A chaque étape de la phase d'élimination directe, chaque équipe peut choisir son adversaire selon un classement obtenu à la fin de la phase de pool appelé rang faible.

module Python nécessaires: tkinter, functools, PIL, matplotlib, FigureCanvasTkAgg, NavigationToolbar2Tk,
numpy, 
json,
subprocess, 
time,
random, 
bs4 (BeautifulSoup), 
urllib3.


Pour créer l'exécutable C++: http://imagine.enpc.fr/~monasse/Imagine++/
Ensuite suivre les instructions pour créer un exécutable à mettre dans le dossier build/build-Choose-your-opponent-Desktop_Qt_5_15_0_MinGW_32_bit-Release.

Instructions pour utiliser l'application:

Soit vous téléchargez les fichiers json (contenant les résultats exécutés par l'algorithme MOPSI) directement depuis le git.
Soit vous ne les téléchargez pas.

Pour créer ces fichiers (cela dure longtemps (minimum 40minutes pour une version inexacte; en moyenne 10h pour la version exacte sur une année), il faut sélectionner une année puis répondre oui à la question du calul 
des scénarios.

Une fois les fichiers obtenus, vous pouvez parcourir les différentes fenêtres de l'application.
Il y en a 2: la première avec la sélection de l'année et l'affichage des scénarios interactifs de l'année en cours.
Le premier scénario affiché est le plus probable.
Sur la deuxième fénêtre on peut sélectionner le type de probabilité que l'on veut comparer entre le format officiel de la ligue des champions et 
le format proposé

Des légendes sont ou seront indiquées pour expliquer certains points

