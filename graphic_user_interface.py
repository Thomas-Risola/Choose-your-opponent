import tkinter as tk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class SimpleTable(tk.Frame):
    def __init__(self, parent, rows=10, columns=2):
        # use black background so it "peeks through" to
        # form grid lines
        tk.Frame.__init__(self, parent, background="black")
        self._widgets = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                label = tk.Label(self, text="%s/%s" % (row, column),
                                 borderwidth=0, width=10)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)


    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)

class GUI:
    def __init__(self, team_list_year, qs_year):
        # dictionnaire : cle: annee; contenu: team_list
        self.team_list_year = team_list_year
        # dictionnaire : cle: annee; contenu: [qs_win,qs_final,qs_semi,qs_quart]
        self.qs_year = qs_year

    def graphic_loop(self):
        root = tk.Tk()
        root.title("Affichage des résultats")
        # root.iconbitmap()
        root.geometry("1300x600")

        metric_options = [
            "Probabilité d'atteindre une étape",
            "Métrique 2"
        ]

        year_options = [
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

        metric_clicked = tk.StringVar()
        metric_clicked.set(metric_options[0])

        # 2021 base case
        year_clicked = tk.StringVar()
        year_clicked.set(year_options[-1])

        drop = tk.OptionMenu(root, year_clicked, *year_options)
        drop.grid(row=0, column=0)

        games_8th = SimpleTable(root, rows=25, columns=1)
        if True: # À remplacer dès que l'on obtient le scénario
            team_list = self.team_list_year[int(year_clicked.get())]
            X1=team_list[:8]
            X2=team_list[8:]
        games_8th.set(0, 0, "8èmes")
        for i in range(len(X1)):
            games_8th.set(3*i+2, 0, X1[i].name)
            games_8th.set(3*i+3, 0, X2[i].name)
            games_8th.set(3*i+1, 0, "")
        games_8th.grid(row=5, column=1)

        games_4th = SimpleTable(root, rows=13, columns=1)
        if True: # À remplacer dès que l'on obtient le scénario
            X2=X1[4:]
            X1=X1[:4]
        games_4th.set(0, 0, "Quarts")
        for i in range(len(X1)):
            games_4th.set(3*i+2, 0, X1[i].name)
            games_4th.set(3*i+3, 0, X2[i].name)
            games_4th.set(3*i+1, 0, "")
        games_4th.grid(row=5, column=2)

        games_2th = SimpleTable(root, rows=7, columns=1)
        if True: # À remplacer dès que l'on obtient le scénario
            X2=X1[2:]
            X1=X1[:2]
        games_2th.set(0, 0, "Demis")
        for i in range(len(X1)):
            games_2th.set(3*i+2, 0, X1[i].name)
            games_2th.set(3*i+3, 0, X2[i].name)
            games_2th.set(3*i+1, 0, "")
        games_2th.grid(row=5, column=3)

        games_1th = SimpleTable(root, rows=4, columns=1)
        if True: # À remplacer dès que l'on obtient le scénario
            X2=X1[1:]
            X1=X1[:1]
        games_1th.set(0, 0, "Finale")
        for i in range(len(X1)):
            games_1th.set(3*i+2, 0, X1[i].name)
            games_1th.set(3*i+3, 0, X2[i].name)
            games_1th.set(3*i+1, 0, "")
        games_1th.grid(row=5, column=4)

        def createNewWindow():
            def leave():
                proba_window.destroy()  # Détruit la fenêtre secondaire
                root.deiconify()  # Remet en avant-plan

            root.withdraw()
            global proba_window
            proba_window = tk.Toplevel(root)
            proba_window.title("Affichage des métriques")
            # proba_window.iconbitmap()
            proba_window.geometry("1300x600")

            drop = tk.OptionMenu(proba_window, metric_clicked, *metric_options)
            drop.grid(row=0, column=0)

            leave_frame = tk.Frame(proba_window)
            leave_frame.grid(row=0, column=1)
            leave_button = tk.Button(leave_frame, text='Quitter', command=leave)
            leave_button.grid(row=0, column=0)




            def show_option(*args):
                global canvas
                plt.close()
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
                fig.suptitle('Comparaison des formats')
                canvas = FigureCanvasTkAgg(fig, proba_window_button)
                for item in canvas.get_tk_widget().find_all():
                    canvas.get_tk_widget().delete(item)
                if metric_clicked.get() == metric_options[0]:
                    qs_win, qs_final, qs_semi, qs_quart = self.qs_year[int(year_clicked.get())]

                    rank = [i for i in range(1, len(qs_win) + 1)]

                    ax1.scatter(rank, qs_win, label="victoire")
                    ax1.scatter(rank, qs_final, label="finale")
                    ax1.scatter(rank, qs_semi, label="demi-finale")
                    ax1.scatter(rank, qs_quart, label="quart de finale")

                    ax1.set_xlim(0, 17)
                    ax1.set_ylim(0, 1)
                    ax1.set_xlabel("rang faible")
                    ax1.set_ylabel("probabilité")

                    ax1.set_title("format: Choose your opponent")
                    ax1.legend()

                    ax2.scatter(rank, qs_win, label="victoire")
                    ax2.scatter(rank, qs_final, label="finale")
                    ax2.scatter(rank, qs_semi, label="demi-finale")
                    ax2.scatter(rank, qs_quart, label="quart de finale")

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

                    team_list = self.team_list_year[int(year_clicked.get())]
                    ranking_table.set(0, 0, "rang faible")
                    ranking_table.set(0, 1, "équipe")
                    for i in range(len(team_list)):
                        ranking_table.set(i+1, 0, team_list[i].competition_rank)
                        ranking_table.set(i+1, 1, team_list[i].name)
                    ranking_table.grid(row=5, column=1)

                if metric_clicked.get() == metric_options[1]:
                    qs_win, qs_final, qs_semi, qs_quart = self.qs_year[int(year_clicked.get())]

                    rank = [i for i in range(1, len(qs_win) + 1)]

                    ax1.scatter(rank, qs_win, label="victoire")

                    ax1.set_xlim(0, 17)
                    ax1.set_ylim(0, 1)
                    ax1.set_xlabel("rang faible")
                    ax1.set_ylabel("probabilité")

                    ax1.set_title("format: Choose your opponent")
                    ax1.legend()

                    ax2.scatter(rank, qs_win, label="victoire")

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

            metric_clicked.trace("w", show_option)

        proba_window_button = tk.Button(root,
                                        text="Create new window",
                                        command=createNewWindow)

        proba_window_button.grid(row=0, column=100)

        root.mainloop()
