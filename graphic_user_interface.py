import tkinter as tk
from tkinter import messagebox
from functools import partial
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import json
import shlex, subprocess

import ParseurMatrix as pm
import get_result as gr
import tirage_8e_8dec as tir

global number_of_open_window
number_of_open_window = 0


class SimpleTable(tk.Frame):
    def __init__(self, parent, rows=10, columns=2, with_button=False, nb_team_round=16, scenario_list=[], team_list=[],
                 year=2021):
        # use black background so it "peeks through" to
        # form grid lines
        tk.Frame.__init__(self, parent, background="black")
        self.parent = parent
        self._widgets = []
        self.nb_team_round = nb_team_round
        self.scenario_list = scenario_list
        self.team_list = team_list
        self.year = year
        for row in range(rows):
            current_row = []
            for column in range(columns):
                if not with_button or nb_team_round < 2:
                    label = tk.Label(self, text="%s/%s" % (row, column),
                                     borderwidth=0, width=10)
                    label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                else:
                    label = tk.Button(self, text="%s/%s" % (row, column),
                                      borderwidth=0, width=10)  # command=def_function
                    label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

    def set(self, row, column, value1, value2=None, team_1=None, team_2=None, victory_matrix=None, winning_teams=[]):
        def create_4th(winning_teams, scenario_list):
            games_4th = SimpleTable(self.parent, rows=13, columns=1, with_button=True, nb_team_round=8,
                                    scenario_list=self.scenario_list, team_list=self.team_list,
                                    year=self.year)
            games_4th.set(0, 0, "Quarts")
            X1, X2 = search_and_fill_scenario(winning_teams, scenario_list)

            new_winning_teams = []
            for i in range(len(X1)):
                if victory_matrix[X1[i]][X2[i]] >= 0.5:
                    new_winning_teams.append(X1[i])
                else:
                    new_winning_teams.append(X2[i])

            for i in range(len(X1)):
                games_4th.set(3 * i + 1, 0, "")
                games_4th.set(3 * i + 2, 0, self.team_list[X1[i]].name, self.team_list[X2[i]].name,
                              self.team_list[X1[i]].competition_rank - 1,
                              self.team_list[X2[i]].competition_rank - 1, victory_matrix, new_winning_teams)

            games_4th.grid(row=5, column=2)
            return X1, X2

        def create_semi(winning_teams, scenario_list):
            games_semi = SimpleTable(self.parent, rows=7, columns=1, with_button=True, nb_team_round=4,
                                     scenario_list=self.scenario_list, team_list=self.team_list,
                                     year=self.year)
            games_semi.set(0, 0, "Demies")

            X1, X2 = search_and_fill_scenario(winning_teams, scenario_list)

            new_winning_teams = []
            for i in range(len(X1)):
                if victory_matrix[X1[i]][X2[i]] >= 0.5:
                    new_winning_teams.append(X1[i])
                else:
                    new_winning_teams.append(X2[i])

            for i in range(len(X1)):
                games_semi.set(3 * i + 1, 0, "")
                games_semi.set(3 * i + 2, 0, self.team_list[X1[i]].name, self.team_list[X2[i]].name,
                               self.team_list[X1[i]].competition_rank - 1,
                               self.team_list[X2[i]].competition_rank - 1, victory_matrix, new_winning_teams)

            games_semi.grid(row=5, column=3)
            return X1, X2

        def create_final(winning_teams, scenario_list):
            games_final = SimpleTable(self.parent, rows=4, columns=1, with_button=True, nb_team_round=2,
                                      scenario_list=self.scenario_list, team_list=self.team_list,
                                      year=self.year)
            games_final.set(0, 0, "Finale")

            X1, X2 = search_and_fill_scenario(winning_teams, scenario_list)

            new_winning_teams = []
            for i in range(len(X1)):
                if victory_matrix[X1[i]][X2[i]] >= 0.5:
                    new_winning_teams.append(X1[i])
                else:
                    new_winning_teams.append(X2[i])

            for i in range(len(X1)):
                games_final.set(3 * i + 1, 0, "")
                games_final.set(3 * i + 2, 0, self.team_list[X1[i]].name, self.team_list[X2[i]].name,
                                self.team_list[X1[i]].competition_rank - 1,
                                self.team_list[X2[i]].competition_rank - 1, victory_matrix, new_winning_teams)

            games_final.grid(row=5, column=4)

        def best_team_command(winning_teams, scenario_list, nb_team_round, best_team, bad_team, up):
            if up:
                widget = self._widgets[row + 1][column]
                widget.configure(
                    bg='#ffb3fe',
                    fg='black',
                    state=tk.NORMAL)
                widget = self._widgets[row][column]
                widget.configure(
                    bg='light green',
                    fg='black',
                    state=tk.DISABLED)
            else:
                widget = self._widgets[row][column]
                widget.configure(
                    bg='#ffb3fe',
                    fg='black',
                    state=tk.NORMAL)
                widget = self._widgets[row + 1][column]
                widget.configure(
                    bg='light green',
                    fg='black',
                    state=tk.DISABLED)
            bad_team_index = winning_teams.index(bad_team)
            winning_teams[bad_team_index] = best_team

            if nb_team_round == 16:
                X1, X2 = create_4th(winning_teams, scenario_list)
                winning_teams = []
                for i in range(len(X1)):
                    if victory_matrix[X1[i]][X2[i]] >= 0.5:
                        winning_teams.append(X1[i])
                    else:
                        winning_teams.append(X2[i])
                X1, X2 = create_semi(winning_teams, scenario_list)
                winning_teams = []
                for i in range(len(X1)):
                    if victory_matrix[X1[i]][X2[i]] >= 0.5:
                        winning_teams.append(X1[i])
                    else:
                        winning_teams.append(X2[i])
                create_final(winning_teams, scenario_list)
            elif nb_team_round == 8:
                X1, X2 = create_semi(winning_teams, scenario_list)
                winning_teams = []
                for i in range(len(X1)):
                    if victory_matrix[X1[i]][X2[i]] >= 0.5:
                        winning_teams.append(X1[i])
                    else:
                        winning_teams.append(X2[i])
                create_final(winning_teams, scenario_list)
            elif nb_team_round == 4:
                create_final(winning_teams, scenario_list)

        def bad_team_command(winning_teams, scenario_list, nb_team_round, best_team, bad_team, up):
            if up:
                widget = self._widgets[row][column]
                widget.configure(
                    bg='#ffb3fe',
                    fg='black',
                    state=tk.NORMAL)
                widget = self._widgets[row + 1][column]
                widget.configure(
                    bg='light green',
                    fg='black',
                    state=tk.DISABLED)
            else:
                widget = self._widgets[row + 1][column]
                widget.configure(
                    bg='#ffb3fe',
                    fg='black',
                    state=tk.NORMAL)
                widget = self._widgets[row][column]
                widget.configure(
                    bg='light green',
                    fg='black',
                    state=tk.DISABLED)

            best_team_index = winning_teams.index(best_team)
            winning_teams[best_team_index] = bad_team

            if nb_team_round == 16:
                X1, X2 = create_4th(winning_teams, scenario_list)
                winning_teams = []
                for i in range(len(X1)):
                    if victory_matrix[X1[i]][X2[i]] >= 0.5:
                        winning_teams.append(X1[i])
                    else:
                        winning_teams.append(X2[i])
                X1, X2 = create_semi(winning_teams, scenario_list)
                winning_teams = []
                for i in range(len(X1)):
                    if victory_matrix[X1[i]][X2[i]] >= 0.5:
                        winning_teams.append(X1[i])
                    else:
                        winning_teams.append(X2[i])
                create_final(winning_teams, scenario_list)
            elif nb_team_round == 8:
                X1, X2 = create_semi(winning_teams, scenario_list)
                winning_teams = []
                for i in range(len(X1)):
                    if victory_matrix[X1[i]][X2[i]] >= 0.5:
                        winning_teams.append(X1[i])
                    else:
                        winning_teams.append(X2[i])
                create_final(winning_teams, scenario_list)
            elif nb_team_round == 4:
                create_final(winning_teams, scenario_list)

        # winning_teams sorted
        def search_and_fill_scenario(winning_teams, scenario_list):
            sorted_winning_teams = sorted(winning_teams)
            if len(winning_teams) == 8:
                round_index = 2
            if len(winning_teams) == 4:
                round_index = 1
            if len(winning_teams) == 2:
                round_index = 0
            for scenario in scenario_list[round_index]:
                number_of_good_teams = 0
                for team_id in winning_teams:
                    if team_id in scenario["X1"] or team_id in scenario["X2"]:
                        number_of_good_teams += 1
                    if number_of_good_teams == len(winning_teams):
                        return scenario["X1"], scenario["X2"]

        if value2 is None:
            widget = self._widgets[row][column]
            widget.configure(text=value1)
            if value1 in ["8èmes", "Quarts", "Demies", "Finale"]:
                widget.configure(state="disabled", bg='light blue', fg='white')
        else:
            if victory_matrix[team_1][team_2] >= 0.5:
                up = True
                best_team = team_1
                bad_team = team_2
                widget = self._widgets[row][column]
                widget.configure(text=value1, command=partial(best_team_command, winning_teams, self.scenario_list,
                                                              self.nb_team_round, best_team, bad_team, up),
                                 bg='light green',
                                 fg='black',
                                 state=tk.DISABLED)
                widget = self._widgets[row + 1][column]
                widget.configure(text=value2, command=partial(bad_team_command, winning_teams, self.scenario_list,
                                                              self.nb_team_round, best_team, bad_team, up),
                                 bg='#ffb3fe',
                                 fg='black',
                                 state=tk.NORMAL)
            else:
                up = False
                best_team = team_2
                bad_team = team_1
                widget = self._widgets[row + 1][column]
                widget.configure(text=value2, command=partial(best_team_command, winning_teams, self.scenario_list,
                                                              self.nb_team_round, best_team, bad_team, up),
                                 bg='light green',
                                 fg='black',
                                 state=tk.DISABLED)
                widget = self._widgets[row][column]
                widget.configure(text=value1, command=partial(bad_team_command, winning_teams, self.scenario_list,
                                                              self.nb_team_round, best_team, bad_team, up),
                                 bg='#ffb3fe',
                                 fg='black', state=tk.NORMAL)


class NewWindow:
    def __init__(self, parent, year_clicked, team_list_year, qs_year, official_qs_year,
                 best_scenario_year, official_best_scenario_year):

        proba_window = tk.Toplevel(parent)
        proba_window.title("Affichage des métriques")
        # proba_window.iconbitmap()
        proba_window.geometry("1300x600")
        self.proba_window = proba_window

        metric_options = [
            "Probabilité d'atteindre une étape (rang faible)",
            "probabilité de victoire (rang faible)",
            "Probabilité d'atteindre une étape (rang elo)",
            "probabilité de victoire (rang elo)",
        ]

        metric_clicked = tk.StringVar()
        metric_clicked.set(metric_options[0])

        drop = tk.OptionMenu(proba_window, metric_clicked, *metric_options)
        drop.grid(row=0, column=0)

        # leave button
        def leave():
            self.proba_window.destroy()  # Détruit la fenêtre secondaire
            parent.deiconify()  # Remet en avant-plan
            global number_of_open_window
            number_of_open_window -= 1

        leave_frame = tk.Frame(proba_window)
        leave_frame.grid(row=0, column=1)
        leave_button = tk.Button(leave_frame, text='Quitter', command=leave)
        leave_button.grid(row=0, column=0)

        # same thing as the leave button but it's the windows cross
        def on_closing():
            global number_of_open_window
            number_of_open_window -= 1
            proba_window.destroy()
            parent.deiconify()

        proba_window.wm_protocol("WM_DELETE_WINDOW", on_closing)

        def show_option(*args):
            global canvas
            plt.close()
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
            fig.suptitle('Comparaison des formats')
            canvas = FigureCanvasTkAgg(fig, proba_window)
            for item in canvas.get_tk_widget().find_all():
                canvas.get_tk_widget().delete(item)

            qs_win, qs_final, qs_semi, qs_quart = qs_year[year_clicked]
            official_qs_win, official_qs_final, official_qs_semi, official_qs_quart = official_qs_year[year_clicked]

            team_list = team_list_year[year_clicked]

            if metric_clicked.get() == metric_options[0]:

                rank = [i for i in range(1, len(qs_win) + 1)]

                ax1.scatter(rank, qs_win, label="victoire", color="r")
                ax1.scatter(rank, qs_final, label="finale", color="g")
                ax1.scatter(rank, qs_semi, label="demi-finale", color="b")
                ax1.scatter(rank, qs_quart, label="quart de finale", color="y")

                ax1.set_xlim(0, 17)
                ax1.set_ylim(0, 1)
                ax1.set_xlabel("rang faible")
                ax1.set_ylabel("probabilité")

                ax1.set_title("format: Choose your opponent")
                ax1.legend()

                ax2.scatter(rank, official_qs_win, label="victoire", color="r")
                ax2.scatter(rank, official_qs_final, label="finale", color="g")
                ax2.scatter(rank, official_qs_semi, label="demi-finale", color="b")
                ax2.scatter(rank, official_qs_quart, label="quart de finale", color="y")
                ax2.legend()

                ax2.set_xlim(0, 17)
                ax2.set_ylim(0, 1)
                ax2.set_xlabel("rang faible")
                ax2.set_ylabel("probabilité")

                ax2.set_title("format: UEFA officiel")

                canvas = FigureCanvasTkAgg(fig, master=proba_window)
                canvas.draw()

                canvas.get_tk_widget().grid(row=25, column=0)

                toolbar_frame = tk.Frame(proba_window)
                toolbar_frame.grid(row=500, column=0)
                toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
                toolbar.update()
                canvas.get_tk_widget().grid(row=5, column=0)

                ranking_table = SimpleTable(proba_window, rows=17, columns=2)

                ranking_table.set(0, 0, "rang faible")
                ranking_table.set(0, 1, "équipe")
                for i in range(len(team_list)):
                    ranking_table.set(i + 1, 0, team_list[i].competition_rank)
                    ranking_table.set(i + 1, 1, team_list[i].name)
                ranking_table.grid(row=5, column=1)

            if metric_clicked.get() == metric_options[1]:

                rank = [i for i in range(1, len(qs_win) + 1)]

                ax1.scatter(rank, qs_win, label="victoire")

                ax1.set_xlim(0, 17)
                ax1.set_ylim(0, 1)
                ax1.set_xlabel("rang faible")
                ax1.set_ylabel("probabilité")

                ax1.set_title("format: Choose your opponent")
                ax1.legend()

                ax2.scatter(rank, official_qs_win, label="victoire")

                ax2.set_xlim(0, 17)
                ax2.set_ylim(0, 1)
                ax2.set_xlabel("rang faible")
                ax2.set_ylabel("probabilité")

                ax2.set_title("format: UEFA officiel")
                ax2.legend()

                canvas = FigureCanvasTkAgg(fig, master=proba_window)
                canvas.draw()

                canvas.get_tk_widget().grid(row=25, column=0)

                toolbar_frame = tk.Frame(proba_window)
                toolbar_frame.grid(row=500, column=0)
                toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
                toolbar.update()
                canvas.get_tk_widget().grid(row=5, column=0)

                ranking_table = SimpleTable(proba_window, rows=17, columns=2)

                ranking_table.set(0, 0, "rang faible")
                ranking_table.set(0, 1, "équipe")
                for i in range(len(team_list)):
                    ranking_table.set(i + 1, 0, team_list[i].competition_rank)
                    ranking_table.set(i + 1, 1, team_list[i].name)
                ranking_table.grid(row=5, column=1)

            if metric_clicked.get() == metric_options[2]:

                rank = [17 - i for i in range(1, len(qs_win) + 1)]

                qs_win_ordered = [y for _, y in sorted(zip(team_list, qs_win), key=lambda x: x[0].elo)]

                qs_final_ordered = [y for _, y in sorted(zip(team_list, qs_final), key=lambda x: x[0].elo)]

                qs_semi_ordered = [y for _, y in sorted(zip(team_list, qs_semi), key=lambda x: x[0].elo)]

                qs_quart_ordered = [y for _, y in sorted(zip(team_list, qs_quart), key=lambda x: x[0].elo)]

                official_qs_win_ordered = [y for _, y in
                                           sorted(zip(team_list, official_qs_win), key=lambda x: x[0].elo)]

                official_qs_final_ordered = [y for _, y in
                                             sorted(zip(team_list, official_qs_final), key=lambda x: x[0].elo)]

                official_qs_semi_ordered = [y for _, y in
                                            sorted(zip(team_list, official_qs_semi), key=lambda x: x[0].elo)]

                official_qs_quart_ordered = [y for _, y in
                                             sorted(zip(team_list, official_qs_quart), key=lambda x: x[0].elo)]

                team_list_ordered = sorted(team_list, key=lambda team: team.elo)

                ax1.scatter(rank, qs_win_ordered, label="victoire", color="r")
                ax1.scatter(rank, qs_final_ordered, label="finale", color="g")
                ax1.scatter(rank, qs_semi_ordered, label="demi-finale", color="b")
                ax1.scatter(rank, qs_quart_ordered, label="quart de finale", color="y")

                ax1.set_xlim(0, 17)
                ax1.set_ylim(0, 1)
                ax1.set_xlabel("rang faible")
                ax1.set_ylabel("probabilité")

                ax1.set_title("format: Choose your opponent")
                ax1.legend()

                ax2.scatter(rank, official_qs_win_ordered, label="victoire", color="r")
                ax2.scatter(rank, official_qs_final_ordered, label="finale", color="g")
                ax2.scatter(rank, official_qs_semi_ordered, label="demi-finale", color="b")
                ax2.scatter(rank, official_qs_quart_ordered, label="quart de finale", color="y")
                ax2.legend()

                ax2.set_xlim(0, 17)
                ax2.set_ylim(0, 1)
                ax2.set_xlabel("rang faible")
                ax2.set_ylabel("probabilité")

                ax2.set_title("format: UEFA officiel")
                ax2.legend()

                canvas = FigureCanvasTkAgg(fig, master=proba_window)
                canvas.draw()

                canvas.get_tk_widget().grid(row=25, column=0)

                toolbar_frame = tk.Frame(proba_window)
                toolbar_frame.grid(row=500, column=0)
                toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
                toolbar.update()
                canvas.get_tk_widget().grid(row=5, column=0)

                ranking_table = SimpleTable(proba_window, rows=17, columns=2)

                ranking_table.set(0, 0, "rang elo")
                ranking_table.set(0, 1, "équipe")
                for i in range(len(team_list)):
                    ranking_table.set(16 - i, 0, 16 - i)
                    ranking_table.set(16 - i, 1, team_list_ordered[i].name)
                ranking_table.grid(row=5, column=1)

            if metric_clicked.get() == metric_options[3]:

                rank = [17 - i for i in range(1, len(qs_win) + 1)]

                qs_win_ordered = [y for _, y in sorted(zip(team_list, qs_win), key=lambda x: x[0].elo)]

                official_qs_win_ordered = [y for _, y in
                                           sorted(zip(team_list, official_qs_win), key=lambda x: x[0].elo)]

                team_list_ordered = sorted(team_list, key=lambda team: team.elo)

                ax1.scatter(rank, qs_win_ordered, label="victoire", color="r")

                ax1.set_xlim(0, 17)
                ax1.set_ylim(0, 1)
                ax1.set_xlabel("rang faible")
                ax1.set_ylabel("probabilité")

                ax1.set_title("format: Choose your opponent")
                ax1.legend()

                ax2.scatter(rank, official_qs_win_ordered, label="victoire", color="r")
                ax2.legend()

                ax2.set_xlim(0, 17)
                ax2.set_ylim(0, 1)
                ax2.set_xlabel("rang faible")
                ax2.set_ylabel("probabilité")

                ax2.set_title("format: UEFA officiel")
                ax2.legend()

                canvas = FigureCanvasTkAgg(fig, master=proba_window)
                canvas.draw()

                canvas.get_tk_widget().grid(row=25, column=0)

                toolbar_frame = tk.Frame(proba_window)
                toolbar_frame.grid(row=500, column=0)
                toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
                toolbar.update()
                canvas.get_tk_widget().grid(row=5, column=0)

                ranking_table = SimpleTable(proba_window, rows=17, columns=2)

                ranking_table.set(0, 0, "rang elo")
                ranking_table.set(0, 1, "équipe")
                for i in range(len(team_list)):
                    ranking_table.set(16 - i, 0, 16 - i)
                    ranking_table.set(16 - i, 1, team_list_ordered[i].name)
                ranking_table.grid(row=5, column=1)

        metric_clicked.trace("w", show_option)


class GUI:
    def __init__(self, team_list_year, qs_year, scenario_year, official_qs_year, victory_matrix_year,
                 best_scenario_year, official_best_scenario_year):
        # dictionnaire : cle: annee; contenu: team_list
        self.team_list_year = team_list_year
        # dictionnaire : cle: annee; contenu: [qs_win,qs_final,qs_semi,qs_quart]
        self.qs_year = qs_year
        # dictionnaire : cle: annee; contenu: [final,semi,quart,huitieme]
        self.scenario_year = scenario_year
        # dictionnaire : cle: annee; contenu: [qs_win,qs_final,qs_semi,qs_quart]
        self.official_qs_year = official_qs_year
        # dictionnaire : cle: annee; contenu: victory_matrix
        self.victory_matrix_year = victory_matrix_year
        # dictionnaire : cle: annee; contenu: [final_elo, final_weak, semi_elo, semi_weak, quart_elo, quart_weak]
        self.best_scenario_year = best_scenario_year
        # dictionnaire : cle: annee; contenu: [final_elo, final_weak, semi_elo, semi_weak, quart_elo, quart_weak]
        self.official_best_scenario_year = official_best_scenario_year

    def graphic_loop(self):
        root = tk.Tk()
        root.title("Affichage des résultats")
        # root.iconbitmap()
        root.geometry("1300x700")

        # 2009 n'existe jamais => juste pour tester si ça marche
        year_options = [
            "2009",
            "2010",
            "2011",
            "2012",
            "2013",
            "2014",
            "2015",
            "2016",
            "2017",
            "2018",
            "2019",
            "2020",
            "2021",
        ]

        # 2021 base case
        year_clicked = tk.StringVar()
        year_clicked.set(year_options[-1])
        global old_clicked
        old_clicked = year_clicked

        # act like the main if you dont have files
        def recalculate(year, fast, day=12, month=12):
            messagebox.showinfo("Message", "Cliquer pour démarrer les calculs, faites une autre activité, "
                                           "une fenêtre s'ouvrira pour vous prévenir quand ce sera fini.")
            try:
                pars = pm.Parser(day, month, year, loaded=False)
                self.team_list_year[year] = pars.team_list
                self.victory_matrix_year[year] = pars.victory_matrix
                result = gr.Result(day, month)
                tir.Round_of_16(day, month, year)
                file = open("json_files/execute_info.txt", 'w', encoding="utf-8")
                sending_info = dict()
                sending_info["year"] = year
                sending_info["fast"] = fast
                json.dump(sending_info, file, ensure_ascii=False)
                file.close()
            except:
                # the website is the only thing that can crash
                messagebox.showinfo("Erreur", "Site Down Impossibilité TOTALE d'avoir des résultats")

            cxx_exefile = "build/build-Choose-your-opponent-Desktop_Qt_5_15_0_MinGW_32_bit-Release/Choose_your_opponent.exe"
            subprocess.run(cxx_exefile)
            messagebox.showinfo("Message", "Calculs finis")
            self.qs_year = result.qs_year
            self.scenario_year = result.scenario_year
            self.official_qs_year = result.official_qs_year
            self.best_scenario_year = result.best_scenario_year
            self.official_best_scenario_year = result.official_best_scenario_year

        def can_you_choose_the_year(*args):
            try:
                dumb = self.scenario_year[int(year_clicked.get())]
                dumb = self.official_qs_year[int(year_clicked.get())]
                dumb = self.qs_year[int(year_clicked.get())]
            except:
                messagebox.showinfo("Erreur", "Le scénario n'existe pas ou n'a pas été calculé lors des étapes backend."
                                              " CHANGEZ L'ANNEE SVP ou répondez à la question suivante")
                MsgBox = tk.messagebox.askquestion('Choix', 'Voulez-vous calculez le scénario?',
                                                   icon='warning')
                fast = tk.messagebox.askquestion('Choix',
                                                 'Voulez-vous que ce soit rapide (30/40 min au lieu de 12h) mais imprécis?',
                                                 icon='warning')
                if MsgBox == 'yes' and fast == 'yes':
                    recalculate(int(year_clicked.get()), True)
                elif MsgBox == 'yes' and fast == 'no':
                    recalculate(int(year_clicked.get()), False)

                year_clicked.set(old_clicked.get())
                return

            team_list = self.team_list_year[int(year_clicked.get())]

            games_8th = SimpleTable(root, rows=25, columns=1, with_button=True, nb_team_round=16,
                                    scenario_list=self.scenario_year[int(year_clicked.get())], team_list=team_list,
                                    year=int(year_clicked.get()))

            X1 = self.scenario_year[int(year_clicked.get())][3][0]["X1"]
            X2 = self.scenario_year[int(year_clicked.get())][3][0]["X2"]
            games_8th.set(0, 0, "8èmes")

            winning_teams = []
            for i in range(len(X1)):
                if self.victory_matrix_year[int(year_clicked.get())][X1[i]][X2[i]] >= 0.5:
                    winning_teams.append(X1[i])
                else:
                    winning_teams.append(X2[i])

            for i in range(len(X1)):
                games_8th.set(3 * i + 1, 0, "")
                games_8th.set(3 * i + 2, 0, team_list[X1[i]].name, team_list[X2[i]].name,
                              team_list[X1[i]].competition_rank - 1,
                              team_list[X2[i]].competition_rank - 1, self.victory_matrix_year[int(year_clicked.get())],
                              winning_teams)

            games_8th.grid(row=5, column=1)

            games_4th = SimpleTable(root, rows=13, columns=1, with_button=True, nb_team_round=8,
                                    scenario_list=self.scenario_year[int(year_clicked.get())], team_list=team_list,
                                    year=int(year_clicked.get()))

            def search_and_fill_scenario(winning_teams, scenario_list):
                sorted_winning_teams = sorted(winning_teams)
                if len(winning_teams) == 8:
                    round_index = 2
                if len(winning_teams) == 4:
                    round_index = 1
                if len(winning_teams) == 2:
                    round_index = 0
                for scenario in scenario_list[round_index]:
                    number_of_good_teams = 0
                    for team_id in winning_teams:
                        if team_id in scenario["X1"] or team_id in scenario["X2"]:
                            number_of_good_teams += 1
                        if number_of_good_teams == len(winning_teams):
                            return scenario["X1"], scenario["X2"]

            X1, X2 = search_and_fill_scenario(winning_teams, self.scenario_year[int(year_clicked.get())])

            winning_teams = []
            for i in range(len(X1)):
                if self.victory_matrix_year[int(year_clicked.get())][X1[i]][X2[i]] >= 0.5:
                    winning_teams.append(X1[i])
                else:
                    winning_teams.append(X2[i])
            games_4th.set(0, 0, "Quarts")

            for i in range(len(X1)):
                games_4th.set(3 * i + 1, 0, "")
                games_4th.set(3 * i + 2, 0, team_list[X1[i]].name, team_list[X2[i]].name,
                              team_list[X1[i]].competition_rank - 1,
                              team_list[X2[i]].competition_rank - 1, self.victory_matrix_year[int(year_clicked.get())],
                              winning_teams)
            games_4th.grid(row=5, column=2)

            games_2th = SimpleTable(root, rows=7, columns=1, with_button=True, nb_team_round=4,
                                    scenario_list=self.scenario_year[int(year_clicked.get())], team_list=team_list,
                                    year=int(year_clicked.get()))

            X1, X2 = search_and_fill_scenario(winning_teams, self.scenario_year[int(year_clicked.get())])

            winning_teams = []
            for i in range(len(X1)):
                if self.victory_matrix_year[int(year_clicked.get())][X1[i]][X2[i]] >= 0.5:
                    winning_teams.append(X1[i])
                else:
                    winning_teams.append(X2[i])
            games_2th.set(0, 0, "Demies")

            for i in range(len(X1)):
                games_2th.set(3 * i + 1, 0, "")
                games_2th.set(3 * i + 2, 0, team_list[X1[i]].name, team_list[X2[i]].name,
                              team_list[X1[i]].competition_rank - 1,
                              team_list[X2[i]].competition_rank - 1, self.victory_matrix_year[int(year_clicked.get())],
                              winning_teams)
            games_2th.grid(row=5, column=3)

            games_1th = SimpleTable(root, rows=4, columns=1, with_button=True, nb_team_round=8,
                                    scenario_list=self.scenario_year[int(year_clicked.get())], team_list=team_list,
                                    year=int(year_clicked.get()))

            X1, X2 = search_and_fill_scenario(winning_teams, self.scenario_year[int(year_clicked.get())])

            winning_teams = []
            for i in range(len(X1)):
                if self.victory_matrix_year[int(year_clicked.get())][X1[i]][X2[i]] >= 0.5:
                    winning_teams.append(X1[i])
                else:
                    winning_teams.append(X2[i])
            games_1th.set(0, 0, "Finale")

            for i in range(len(X1)):
                games_1th.set(3 * i + 1, 0, "")
                games_1th.set(3 * i + 2, 0, team_list[X1[i]].name, team_list[X2[i]].name,
                              team_list[X1[i]].competition_rank - 1,
                              team_list[X2[i]].competition_rank - 1, self.victory_matrix_year[int(year_clicked.get())],
                              winning_teams)
            games_1th.grid(row=5, column=4)

        drop = tk.OptionMenu(root, year_clicked, *year_options)
        drop.grid(row=0, column=0)

        year_clicked.trace("w", can_you_choose_the_year)

        def create_new_window():
            max_number_of_window = 2
            global number_of_open_window
            if number_of_open_window < max_number_of_window:
                number_of_open_window += 1
                int_year_clicked = int(year_clicked.get())
                NewWindow(root, int_year_clicked, self.team_list_year, self.qs_year, self.official_qs_year,
                          self.best_scenario_year, self.official_best_scenario_year)
            else:
                messagebox.showinfo("Erreur", "Trop de fenêtres ouvertes")

        proba_window_button = tk.Button(root,
                                        text="Ouvrir métrique",
                                        command=create_new_window)

        proba_window_button.grid(row=0, column=100)

        root.mainloop()
