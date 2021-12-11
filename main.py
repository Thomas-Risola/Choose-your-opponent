import ParseurMatrix as pm

if __name__ == '__main__':

    day = 12
    month = 11
    year = 2021
    pars=pm.Parseur(day,month,year)

    print(pars.victory_matrix)
    for i in range(len(pars.team_list)):
        pars.team_list[i].str()
        print("\n")
    print(pars.play_match)
    for i in range(len(pars.team_list)):
        print("rank of", pars.team_list[i].name, ": ", pars.team_list[i].competition_rank)
    # we need to save the matrix to use it in C++ MOPSI Program
    # or we can try to execute this in the C++ program?
