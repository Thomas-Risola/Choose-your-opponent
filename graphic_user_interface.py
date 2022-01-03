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
        root.geometry("1300x600")

        options = [
            "Probabilité d'atteindre une étape",
            "Métrique 2"
        ]

        clicked = tk.StringVar()
        clicked.set(options[0])

        drop = tk.OptionMenu(root, clicked, *options)
        drop.grid(row=0, column=0)


        def show_option(*args):
            global canvas
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
            fig.suptitle('Comparaison des formats')
            canvas = FigureCanvasTkAgg(fig, root)
            for item in canvas.get_tk_widget().find_all():
                canvas.get_tk_widget().delete(item)
            if clicked.get() == options[0]:
                rank = [i for i in range(1, len(self.qs_win) + 1)]

                ax1.scatter(rank, self.qs_win, label="victoire")
                ax1.scatter(rank, self.qs_final, label="finale")
                ax1.scatter(rank, self.qs_semi, label="demi-finale")
                ax1.scatter(rank, self.qs_quart, label="quart de finale")

                ax1.set_xlim(0, 17)
                ax1.set_ylim(0, 1)
                ax1.set_xlabel("rang faible")
                ax1.set_ylabel("probabilité")

                ax1.set_title("format: Choose your opponent")
                ax1.legend()

                ax2.scatter(rank, self.qs_win, label="victoire")
                ax2.scatter(rank, self.qs_final, label="finale")
                ax2.scatter(rank, self.qs_semi, label="demi-finale")
                ax2.scatter(rank, self.qs_quart, label="quart de finale")

                ax2.set_xlim(0, 17)
                ax2.set_ylim(0, 1)
                ax2.set_xlabel("rang faible")
                ax2.set_ylabel("probabilité")

                ax2.set_title("format: UEFA officiel")
                ax2.legend()

                canvas = FigureCanvasTkAgg(fig, master=root)
                canvas.draw()

                canvas.get_tk_widget().grid(row=25, column=0)

                frame = tk.Frame(root)
                frame.grid(row=0, column=1)
                toolbar = NavigationToolbar2Tk(canvas, frame)
                toolbar.update()
                canvas.get_tk_widget().grid(row=5, column=0)
            if clicked.get() == options[1]:
                rank = [i for i in range(1, len(self.qs_win) + 1)]

                ax1.scatter(rank, self.qs_win, label="victoire")

                ax1.set_xlim(0, 17)
                ax1.set_ylim(0, 1)
                ax1.set_xlabel("rang faible")
                ax1.set_ylabel("probabilité")

                ax1.set_title("format: Choose your opponent")
                ax1.legend()

                ax2.scatter(rank, self.qs_win, label="victoire")

                ax2.set_xlim(0, 17)
                ax2.set_ylim(0, 1)
                ax2.set_xlabel("rang faible")
                ax2.set_ylabel("probabilité")

                ax2.set_title("format: UEFA officiel")
                ax2.legend()

                canvas = FigureCanvasTkAgg(fig, master=root)
                canvas.draw()

                canvas.get_tk_widget().grid(row=25, column=0)

                frame = tk.Frame(root)
                frame.grid(row=0, column=1)
                toolbar = NavigationToolbar2Tk(canvas, frame)
                toolbar.update()
                canvas.get_tk_widget().grid(row=5, column=0)

        clicked.trace("w", show_option)

        root.mainloop()
