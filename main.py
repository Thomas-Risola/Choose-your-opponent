import ParseurMatrix as pm

if __name__ == '__main__':

    day = 12
    month = 11
    year = 2021
    team_list = pm.search_and_fill_team_info(day, month, year)
    pm.compute_competition_ranking(team_list)
    team_list = sorted(team_list, key=lambda team: team.competition_rank)
    victory_matrix = pm.victory_matrix(team_list)
    play_match = pm.playable_match_matrix(team_list)

    print(victory_matrix)
    for i in range(len(team_list)):
        team_list[i].str()
        print("\n")
    print(play_match)
    for i in range(len(team_list)):
        print("rank of", team_list[i].name, ": ", team_list[i].competition_rank)
    # we need to save the matrix to use it in C++ MOPSI Program
    # or we can try to execute this in the C++ program?
