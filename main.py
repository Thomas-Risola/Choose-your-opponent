import ParseurMatrix as pm
import get_result as gr
import graphic_user_interface as gui
import tirage_8e_8dec as tir

if __name__ == '__main__':

    # fill json files to feed MOPSI algorithm, can be commented if done once or
    # file already collected
    day = 12
    month = 12
    # draw around 12th December each year

    victory_matrix_year = dict()
    team_list_year = dict()

    for year in range(2010, 2022):
        pars = pm.Parser(day, month, year, loaded=True)
        team_list_year[year] = pars.team_list
        victory_matrix_year[year] = pars.victory_matrix
    result = gr.Result(day, month)

    
    graphic = gui.GUI(team_list_year, result.qs_year, result.scenario_year, result.official_qs_year,
                      victory_matrix_year, result.best_scenario_year, result.official_best_scenario_year)

    graphic.graphic_loop()
