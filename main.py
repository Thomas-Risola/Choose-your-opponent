import ParseurMatrix as pm
import get_result as gr
import graphic_user_interface as gui

if __name__ == '__main__':

    # fill json files to feed MOPSI algorithm, can be commented if done once or
    # file already collected
    day = 12
    month = 12
    # draw around 12th December each year

    # problem en 2019
    for year in range(2010, 2022):
        if year == 2019:
            pars = pm.Parser(10, 6, year)
            continue
        pars = pm.Parser(day, month, year)  


    result = gr.Result(day, month, year)
    graphic = gui.GUI(pars.team_list, result.qs_win, result.qs_final, result.qs_semi, result.qs_quart)

    graphic.graphic_loop()
