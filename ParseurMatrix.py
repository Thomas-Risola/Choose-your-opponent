# import libraries
from bs4 import BeautifulSoup
import urllib3
import numpy as np


class Team:
    def __init__(self, name, elo, nationality=0, group=0):
        self.name = name
        self.elo = elo
        self.nationality = nationality
        self.group = group

    def __str__(self):
        print(self.name + " " + self.elo)

    def __set_name__(self, name):
        self.name = name

    def __set_elo__(self, elo):
        self.elo = elo
        
    def __set_nationality__(self, nationality):
        self.name = nationality

    def __set_group__(self, group):
        self.elo = group


# functions to generate url
def convert_date_to_string(day, month, year):
    return str(year) + "-" + str(month) + "-" + str(day)


def get_clubelo_url(str_date):
    return "http://clubelo.com/" + str_date + "/Ranking"


# set elos for all teams
def set_elo_from_soup(soup, team_list):
    ranking = soup.find("table", attrs={"class": "ranking"})
    for team in team_list:
        set_elo_from_ranking(ranking, team)


# set elo for one team
def set_elo_from_ranking(ranking, team):
    team_info = ranking.find("a", string=team.name).parent.parent
    # elo is what contain the elo information
    elo = team_info.find("td", attrs={"class": "r"})
    # .string to get  only the elo
    # then we convert into int
    team.__set_elo__(int(elo.string))


# do what you think it does with elo formulas
def victory_probability_1vs2(team1, team2):
    diff_elo = team1.elo - team2.elo
    return 1 / (10 ** (-diff_elo / 400) + 1)


# set probabilities into a matrix
def fill_victory_matrix(team_list):
    number_of_teams = len(team_list)
    matrix = np.zeros((number_of_teams, number_of_teams))
    for i in range(number_of_teams):
        for j in range(i+1, number_of_teams):
            matrix[i][j] = victory_probability_1vs2(team_list[i], team_list[j])
            matrix[j][i] = 1 - matrix[i][j]
    return matrix


def victory_matrix(team_list, day, month, year):
    # specify the url from the date you want
    http = urllib3.PoolManager()

    str_date = convert_date_to_string(day, month, year)
    url = get_clubelo_url(str_date)

    # get page
    response = http.request('GET', url)

    # make it usable
    soup = BeautifulSoup(response.data, "html.parser")

    set_elo_from_soup(soup, team_list)

    return fill_victory_matrix(team_list)
