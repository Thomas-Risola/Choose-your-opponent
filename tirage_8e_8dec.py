"""
Created on Sat Nov 13 20:06:25 2021

@author: badmax
"""
from random import *
import numpy as np
from time import *
import json
import ParseurMatrix as pm


# tirage 8e de la ligue des champions

# Situation:

# La ligue des champions présente 8 poules de 4 équipes
# De chaque poule sort un gagnant W et un second S qui ont accès au 8e de finale
# Comment en déduire les tirages possibles, il y a 3 règles à respecter:

# 1) Les gagnants W ne peuvent rencontrer que des seconds S
# 2) 2 équipes de la même poule ne peuvent pas se rencontrer en 8e
# 3) 2 équipes d'un même pays ne peuvent se rencontrer en 8e

# les listes de vainqueurs W et S sont composé d'équipes avec les renseignement du code ISO du pays et le numero de
# leur poule W = [[nom_equipe,code_iso,numero_poule],...]=[equipe,...]

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
def remove(winner, W):
    W_restant = []
    for equipe in W:
        if (equipe != winner):
            W_restant.append(equipe)
    return W_restant


# le but de cette fonction est de savoir si avec la liste de winner W et de seconds S il y a une solution possible
def solution_possible(W, S):
    if (len(S) == 0):
        return True
    if (len(S) == 1):
        if (tirage_possible(S[0], W) == []):
            return False
        return True
    else:
        possible = False  # si possible est false, on n'a pas encore trouvé de solution pour le tirage au sort avec
        # ce W et ce S
        for j in range(len(S)):
            if not possible:
                W_possible = tirage_possible(S[j], W)
                if (len(W_possible) == 0):  # pas d'équipes de W que S peut rencontrer, donc pas de solution encore
                    possible = possible or False
                else:
                    for i in range(len(W_possible)):
                        possible = possible or (solution_possible(remove(W_possible[i], W), remove(S[j], S)))
        return possible


# renvoie un tirage admissible avec les équipes dans W et S
def tirage(W, S):
    matchup = []  # retourne des couples equipe W, equipe S correspondant à l'affiche du match
    n = len(S)
    for k in range(n - 1):
        possible = False
        j = 0
        i = 0
        W_possible = []

        while (not (possible)):
            j = randint(0, len(S) - 1)

            W_possible = tirage_possible(S[j], W)
            if (len(W_possible) == 1):
                i = 0
            elif (len(W_possible) == 0):
                return "problème"
            else:
                i = randint(0, len(W_possible) - 1)

            possible = solution_possible(remove(W_possible[i], W), remove(S[j], S))

        matchup.append([W_possible[i], S[j]])

        W = remove(W_possible[i], W)
        S = remove(S[j], S)

    matchup.append([W[0], S[0]])

    return matchup


# affiche la matrice de probabilité
def affichage_proba(N_tirages, W, S):
    t_1 = time()

    P = np.zeros((8, 8))
    for k in range(N_tirages):
        matchup = tirage(W, S)
        for i in range(8):
            indS = indice(matchup[i][1][2])
            indW = indice(matchup[i][0][2])
            P[indS][indW] += 1 / N_tirages
    for i in range(8):
        for j in range(8):
            P[i][j] *= 100
            P[i][j] = round(P[i][j], 2)
    for i in range(8):
        print(P[i])
    t_2 = time()
    print('le temps d execution :', t_2 - t_1)
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
        for i in range(len(key) // 2):
            if key[2 * i] == "A":
                real_key += key[2 * i]
                real_key += key[2 * i + 1]
                break
        for i in range(len(key) // 2):
            if key[2 * i] == "B":
                real_key += key[2 * i]
                real_key += key[2 * i + 1]
                break
        for i in range(len(key) // 2):
            if key[2 * i] == "C":
                real_key += key[2 * i]
                real_key += key[2 * i + 1]
                break
        for i in range(len(key) // 2):
            if key[2 * i] == "D":
                real_key += key[2 * i]
                real_key += key[2 * i + 1]
                break
        for i in range(len(key) // 2):
            if key[2 * i] == "E":
                real_key += key[2 * i]
                real_key += key[2 * i + 1]
                break
        for i in range(len(key) // 2):
            if key[2 * i] == "F":
                real_key += key[2 * i]
                real_key += key[2 * i + 1]
                break
        for i in range(len(key) // 2):
            if key[2 * i] == "G":
                real_key += key[2 * i]
                real_key += key[2 * i + 1]
                break
        for i in range(len(key) // 2):
            if key[2 * i] == "H":
                real_key += key[2 * i]
                real_key += key[2 * i + 1]
                break
        try:
            all_matchup[real_key] += 1 / N_tirages
        except:
            all_matchup[real_key] = 1 / N_tirages
        if (k % (N_tirages / 100) == 0):
            print(k / 10000, "%")

    for key, value in all_matchup.items():
        # 6 car on tire 1 000 000
        all_matchup[key] = round(value, 6)

    t_2 = time()
    print('le temps d execution :', t_2 - t_1)
    return all_matchup


# affiche les confrontations du 8e de finale
def affichage_matchup(W, S):
    matchup = tirage(W, S)
    print('le tirage des 8e de finales a été un succès et les confrontations seront')
    for i in range(len(matchup)):
        print('le match n°', i, ' oppose l équipe de ', matchup[i][0][0], 'à ', matchup[i][1][0])


# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# Maintenant on définit les probas exactes

# on code un algorithme renvoyant toutes les permutations
def permutation(S):
    if (len(S) == 1):
        return [S]
    else:
        perm = []
        for i in range(len(S)):
            for p in permutation(remove(S[i], S)):
                perm.append([S[i]] + p)
        return perm


# renvoie la liste des vainqueurs admissibles par l'équipe second parmi les W restant
def tirages_admissibles(W, S,
                        second):  # la liste S représente les seconds dans l'équipe S et W représente la liste des vainqueurs encore dispo
    liste = tirage_possible(second, W)
    if (len(liste) == 0):
        return []
    else:
        admissible = []
        for i in range(len(liste)):
            if (solution_possible(remove(liste[i], W), remove(second, S))):
                admissible.append(liste[i])
        return admissible


def verif_condition(matchup):  # vérifie que tout les matchs de ce tirage vérifie les conditions de groupe et de pays
    ok = True
    for i in range(len(matchup)):
        ok = ok and (matchup[i][0][1] != matchup[i][1][1]) and (matchup[i][0][2] != matchup[i][1][2])
    return ok


def proba_exacte(W, S):
    n = len(S)
    if (n == 0):
        return 1
    proba_totale = 0
    for i in range(n):
        mi = len(tirages_admissibles(W, S, S[i]))
        if (mi != 0):
            proba_totale += 1 / mi * proba_exacte(remove(W[i], W), remove(S[i], S))
    return proba_totale


def factoriel(n):
    if n == 1:
        return 1
    else:
        return n * factoriel(n - 1)


def proba_exacte_tirage(matchup):
    S = [matchup[i][1] for i in range(len(matchup))]
    W = [matchup[i][0] for i in range(len(matchup))]
    proba = proba_exacte(W, S)
    return proba / factoriel(8)


def match_dispos(S, W):
    if (len(S) == 1):
        return [[[W[0], S[0]]]]
    else:
        dispo = []
        for i in range(len(W)):
            for match in match_dispos(remove(S[0], S), remove(W[i], W)):
                dispo.append([[W[i], S[0]]] + match)
        return dispo


def proba_match(second, winner, W, S):
    if (second[1] == winner[1] or second[2] == winner[2]):
        return 0
    dispo = match_dispos(remove(second, S), remove(winner, W))
    proba = 0
    for i in range(len(dispo)):
        if (verif_condition([[winner, second]] + dispo[i])):
            proba += proba_exacte_tirage([[winner, second]] + dispo[i])
    return proba


def all_matchup_with_S_given(W, S):
    all_matchup = []
    liste_permut_W = permutation(W)
    for i in range(len(liste_permut_W)):
        matchup = []
        for j in range(len(S)):
            matchup.append([liste_permut_W[i][j], S[j]])
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
        compteur += 1
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
            P[i][j] = round(P[i][j], 2)
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
        compteur += 1
        print(compteur / len(all_matchup_admissible) * 100, "%")
        S_c = [matchup[i][1] for i in range(len(matchup))]
        W_c = [matchup[i][0] for i in range(len(matchup))]
        proba_matchup.append(proba_exacte(W_c, S_c) / fact8)

    t_2 = time()
    print('le temps d execution :', t_2 - t_1)
    return all_matchup_admissible, proba_matchup


"""

# on reprend les résultats de la ligue des champions 2020-21 W = [['BAY','DE','A'],['Real', 'ES', 'B'],['ManC','EN',
'C'],['LIV','EN','D'],['CHE','EN','E'],['DOR','DE','F'],['JUV','IT','G'],['PSG','FR','H']] S = [['ATL','ES','A'],
['MGlad','DE','B'],['POR','PT','C'],['ATA','IT','D'],['SEV','ES','E'],['LAZ','IT','F'],['BCN','ES','G'],['LEI','DE',
'H']] 

"""

# Ligue des champions 2021-22
'''
W = [['ManC', 'EN', 'A'], ['LIV', 'EN', 'B'], ['AJX', 'NE', 'C'], ['Real', 'ES', 'D'], ['BAY', 'DE', 'E'],
     ['ManU', 'EN', 'F'], ['LIL', 'FR', 'G'], ['JUV', 'IT', 'H']]
S = [['PSG', 'FR', 'A'], ['ATL', 'ES', 'B'], ['SPO', 'PT', 'C'], ['INT', 'IT', 'D'], ['BEN', 'PT', 'E'],
     ['VIL', 'ES', 'F'], ['SAL', 'AU', 'G'], ['CHE', 'EN', 'H']]

N_tirages = 1000000
all_matchup = affichage_proba_matchup(N_tirages, W, S)

print(all_matchup)
print(len(all_matchup))
'''


# all_matchup, proba_matchup = affichage_proba_matchup_exacte(W, S)

# save_matchup("test", all_matchup, proba_matchup)

class Round_of_16:
    def __init__(self, day, month, year, fileprefix1="json_files/round_of_16_official",
                 fileprefix2="json_files/team_list"):
        filename1 = fileprefix1 + "-" + str(day) + "-" + str(month) + "-" + str(year) + ".txt"
        filename2 = fileprefix2 + "-" + str(day) + "-" + str(month) + "-" + str(year) + ".txt"
        team_list = Round_of_16.get_team_list_from_file(filename2)
        self.W, self.S = Round_of_16.format(team_list)
        N_tirages = 1000000
        all_matchup = affichage_proba_matchup(N_tirages, self.W, self.S)
        list_scenario = Round_of_16.convert_to_feed_algo(all_matchup, team_list)
        Round_of_16.save_scenario(filename1, list_scenario)

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
    def save_scenario(filename, list_scenario):
        file = open(filename, 'w', encoding="utf-8")
        dict_list = ({
            "round_of_16": list_scenario,
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
            if team.group_rank == 1:
                W.append(team_new_format)
            else:
                S.append(team_new_format)
        return W, S

    @staticmethod
    def convert_to_feed_algo(all_matchup, team_list):
        list_scenario = []
        for matchup, value in all_matchup.items():
            scenario = dict()
            X1 = []
            X2 = []
            for i in range(len(matchup) // 2):
                for j in range(len(team_list) // 2):
                    if team_list[j].group[-11] == matchup[2 * i]:
                        team_1 = team_list[j].competition_rank - 1

                for j in range(len(team_list) // 2, len(team_list)):
                    if team_list[j].group[-11] == matchup[2 * i + 1]:
                        team_2 = team_list[j].competition_rank - 1
                X1.append(team_1)
                X2.append(team_2)
            scenario["proba"] = value
            scenario["X1"] = X1
            scenario["X2"] = X2
            scenario["parent"] = 0
            list_scenario.append(scenario)
        return list_scenario


""""

#----------------------------------------
#----------------------------------------2019-20   BEGINING
#----------------------------------------

W0 = [['PSG','FR','A'],['BAY','DE','B'],['ManC','EN','C'],['JUV','IT','D'],['LIV','EN','E'],['BCN','ES','F'],['LEI',
'DE','G'],['VAL','ES','H']] S0 = [['Real', 'ES', 'A'],['TOT','EN','B'],['ATA','IT','C'],['ATL','ES','D'],['NAP','IT',
'E'],['DOR','DE','F'],['LYO','FR','G'],['CHE','EN','H']] 

P_exact19 = affichage_proba_exacte(W0,S0)

#----------------------------------------
#----------------------------------------2019-20   END
#----------------------------------------

"""

'''

#Affichage tableaux

fig = plt.figure(figsize=(10,10)) ax = fig.add_subplot(111, frameon=False, xticks = [], yticks = []) cells = P_simul 
img = plt.imshow(cells, cmap="hot") img.set_visible(False) plt.title('2021-22 Champions League Round of 16 draw 
probabilities in %', fontsize = 18) tb = plt.table(cellText = cells, rowLabels = np.array([S[i][0] for i in range(
8)]), colLabels = np.array([W[i][0] for i in range(8)]), rowColours = plt.cm.BuPu(np.full(8, 0.3)), colColours = 
plt.cm.BuPu(np.full(8, 0.3)), cellLoc = 'center', loc = 'center', cellColours = img.to_rgba(1/(0.0055*cells))) 
tb.auto_set_font_size(False) tb.set_fontsize(18) tb.scale(1, 5) ax.add_table(tb) plt.text(-1.4,7.8,'@julienguyon1977  
  -    Cyril Bertrand    -    Maxim Legendre                   Dec 8, 2021',fontsize = 14.5) plt.show() 

fig = plt.figure(figsize=(10,10)) ax = fig.add_subplot(111, frameon=False, xticks = [], yticks = [] ) cells = P_exact 
img = plt.imshow(cells, cmap="hot") img.set_visible(False) plt.title('2021-22 Champions League Round of 16 draw 
probabilities in %', fontsize = 18) tb = plt.table(cellText = cells, rowLabels = np.array([S[i][0] for i in range(
8)]), colLabels = np.array([W[i][0] for i in range(8)]), rowColours = plt.cm.BuPu(np.full(8, 0.3)), colColours = 
plt.cm.BuPu(np.full(8, 0.3)), cellLoc = 'center', loc = 'center', cellColours = img.to_rgba(1/(0.0055*cells))) 
tb.auto_set_font_size(False) tb.set_fontsize(18) tb.scale(1, 5) ax.add_table(tb) plt.text(-1.4,7.8,'@julienguyon1977  
  -    Cyril Bertrand    -    Maxim Legendre                   Dec 8, 2021',fontsize = 14.5) plt.show() 

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


def get_all_scenario(filename):
    file = open(filename, 'r', encoding="utf-8")
    dict_list = json.load(file)
    all_scenario = dict_list["round_of_16"]
    file.close()
    return all_scenario

def draw(winners):
    set1 = []
    set2 = []
    while len(winners) > 0:
        set1.append(winners[0])
        picked_team = winners[np.random.randint(1, len(winners))]
        set2.append(picked_team)
        index = winners.index(picked_team)
        winners.pop(index)
        winners.pop(0)

    return set1, set2

def play_round(set1, set2, victory_matrix):
    winners = []
    for i in range(len(set1)):
        if np.random.uniform() < victory_matrix[set1[i]][set2[i]]:
            winners.append(set1[i])
        else:
            winners.append(set2[i])
    return winners

def play_tournament(set1, set2, victory_matrix, elo_ranking, proba_scenario, number_monte_carlo):
    proba = dict()
    proba["win"] = [0 for i in range(16)]
    proba["semi"] = [0 for i in range(16)]
    proba["quart"] = [0 for i in range(16)]
    proba["finale"] = [0 for i in range(16)]

    proba["best_finale"] = 0
    proba["best_finale_elo"] = 0
    proba["best_semi"] = 0
    proba["best_semi_elo"] = 0
    proba["best_quart"] = 0
    proba["best_quart_elo"] = 0

    proba["moyenne_rang_finale"] = 0
    proba["moyenne_rang_semi"] = 0
    proba["moyenne_rang_quart"] = 0

    proba["moyenne_rang_finale_elo"] = 0
    proba["moyenne_rang_semi_elo"] = 0
    proba["moyenne_rang_quart_elo"] = 0

    for k in range(number_monte_carlo):
        winners_16th = play_round(set1, set2, victory_matrix)
        number_monte_carlo = number_monte_carlo/proba_scenario
        for i in range(16):
            if i in winners_16th:
                proba["quart"][i] += 1/number_monte_carlo

        for i in range(len(winners_16th)):
            if winners_16th[i] in elo_ranking[:8]:
                if i == 7:
                    proba["best_quart_elo"] += 1/number_monte_carlo
            else:
                break

        for i in range(len(winners_16th)):
            if winners_16th[i] in [0, 1, 2, 3, 4, 5, 6, 7]:
                if i == 7:
                    proba["best_quart"] += 1/number_monte_carlo
            else:
                break

        for i in range(len(winners_16th)):
            proba["moyenne_rang_quart"] += (1+winners_16th[i])/len(winners_16th)/number_monte_carlo
            proba["moyenne_rang_quart_elo"] += (1 + elo_ranking[winners_16th[i]]) / len(winners_16th) / number_monte_carlo

        set1_8th, set2_8th = draw(winners_16th)

        winners_8th = play_round(set1_8th, set2_8th, victory_matrix)

        for i in range(16):
            if i in winners_8th:
                proba["semi"][i] += 1/number_monte_carlo


        for i in range(len(winners_8th)):
            if winners_8th[i] in [0, 1, 2, 3]:
                if i == 3:
                    proba["best_semi"] += 1/number_monte_carlo
            else:
                
                break

        for i in range(len(winners_8th)):
            if winners_8th[i] in elo_ranking[:4]:
                if i == 3:
                    proba["best_semi_elo"] += 1/number_monte_carlo
            else:
                break

        for i in range(len(winners_8th)):
            proba["moyenne_rang_semi"] += (1+winners_8th[i])/len(winners_8th)/number_monte_carlo
            proba["moyenne_rang_semi_elo"] += (1+elo_ranking[winners_8th[i]])/len(winners_8th)/number_monte_carlo

        set1_4th, set2_4th = draw(winners_8th)

        winners_4th = play_round(set1_4th, set2_4th, victory_matrix)

        for i in range(16):
            if i in winners_4th:
                proba["finale"][i] += 1/number_monte_carlo

        for i in range(len(winners_4th)):
            if winners_4th[i] in [0, 1]:
                if i == 1:
                    proba["best_finale"] += 1/number_monte_carlo
            else:
                break

        for i in range(len(winners_4th)):
            if winners_4th[i] in elo_ranking[:2]:
                if i == 1:
                    proba["best_finale_elo"] += 1/number_monte_carlo
            else:
                break

        for i in range(len(winners_4th)):
            proba["moyenne_rang_finale"] += (1+winners_4th[i])/len(winners_4th)/number_monte_carlo
            proba["moyenne_rang_finale_elo"] += (1 + elo_ranking[winners_4th[i]]) / len(winners_4th) / number_monte_carlo

        set1_2th, set2_2th = draw(winners_4th)

        winners_2th = play_round(set1_2th, set2_2th, victory_matrix)
        for i in range(16):
            if i in winners_2th:
                proba["win"][i] += 1/number_monte_carlo

    return proba


def get_proba(victory_matrix, elo_ranking, filename, number_monte_carlo):
    proba = dict()

    proba["win"] = [0 for i in range(16)]
    proba["semi"] = [0 for i in range(16)]
    proba["quart"] = [0 for i in range(16)]
    proba["finale"] = [0 for i in range(16)]

    proba["best_finale"] = 0
    proba["best_finale_elo"] = 0
    proba["best_semi"] = 0
    proba["best_semi_elo"] = 0
    proba["best_quart"] = 0
    proba["best_quart_elo"] = 0

    proba["moyenne_rang_finale"] = 0
    proba["moyenne_rang_semi"] = 0
    proba["moyenne_rang_quart"] = 0

    proba["moyenne_rang_finale_elo"] = 0
    proba["moyenne_rang_semi_elo"] = 0
    proba["moyenne_rang_quart_elo"] = 0

    compteur = 0

    scenario_list = get_all_scenario(filename)
    for scenario in scenario_list:
        print(compteur/len(scenario_list) * 100 , "%")
        compteur += 1
        set1 = scenario["X1"]
        set2 = scenario["X2"]
        proba_scenario = scenario["proba"]
        tournament_proba = play_tournament(set1, set2, victory_matrix, elo_ranking, proba_scenario, number_monte_carlo)
        for i in range(16):
            proba["win"][i] += tournament_proba["win"][i]*number_monte_carlo
            proba["semi"][i] += tournament_proba["semi"][i]*number_monte_carlo
            proba["quart"][i] += tournament_proba["quart"][i]*number_monte_carlo
            proba["finale"][i] += tournament_proba["finale"][i]*number_monte_carlo
        proba["best_finale"] += tournament_proba["best_finale"]*number_monte_carlo
        proba["best_finale_elo"] += tournament_proba["best_finale_elo"]*number_monte_carlo
        proba["best_semi"] += tournament_proba["best_semi"]*number_monte_carlo
        proba["best_semi_elo"] += tournament_proba["best_semi_elo"]*number_monte_carlo
        proba["best_quart"] += tournament_proba["best_quart"]*number_monte_carlo
        proba["best_quart_elo"] += tournament_proba["best_quart_elo"]*number_monte_carlo
        proba["moyenne_rang_finale"] += tournament_proba["moyenne_rang_finale"]*number_monte_carlo
        proba["moyenne_rang_semi"] += tournament_proba["moyenne_rang_semi"]*number_monte_carlo
        proba["moyenne_rang_quart"] += tournament_proba["moyenne_rang_quart"]*number_monte_carlo
        proba["moyenne_rang_finale_elo"] += tournament_proba["moyenne_rang_finale_elo"] * number_monte_carlo
        proba["moyenne_rang_semi_elo"] += tournament_proba["moyenne_rang_semi_elo"] * number_monte_carlo
        proba["moyenne_rang_quart_elo"] += tournament_proba["moyenne_rang_quart_elo"] * number_monte_carlo
    return proba


def save_proba(filename, proba):
    filename_qs_vector = "json_files/official_qs_vector" + filename
    file = open(filename_qs_vector, 'w', encoding="utf-8")
    dict_list = dict()
    dict_list["qs_win"] = proba["win"]
    dict_list["qs_final"] = proba["finale"]
    dict_list["qs_semi"] = proba["semi"]
    dict_list["qs_quart"] = proba["quart"]
    json.dump(dict_list, file, ensure_ascii=False)
    file.close()

    filename_official_best = "json_files/official_best_scenario" + filename
    file = open(filename_official_best, 'w', encoding="utf-8")
    dict_list = dict()
    dict_list["best_final_elo"] = proba["best_finale_elo"]
    dict_list["best_final_weak"] = proba["best_finale"]
    dict_list["best_semi_elo"] = proba["best_semi_elo"]
    dict_list["best_semi_weak"] = proba["best_semi"]
    dict_list["best_quart_elo"] = proba["best_quart_elo"]
    dict_list["best_quart_weak"] = proba["best_quart"]
    dict_list["mean_final"] = proba["moyenne_rang_finale"]
    dict_list["mean_semi"] = proba["moyenne_rang_semi"]
    dict_list["mean_quart"] = proba["moyenne_rang_quart"]
    dict_list["mean_final_elo"] = proba["moyenne_rang_finale_elo"]
    dict_list["mean_semi_elo"] = proba["moyenne_rang_semi_elo"]
    dict_list["mean_quart_elo"] = proba["moyenne_rang_quart_elo"]
    json.dump(dict_list, file, ensure_ascii=False)
    file.close()


def all_in_one_official(day, month, year, victory_matrix, number_monte_carlo):
    date_string = "-" + str(day) + "-" + str(month) + "-" + str(year) + ".txt"
    round_of_16_filename = "json_files/round_of_16_official" + date_string
    elo_ranking = create_elo_ranking(victory_matrix)
    proba = get_proba(victory_matrix, elo_ranking, round_of_16_filename, number_monte_carlo)
    save_proba(date_string, proba)
    qs_filename = "json_files/qs_vector" + date_string
    best_filename = "json_files/best_scenario" + date_string
    get_mean_scenario(qs_filename, best_filename, elo_ranking)

def create_elo_ranking(victory_matrix):
    weak_rank = [i for i in range(16)]
    elo_rank = sorted(weak_rank, key=lambda i: victory_matrix[0][i])
    print(elo_rank)
    return elo_rank

def get_mean_scenario(qs_filename, best_filename, elo):
    file = open(qs_filename, 'r', encoding="utf-8")
    dict_list = json.load(file)
    qs_win = dict_list["qs_win"]
    qs_final = dict_list["qs_final"]
    qs_semi = dict_list["qs_semi"]
    qs_quart = dict_list["qs_quart"]
    file.close()

    mean_final = 0
    mean_semi = 0
    mean_quart = 0
    mean_final_elo = 0
    mean_semi_elo = 0
    mean_quart_elo = 0

    for i in range(16):
        mean_final += qs_final[i]*(i+1)/2
        mean_semi += qs_semi[i]*(i+1)/4
        mean_quart += qs_quart[i]*(i+1)/8
        mean_final_elo += qs_final[elo[i]]*(i+1)/2
        mean_semi_elo += qs_semi[elo[i]]*(i+1)/4
        mean_quart_elo += qs_quart[elo[i]]*(i+1)/8

    file = open(best_filename, 'r', encoding="utf-8")
    dict_list = json.load(file)

    file.close()
    file = open(best_filename, 'w', encoding="utf-8")

    dict_list["mean_final"] = mean_final
    dict_list["mean_semi"] = mean_semi
    dict_list["mean_quart"] = mean_quart
    dict_list["mean_final_elo"] = mean_final_elo
    dict_list["mean_semi_elo"] = mean_semi_elo
    dict_list["mean_quart_elo"] = mean_quart_elo
    json.dump(dict_list, file, ensure_ascii=False)
    file.close()
    return
