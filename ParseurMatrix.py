# import libraries
from bs4 import BeautifulSoup
import urllib3
import numpy as np


# class gathering team data
class Team:
    def __init__(self, name="a", elo=0, nationality="a", group="a", group_rank=0, point=0, goal_difference=0,
                 goal_for=0,
                 competition_rank=1):
        self.name = name
        self.elo = elo
        self.nationality = nationality
        self.group = group
        self.group_rank = group_rank
        self.point = point
        self.goal_difference = goal_difference
        self.goal_for = goal_for
        self.competition_rank = competition_rank

    def str(self):
        print("name: " + self.name + "\n" + "elo: " + str(
            self.elo) + "\n" + "nationality: " + self.nationality + "\n" + "group: " + self.group + "\n" + "group_rank: " + str(
            self.group_rank) + "\n" + "point: " + str(self.point) + "\n" + "goal_difference: " + str(
            self.goal_difference) + "\n" + "goal_for: " + str(self.goal_for) + "\n" + "competition_rank: " + str(
            self.competition_rank))

    def set_name(self, name):
        self.name = name

    def set_elo(self, elo):
        self.elo = elo

    def set_nationality(self, nationality):
        self.nationality = nationality

    def set_group(self, group):
        self.group = group

    def set_group_rank(self, group_rank):
        self.group_rank = group_rank

    def set_point(self, point):
        self.point = point

    def set_goal_difference(self, goal_difference):
        self.goal_difference = goal_difference

    def set_goal_for(self, goal_for):
        self.goal_for = goal_for

    def set_competition_rank(self, competition_rank):
        self.competition_rank = competition_rank


# functions to generate url
def convert_date_to_string(day, month, year):
    return str(year) + "-" + str(month) + "-" + str(day)


def get_clubelo_url(str_date):
    return "http://clubelo.com/" + str_date + "/Ranking"


# set elos and nationalities for all teams
def set_info_from_clubelo(soup, team_list):
    ranking = soup.find("table", attrs={"class": "ranking"})
    for team in team_list:
        set_info_from_ranking(ranking, team)


# set elo and nationality for one team
def set_info_from_ranking(ranking, team):
    team_info = ranking.find("a", string=team.name).parent.parent
    # elo is what contain the elo information
    elo = team_info.find("td", attrs={"class": "r"})
    # we find the nationality in the name of the flag on the site
    nationality = team_info.find("img").get("alt")
    # .string to get  only the info
    # then we convert into int
    team.set_elo(int(elo.string))
    team.set_nationality(nationality)


# do what you think it does with elo formulas
def victory_probability_1vs2(team1, team2):
    diff_elo = team1.elo - team2.elo
    return 1 / (10 ** (-diff_elo / 400) + 1)


# set probabilities into a matrix
def victory_matrix(team_list):
    number_of_teams = len(team_list)
    matrix = np.zeros((number_of_teams, number_of_teams))
    for i in range(number_of_teams):
        for j in range(i + 1, number_of_teams):
            matrix[i][j] = victory_probability_1vs2(team_list[i], team_list[j])
            matrix[j][i] = 1 - matrix[i][j]
    return matrix


def can_1_play_2(team1, team2):
    if team1.group == team2.group or team1.nationality == team2.nationality:
        return False
    else:
        return True


def playable_match_matrix(team_list):
    number_of_teams = len(team_list)
    matrix = np.empty((number_of_teams, number_of_teams), dtype=bool)
    for i in range(number_of_teams):
        matrix[i][i] = False
        for j in range(i + 1, number_of_teams):
            # symmetric matrix
            matrix[i][j] = can_1_play_2(team_list[i], team_list[j])
            matrix[j][i] = matrix[i][j]
    return matrix


def get_uefa_group_url(year):
    return "https://www.skysports.com/champions-league-table/" + str(year)


def search_and_fill_team_info(day, month, year, number_of_teams=16):
    # parse on UEFA group site

    # specify the url from the date you want
    http = urllib3.PoolManager()
    url = get_uefa_group_url(year)
    # get page
    response = http.request('GET', url)
    # make it usable
    soup = BeautifulSoup(response.data, "html.parser")
    team_list = [Team(str(i)) for i in range(number_of_teams)]
    set_info_from_uefa_groups(soup, team_list)

    name_converter_from_clubelo_to_uefa_group(team_list)
    # parse on clubelo site

    # specify the url from the date you want
    http = urllib3.PoolManager()
    str_date = convert_date_to_string(day, month, year)
    url = get_clubelo_url(str_date)
    # get page
    response = http.request('GET', url)
    # make it usable
    soup = BeautifulSoup(response.data, "html.parser")
    set_info_from_clubelo(soup, team_list)
    return team_list


def compute_competition_ranking(team_list):
    number_of_teams = len(team_list)
    group_winner_list = []
    runner_up_list = []
    # first we compare whether the team has won its group or not
    for i in range(number_of_teams):
        if team_list[i].group_rank == 1:
            group_winner_list.append(team_list[i])
        else:
            team_list[i].competition_rank = number_of_teams // 2 + 1
            runner_up_list.append(team_list[i])
    # then we start comparing the points of each team to rank them
    compare_point(group_winner_list)
    compare_point(runner_up_list)
    all_tie_case1 = build_tie_case(team_list)
    # if there are tie cases we compare on Goal Difference
    if len(all_tie_case1) > 0:
        for i in range(len(all_tie_case1)):
            compare_goal_difference(all_tie_case1[i])
    all_tie_case2 = build_tie_case(team_list)

    # if there are tie cases we compare on Goal For
    if len(all_tie_case2) > 0:
        for j in range(len(all_tie_case2)):
            compare_goal_for(all_tie_case2[j])
    # we then hope that all cases are cleared or we should add 
    # the other decider rules


# do what it does
def search_tie_case(team_list):
    number_of_teams = len(team_list)
    competition_rank_list = []
    for i in range(number_of_teams):
        competition_rank_list.append(team_list[i].competition_rank)
    unique, counts = np.unique(competition_rank_list, return_counts=True)
    return dict(zip(unique, counts))


# return lists of tie cases
def build_tie_case(team_list):
    number_of_teams = len(team_list)
    rank_count = search_tie_case(team_list)
    all_tie_case = []
    for key in rank_count:
        if rank_count[key] >= 2:
            tie_case = []
            for j in range(number_of_teams):
                if team_list[j].competition_rank == key:
                    tie_case.append(team_list[j])
            all_tie_case.append(tie_case)
    return all_tie_case


# compare team point then add rank to the one with lowest point
def compare_point(team_list):
    number_of_teams = len(team_list)
    for i in range(number_of_teams):
        for j in range(i + 1, number_of_teams):
            if team_list[i].point > team_list[j].point:
                team_list[j].competition_rank += 1
            elif team_list[i].point < team_list[j].point:
                team_list[i].competition_rank += 1


# compare team goal_difference then add rank to the one with lowest point
def compare_goal_difference(team_list):
    number_of_teams = len(team_list)
    for i in range(number_of_teams):
        for j in range(i + 1, number_of_teams):
            if team_list[i].goal_difference > team_list[j].goal_difference:
                team_list[j].competition_rank += 1
            elif team_list[i].goal_difference < team_list[j].goal_difference:
                team_list[i].competition_rank += 1


# compare team goal_for then add rank to the one with lowest point
def compare_goal_for(team_list):
    number_of_teams = len(team_list)
    for i in range(number_of_teams):
        for j in range(i + 1, number_of_teams):
            if team_list[i].goal_for > team_list[j].goal_for:
                team_list[j].competition_rank += 1
            elif team_list[i].goal_for < team_list[j].goal_for:
                team_list[i].competition_rank += 1


# set info for all teams
def set_info_from_uefa_groups(soup, team_list):
    groups = soup.find("div", attrs={"class": "page-filters__offset"})
    name_list = groups.find_all("td", attrs={"class": "standing-table__cell standing-table__cell--name"})
    team_info_list = soup.find_all("td", attrs={"class": "standing-table__cell"})
    number_of_player_in_competition = len(name_list)
    number_of_info_for_each_team_on_the_site = 11
    team_id = 0
    for i in range(number_of_player_in_competition):
        if int(team_info_list[i * number_of_info_for_each_team_on_the_site].string) < 3:
            group_name_info = name_list[i].parent.parent.parent
            group_name = group_name_info.find("caption", attrs={"class": "standing-table__caption"})
            team_list[team_id].set_group(group_name.string)
            team_list[team_id].set_name(name_list[i].get('data-short-name'))
            team_list[team_id].set_group_rank(int(team_info_list[i * number_of_info_for_each_team_on_the_site].string))
            set_other_info_from_group(team_info_list, team_list[team_id], number_of_info_for_each_team_on_the_site, i)
            team_id += 1


# set goal for, goal diff, point for one team
def set_other_info_from_group(info_list, team, number_of_info_for_each_team_on_the_site, soup_index):
    team.set_goal_for(int(info_list[soup_index * number_of_info_for_each_team_on_the_site + 6].string))
    team.set_goal_difference(int(info_list[soup_index * number_of_info_for_each_team_on_the_site + 8].string))
    team.set_point(int(info_list[soup_index * number_of_info_for_each_team_on_the_site + 9].string))


def name_converter_from_clubelo_to_uefa_group(team_list):
    uefa_group_name = {"0": "Bayern Munich", "1": "Manchester City", "3": "Liverpool", "4": "Chelsea",
                       "5": "Real Madrid", "6": "Paris Saint-Germain",
                       "7": "Manchester United", "8": "Ajax", "9": "Inter Milan", "10": "Atletico Madrid",
                       "11": "Arsenal",
                       "12": "West Ham", "13": "Barcelona", "14": "Sevilla", "15": "Borussia Dortmund",
                       "16": "Juventus",
                       "17": "FC Porto", "18": "Naples", "19": "AC Milan", "20": "Atalanta", "21": "RB Leipzig",
                       "22": "Villarreal", "23": "Tottenham", "24": "Real Sociedad", "25": "Red Bull Salzburg",
                       "26": "Club Brugge", "27": "Sporting Lisbon", "28": "Besiktas", "29": "Sheriff Tiraspol(Mol)",
                       "30": "Shakhtar Donetsk",
                       "31": "Benfica", "32": "Dynamo Kiev", "33": "BSC Young Boys Bern", "34": "Lille",
                       "35": "Wolfsburg",
                       "36": "Zenit St. Petersburg", "37": "Malmo FF"}
    clubelo_name = {"0": "Bayern", "1": "Man City", "3": "Liverpool", "4": "Chelsea", "5": "Real Madrid",
                    "6": "Paris SG", "7": "Man United", "8": "Ajax", "9": "Inter", "10": "Atlético", "11": "Arsenal",
                    "12": "West Ham", "13": "Barcelona", "14": "Sevilla", "15": "Dortmund", "16": "Juventus",
                    "17": "Porto", "18": "Napoli", "19": "Milan", "20": "Atalanta", "21": "RB Leipzig",
                    "22": "Villarreal", "23": "Tottenham", "24": "Real Sociedad", "25": "Salzburg", "26": "Brugge",
                    "27": "Sporting", "28": "Beşiktaş", "29": "Sheriff", "30": "Шахтар", "31": "Benfica",
                    "32": "Динамо Київ", "33": "Young Boys", "34": "Lille", "35": "Wolfsburg", "36": "Зенит",
                    "37": "Malmö"}
    for team in team_list:
        key = get_key(team.name, uefa_group_name)
        team.set_name(clubelo_name[key])


def get_key(val, my_dict):
    for key, value in my_dict.items():
        if val == value:
            return key
