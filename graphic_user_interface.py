import tkinter as tk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class GUI:
    def __init__(self, team_list, qs_win, qs_final, qs_semi, qs_quart):
        self.team_list = team_list
        self.qs_win = qs_win
        self.qs_final = qs_final
        self.qs_semi = qs_semi
        self.qs_quart = qs_quart

    @staticmethod
    def graphic_loop(self):
        root = tk.Tk()
        root.title("Affichage des résultats")
        # root.iconbitmap()
        # root.geometry("400*400")

        options = [
            "Probabilité d'atteindre une étape",
            "Métrique 2"
        ]

        clicked = tk.StringVar()
        clicked.set(options[0])

        drop = tk.OptionMenu(root, clicked, *options)
        drop.pack()

        def show_option(team_list, qs_win, qs_final, qs_semi, qs_quart):
            rank = [i for i in range(1, len(qs_win) + 1)]
            fig = plt.figure()

            plt.plot(rank, qs_win)
            plt.plot(rank, qs_final)
            plt.plot(rank, qs_semi)
            plt.plot(rank, qs_quart)

            canvas = FigureCanvasTkAgg(fig, master=root)
            canvas.draw()

            canvas.get_tk_widget().pack()
            toolbar = NavigationToolbar2Tk(canvas, root)
            toolbar.update()
            canvas.get_tk_widget().pack()

        clicked.trace("w", show_option)

        root.mainloop()
