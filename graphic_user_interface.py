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

    def graphic_loop(self):
        root = tk.Tk()
        root.title("Affichage des résultats")
        # root.iconbitmap()
        root.geometry("800x600")

        options = [
            "Probabilité d'atteindre une étape",
            "Métrique 2"
        ]

        clicked = tk.StringVar()
        clicked.set(options[0])

        drop = tk.OptionMenu(root, clicked, *options)
        drop.grid(row=1, column=0, pady=10)


        def show_option(*args):
            global canvas
            fig = plt.figure()
            canvas = FigureCanvasTkAgg(fig,root)
            for item in canvas.get_tk_widget().find_all():
                canvas.get_tk_widget().delete(item)
            if clicked.get() == options[0]:
                rank = [i for i in range(1, len(self.qs_win) + 1)]

                plt.plot(rank, self.qs_win)
                plt.plot(rank, self.qs_final)
                plt.plot(rank, self.qs_semi)
                plt.plot(rank, self.qs_quart)

                canvas = FigureCanvasTkAgg(fig, master=root)
                canvas.draw()

                canvas.get_tk_widget().grid(row=5, column=0)
                toolbar = NavigationToolbar2Tk(canvas, root)
                toolbar.update()
                canvas.get_tk_widget().grid(row=5, column=0)
            if clicked.get() == options[1]:
                rank = [i for i in range(1, len(self.qs_win) + 1)]

                plt.plot(rank, self.qs_win)

                canvas = FigureCanvasTkAgg(fig, master=root)
                canvas.draw()
                canvas.get_tk_widget().grid(row=5, column=0)

                toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
                toolbar.update()
                canvas.toolbar.grid(row=5, column=0)

        clicked.trace("w", show_option)

        root.mainloop()
