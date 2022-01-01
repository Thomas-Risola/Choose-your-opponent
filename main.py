import ParseurMatrix as pm
import get_result as gr
import graphic_user_interface as gui

if __name__ == '__main__':

    day = 12
    month = 11
    year = 2021
    pars = pm.Parser(day, month, year)

    print(pars.victory_matrix)
    for i in range(len(pars.team_list)):
        pars.team_list[i].str()
        print("\n")

    print(pars.play_matrix)
    for i in range(len(pars.team_list)):
        print("rank of", pars.team_list[i].name, ": ", pars.team_list[i].competition_rank)
    # we need to save the matrix to use it in C++ MOPSI Program
    # or we can try to execute this in the C++ program?

    result = gr.Result(day, month, year)
    graphic = gui.GUI(pars.team_list, result.qs_win, result.qs_final, result.qs_semi, result.qs_quart)

    graphic.graphic_loop()
