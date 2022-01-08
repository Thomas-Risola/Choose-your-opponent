"""
Created on Sat Nov 13 20:06:25 2021

@author: badmax
"""
from random import *
import numpy as np
from time import *
import json
import ParseurMatrix as pm
import matplotlib.pyplot as plt
from decimal import *

# tirage 8e de la ligue des champions

# Situation:
    
# La ligue des champions présente 8 poules de 4 équipes
# De chaque poule sort un gagnant W et un second S qui ont accès au 8e de finale
# Comment en déduire les tirages possibles, il y a 3 règles à respecter:

# 1) Les gagnants W ne peuvent rencontrer que des seconds S
# 2) 2 équipes de la même poule ne peuvent pas se rencontrer en 8e
# 3) 2 équipes d'un même pays ne peuvent se rencontrer en 8e
        
# les listes de vainqueurs W et S sont composé d'équipes avec les renseignement du code ISO du pays et le numero de leur poule
# W = [[nom_equipe,code_iso,numero_poule],...]=[equipe,...]

# On définit toujours les tirages possibles à partir d'une équipe de S
# ce programme renvoie les équipes de W que l'équipe equipe de S peut affronter théoriquement en 8e
def tirage_possible(equipe, W):
    W_possible = []
    for winner in W:
        if ((winner[1] != equipe[1]) and (winner[2] != equipe[2])):
            W_possible.append(winner)
    return W_possible

# renvoie des indices pour chaque groupe
def indice(char):
    if char == 'A': return 0
    if char == 'B': return 1
    if char == 'C': return 2
    if char == 'D': return 3
    if char == 'E': return 4
    if char == 'F': return 5
    if char == 'G': return 6
    if char == 'H': return 7

# renvoie une nouvelle liste de W sans l'équipe winner dans W
def remove(winner,W):
    W_restant =[]
    for equipe in W:
        if(equipe != winner): 
            W_restant.append(equipe)
    return W_restant

# le but de cette fonction est de savoir si avec la liste de winner W et de seconds S il y a une solution possible
def solution_possible(W,S):
    if (len(S) == 0):
        return True
    if (len(S) == 1):
        if( tirage_possible(S[0],W) == []):
            return False
        return True
    else:
        possible = False             # si possible est false, on n'a pas encore trouvé de solution pour le tirage au sort avec ce W et ce S
        for j in range(len(S)):
            if not possible:
                W_possible = tirage_possible(S[j],W)
                if (len(W_possible) == 0):          # pas d'équipes de W que S peut rencontrer, donc pas de solution encore
                    possible = possible or False
                else:
                    for i in range(len(W_possible)):
                        possible = possible or (solution_possible(remove(W_possible[i],W),remove(S[j],S)))
        return possible
    
# renvoie un tirage admissible avec les équipes dans W et S
def tirage(W,S):
    matchup= []     # retourne des couples equipe W, equipe S correspondant à l'affiche du match
    n = len(S)
    for k in range(n-1):
        possible = False
        j=0
        i=0
        W_possible = []
        
        while (not(possible)):
            j = randint(0,len(S)-1)

            W_possible = tirage_possible(S[j], W)
            if(len(W_possible)==1): i=0
            elif(len(W_possible)==0): return "problème"
            else : i = randint(0,len(W_possible)-1)
            
            possible = solution_possible(remove(W_possible[i], W),remove(S[j], S))
            
        matchup.append([W_possible[i],S[j]])
        
        W = remove(W_possible[i], W)
        S = remove(S[j], S)
        
    matchup.append([W[0],S[0]])
    
    return matchup

# affiche la matrice de probabilité
def affichage_proba(N_tirages,W,S):
    
    t_1 = time()
    
    P = np.zeros((8,8))       
    for k in range(N_tirages):
        matchup = tirage(W,S)
        for i in range(8):
            indS = indice(matchup[i][1][2])
            indW = indice(matchup[i][0][2])
            P[indS][indW] += 1/N_tirages
    for i in range(8):
        for j in range(8):
            P[i][j] *= 100
            P[i][j] = round(P[i][j],2)
    for i in range(8):
        print(P[i])
    t_2 = time()
    print('le temps d execution :', t_2-t_1)
    return P


def affichage_proba_matchup(N_tirages, W, S):
    t_1 = time()

    all_matchup = dict()
    for k in range(N_tirages):
        matchup = tirage(W, S)
        key = ""
        real_key = ""
        for i in range(len(matchup)):
            key += matchup[i][0][2]
            key += matchup[i][1][2]
        for i in range(len(key)//2):
            if key[2*i] == "A":
                real_key += key[2*i]
                real_key += key[2*i+1]
                break
        for i in range(len(key)//2):
            if key[2*i] == "B":
                real_key += key[2 * i]
                real_key += key[2 * i + 1]
                break
        for i in range(len(key)//2):
            if key[2*i] == "C":
                real_key += key[2 * i]
                real_key += key[2 * i + 1]
                break
        for i in range(len(key)//2):
            if key[2*i] == "D":
                real_key += key[2 * i]
                real_key += key[2 * i + 1]
                break
        for i in range(len(key)//2):
            if key[2*i] == "E":
                real_key += key[2 * i]
                real_key += key[2 * i + 1]
                break
        for i in range(len(key)//2):
            if key[2*i] == "F":
                real_key += key[2 * i]
                real_key += key[2 * i + 1]
                break
        for i in range(len(key)//2):
            if key[2*i] == "G":
                real_key += key[2 * i]
                real_key += key[2 * i + 1]
                break
        for i in range(len(key)//2):
            if key[2*i] == "H":
                real_key += key[2 * i]
                real_key += key[2 * i + 1]
                break
        try:
            all_matchup[real_key] += 1/N_tirages
        except:
            all_matchup[real_key] = 1/N_tirages
        if(k % (N_tirages/100) == 0):
            print(k/10000, "%")

    for key, value in all_matchup.items():
        # 6 car on tire 1 000 000
        all_matchup[key] = round(value, 6)



    t_2 = time()
    print('le temps d execution :', t_2 - t_1)
    return all_matchup


# affiche les confrontations du 8e de finale
def affichage_matchup(W,S):
    matchup = tirage(W,S)
    print('le tirage des 8e de finales a été un succès et les confrontations seront')
    for i in range(len(matchup)):
        print('le match n°', i, ' oppose l équipe de ', matchup[i][0][0], 'à ', matchup[i][1][0])

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# Maintenant on définit les probas exactes

#on code un algorithme renvoyant toutes les permutations
def permutation(S):
    if (len(S)==1) :
        return [S]
    else:
        perm = []
        for i in range(len(S)):
            for p in permutation(remove(S[i],S)):
                perm.append([S[i]] + p)
        return perm

# renvoie la liste des vainqueurs admissibles par l'équipe second parmi les W restant
def tirages_admissibles(W,S,second): # la liste S représente les seconds dans l'équipe S et W représente la liste des vainqueurs encore dispo
    liste = tirage_possible(second, W)
    if (len(liste)==0): 
        return []
    else:
        admissible =[]
        for i in range(len(liste)):
            if (solution_possible(remove(liste[i],W), remove(second,S))):
                admissible.append(liste[i])
        return admissible

def verif_condition(matchup):     # vérifie que tout les matchs de ce tirage vérifie les conditions de groupe et de pays
    ok = True
    for i in range(len(matchup)):
        ok = ok and (matchup[i][0][1]!=matchup[i][1][1]) and (matchup[i][0][2]!=matchup[i][1][2])
    return ok

def proba_exacte(W,S):
    n = len(S)
    if (n==0):
        return 1
    proba_totale =0
    for i in range(n):
        mi = len(tirages_admissibles(W, S, S[i]))
        if (mi!=0):
            proba_totale += 1/mi*proba_exacte(remove(W[i], W),remove(S[i],S))
    return proba_totale


def factoriel(n):
    if n==1: 
        return 1
    else:
        return n*factoriel(n-1)

def proba_exacte_tirage(matchup):
    S =[matchup[i][1] for i in range(len(matchup))]
    W = [matchup[i][0] for i in range(len(matchup))]
    proba = proba_exacte(W, S)
    return proba/factoriel(8)


def match_dispos(S,W):
    if (len(S)==1):
        return [[[W[0],S[0]]]]
    else:
        dispo=[]
        for i in range(len(W)):
            for match in match_dispos(remove(S[0],S),remove(W[i],W)):
                dispo.append([[W[i],S[0]]]+match)
        return dispo


def proba_match(second,winner,W,S):
    if (second[1]==winner[1] or second[2]==winner[2]):
        return 0
    dispo = match_dispos(remove(second,S),remove(winner,W))
    proba=0
    for i in range(len(dispo)):
        if (verif_condition([[winner,second]]+dispo[i])):
            proba += proba_exacte_tirage([[winner,second]]+dispo[i])
    return proba


def all_matchup_with_S_given(W, S):
    all_matchup = []
    liste_permut_W = permutation(W)
    for i in range(len(liste_permut_W)):
        matchup = []
        for j in range(len(S)):
            matchup.append([ liste_permut_W[i][j], S[j] ])
        all_matchup.append(matchup)
    return all_matchup

def all_admissible_matchup_with_S_given(W, S):
    all_admissible_matchup = []
    all_matchup = all_matchup_with_S_given(W, S)
    for matchup in all_matchup:
        if verif_condition(matchup):
            all_admissible_matchup.append(matchup)
    return all_admissible_matchup


# affiche la matrice de probabilités exactes
def affichage_proba_exacte(W, S):
    t_1 = time()

    all_matchup_admissible = all_admissible_matchup_with_S_given(W, S)

    P = np.zeros((8, 8))
    fact8 = factoriel(8)
    compteur = 0

    for matchup in all_matchup_admissible:
        compteur +=1
        print(compteur)
        S_c = [matchup[i][1] for i in range(len(matchup))]
        W_c = [matchup[i][0] for i in range(len(matchup))]
        proba_matchup = proba_exacte(W_c, S_c) / fact8
        for i in range(8):
            indS = indice(matchup[i][1][2])
            indW = indice(matchup[i][0][2])
            P[indS][indW] += proba_matchup
    for i in range(8):
        for j in range(8):
            P[i][j] *= 100
            P[i][j] = round(P[i][j],2)
    for i in range(8):
        print(P[i])

    t_2 = time()
    print('le temps d execution :', t_2 - t_1)
    return P

# affiche la matrice de probabilités exactes
def affichage_proba_matchup_exacte(W, S):
    t_1 = time()

    all_matchup_admissible = all_admissible_matchup_with_S_given(W, S)

    P = np.zeros((8, 8))
    fact8 = factoriel(8)
    compteur = 0

    proba_matchup = []
    print(len(all_matchup_admissible))
    for matchup in all_matchup_admissible:
        compteur +=1
        print(compteur/len(all_matchup_admissible)*100, "%")
        S_c = [matchup[i][1] for i in range(len(matchup))]
        W_c = [matchup[i][0] for i in range(len(matchup))]
        proba_matchup.append(proba_exacte(W_c, S_c) / fact8)

    t_2 = time()
    print('le temps d execution :', t_2 - t_1)
    return all_matchup_admissible, proba_matchup


"""

# on reprend les résultats de la ligue des champions 2020-21
W = [['BAY','DE','A'],['Real', 'ES', 'B'],['ManC','EN','C'],['LIV','EN','D'],['CHE','EN','E'],['DOR','DE','F'],['JUV','IT','G'],['PSG','FR','H']]
S = [['ATL','ES','A'],['MGlad','DE','B'],['POR','PT','C'],['ATA','IT','D'],['SEV','ES','E'],['LAZ','IT','F'],['BCN','ES','G'],['LEI','DE','H']]

"""


#Ligue des champions 2021-22
W = [['ManC','EN','A'],['LIV', 'EN', 'B'],['AJX','NE','C'],['Real','ES','D'],['BAY','DE','E'],['ManU','EN','F'],['LIL','FR','G'],['JUV','IT','H']]
S = [['PSG','FR','A'],['ATL','ES','B'],['SPO','PT','C'],['INT','IT','D'],['BEN','PT','E'],['VIL','ES','F'],['SAL','AU','G'],['CHE','EN','H']]

N_tirages = 1000000
all_matchup = affichage_proba_matchup(N_tirages, W, S)

print(all_matchup)
print(len(all_matchup))

#all_matchup, proba_matchup = affichage_proba_matchup_exacte(W, S)

#save_matchup("test", all_matchup, proba_matchup)

class Round_of_16:
    def __init__(self, day, month, year, fileprefix1="json_files/qs_vector", fileprefix2="json_files/team_list"):
        filename1 = fileprefix1 + "-" + str(day) + "-" + str(month) + "-" + str(year) + ".txt"
        filename2 = fileprefix2 + "-" + str(day) + "-" + str(month) + "-" + str(year) + ".txt"
        team_list = Round_of_16.get_team_list_from_file(filename1)
        self.W, self.S = Round_of_16.format(team_list)
        N_tirages = 1000000
        all_matchup = affichage_proba_matchup(N_tirages, self.W, self.S)




    @staticmethod
    def get_team_list_from_file(filename):
        file = open(filename, 'r', encoding="utf-8")
        dict_list = json.load(file)
        team_list = []
        for dd in dict_list:
            team_list.append(pm.Team(
                dd["name"],
                dd["elo"],
                dd["nationality"],
                dd["group"],
                dd["group_rank"],
                dd["point"],
                dd["goal_difference"],
                dd["goal_for"],
                dd["competition_rank"]))
        file.close()
        return team_list

    @staticmethod
    def save_matchup(filename, all_matchup, proba_matchup):
        file = open(filename, 'w', encoding="utf-8")
        dict_list = ({
            "all_matchup": all_matchup,
            "probability": proba_matchup,
        })
        json.dump(dict_list, file, ensure_ascii=False)
        file.close()

    @staticmethod
    def format(team_list):
        W = []
        S = []
        for team in team_list:
            team_new_format = []
            team_new_format.append(team.name)
            team_new_format.append(team.nationality)
            team_new_format.append(team.group[-11])
            if (team_list.group_rank == 1):
                W.append(team_new_format)
            else:
                S.append(team_new_format)
        return W, S

    @staticmethod
    def convert_to_feed_algo(all_matchup, team_list):
        for matchup, value in all_matchup.items():
            scenario = dict()
            scenario["X1"] = 1
            scenario["X2"] = 1


""""

#----------------------------------------
#----------------------------------------2019-20   BEGINING
#----------------------------------------

W0 = [['PSG','FR','A'],['BAY','DE','B'],['ManC','EN','C'],['JUV','IT','D'],['LIV','EN','E'],['BCN','ES','F'],['LEI','DE','G'],['VAL','ES','H']]
S0 = [['Real', 'ES', 'A'],['TOT','EN','B'],['ATA','IT','C'],['ATL','ES','D'],['NAP','IT','E'],['DOR','DE','F'],['LYO','FR','G'],['CHE','EN','H']]

P_exact19 = affichage_proba_exacte(W0,S0)

#----------------------------------------
#----------------------------------------2019-20   END
#----------------------------------------

"""

'''

#Affichage tableaux

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111, frameon=False, xticks = [], yticks = [])
cells = P_simul
img = plt.imshow(cells, cmap="hot")
img.set_visible(False)
plt.title('2021-22 Champions League Round of 16 draw probabilities in %', fontsize = 18)
tb = plt.table(cellText = cells,
    rowLabels = np.array([S[i][0] for i in range(8)]),
    colLabels = np.array([W[i][0] for i in range(8)]),
    rowColours = plt.cm.BuPu(np.full(8, 0.3)),
    colColours = plt.cm.BuPu(np.full(8, 0.3)),
    cellLoc = 'center',
    loc = 'center',
    cellColours = img.to_rgba(1/(0.0055*cells)))
tb.auto_set_font_size(False)
tb.set_fontsize(18)
tb.scale(1, 5)
ax.add_table(tb)
plt.text(-1.4,7.8,'@julienguyon1977    -    Cyril Bertrand    -    Maxim Legendre                   Dec 8, 2021',fontsize = 14.5)
plt.show()

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111, frameon=False, xticks = [], yticks = [] )
cells = P_exact
img = plt.imshow(cells, cmap="hot")
img.set_visible(False)
plt.title('2021-22 Champions League Round of 16 draw probabilities in %', fontsize = 18)
tb = plt.table(cellText = cells,
    rowLabels = np.array([S[i][0] for i in range(8)]),
    colLabels = np.array([W[i][0] for i in range(8)]),
    rowColours = plt.cm.BuPu(np.full(8, 0.3)),
    colColours = plt.cm.BuPu(np.full(8, 0.3)),
    cellLoc = 'center',
    loc = 'center',
    cellColours = img.to_rgba(1/(0.0055*cells)))
tb.auto_set_font_size(False)
tb.set_fontsize(18)
tb.scale(1, 5)
ax.add_table(tb)
plt.text(-1.4,7.8,'@julienguyon1977    -    Cyril Bertrand    -    Maxim Legendre                   Dec 8, 2021',fontsize = 14.5)
plt.show()

'''

""""

#----------------------------------------
#----------------------------------------2019-20   BEGINING 
#----------------------------------------

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111, frameon=False, xticks = [], yticks = [])
cells = P_exact19
img = plt.imshow(cells, cmap="hot")
img.set_visible(False)
plt.title('2019-20 Champions League Round of 16 draw probabilities in %', fontsize = 16)
tb = plt.table(cellText = cells,
    rowLabels = np.array([S0[i][0] for i in range(8)]),
    colLabels = np.array([W0[i][0] for i in range(8)]),
    rowColours = plt.cm.BuPu(np.full(8, 0.3)),
    colColours = plt.cm.BuPu(np.full(8, 0.3)),
    cellLoc = 'center',
    loc = 'center',
    cellColours = img.to_rgba(1/(0.0055*cells)))
tb.auto_set_font_size(False)
tb.set_fontsize(18)
tb.scale(1, 5)
ax.add_table(tb)
plt.show()

#----------------------------------------
#----------------------------------------2019-20   END
#----------------------------------------

"""


