import ParseurMatrix as pm

if __name__ == '__main__':
    day = 14
    month = 11
    year = 2021
    team_list = pm.search_and_fill_team_info(day, month, year)
    victory_matrix = pm.victory_matrix(team_list)
    print(victory_matrix)
    print(team_list[0].nationality)
    print(team_list[0].nationality)
    # we need to save the matrix to use it in C++ MOPSI Program
    # or we can try to execute this in the C++ program?
