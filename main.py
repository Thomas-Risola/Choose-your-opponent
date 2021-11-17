import ParseurMatrix as pm

if __name__ == '__main__':
    day = 14
    month = 12
    year = 2021
    team_list = [pm.Team("Man City", 0), pm.Team("Bayern", 0), pm.Team("Liverpool", 0), pm.Team("Chelsea", 0),
                 pm.Team("Juventus", 0), pm.Team("Paris SG", 0), pm.Team("Dortmund", 0), pm.Team("Real Madrid", 0),
                 pm.Team("Porto", 0), pm.Team("RB Leipzig", 0), pm.Team("Atlético", 0), pm.Team("Barcelona", 0),
                 pm.Team("Sevilla", 0), pm.Team("Lazio", 0), pm.Team("Atalanta", 0), pm.Team("Gladbach", 0)]
    pm.set_info_from_clubelo(team_list)
    victory_matrix = pm.victory_matrix(team_list, day, month, year)
    print(victory_matrix)
    # we need to save the matrix to use it in C++ MOPSI Program
    # or we can try to execute this in the C++ program?
