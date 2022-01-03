# import libraries
from bs4 import BeautifulSoup
import urllib3
import json
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
            self.elo) + "\n" + "nationality: " + self.nationality + "\n" + "group: " + self.group + "\n" +
              "group_rank: " + str(self.group_rank) + "\n" + "point: " + str(self.point) + "\n" + "goal_difference: "
              + str(self.goal_difference) + "\n" + "goal_for: " + str(
            self.goal_for) + "\n" + "competition_rank: " + str(
            self.competition_rank))


class Parser:
    def __init__(self, day, month, year, fileprefix1="json_files/team_list", fileprefix2="json_files/matrix"):
        filename1 = fileprefix1 + "-" + str(day) + "-" + str(month) + "-" + str(year) + ".txt"
        filename2 = fileprefix2 + "-" + str(day) + "-" + str(month) + "-" + str(year) + ".txt"
        print("Trying connection for around 15 seconds...")
        try:
            self.team_list = Parser.search_and_fill_team_info(day, month, year)
        except:
            print("Failed to connect, trying backup file...")
            try:
                self.team_list = Parser.get_team_list_from_file(filename1)
                self.victory_matrix, self.play_matrix = Parser.get_matrix_from_file(filename2)
            except:
                raise RuntimeError("Could not find neither the web page nor the backup file")
        else:
            print("Site found")
            Parser.compute_competition_ranking(self.team_list)
            self.team_list = sorted(self.team_list, key=lambda team: team.competition_rank)
            Parser.write_team_list_to_file(filename1, self.team_list)
            self.victory_matrix = Parser.victory_matrix(self.team_list)
            self.play_matrix = Parser.playable_match_matrix(self.team_list)
            Parser.write_matrix_to_file(filename2, self.victory_matrix, self.play_matrix)

    # write data to file so as to be able to work offline
    # relies on semicolons and new lines; do not use these characters in the attributes of the teams
    @staticmethod
    def write_team_list_to_file(filename, team_list):
        file = open(filename, 'w', encoding="utf-8")
        dict_list = []
        for team in team_list:
            dict_list.append({
                "name": team.name,
                "elo": team.elo,
                "nationality": team.nationality,
                "group": team.group,
                "group_rank": team.group_rank,
                "point": team.point,
                "goal_difference": team.goal_difference,
                "goal_for": team.goal_for,
                "competition_rank": team.competition_rank})
        json.dump(dict_list, file, ensure_ascii=False)
        file.close()

    # write data to file so as to be able to work on C++ algorithm
    # relies on semicolons and new lines; do not use these characters in the attributes of the teams
    @staticmethod
    def write_matrix_to_file(filename, victory_matrix, play_matrix):
        file = open(filename, 'w', encoding="utf-8")
        v_matrix = victory_matrix.tolist()
        p_matrix = play_matrix.tolist()
        dict_list = [{
            "victory_matrix": v_matrix,
            "play_matrix": p_matrix}]
        json.dump(dict_list, file, ensure_ascii=False)
        file.close()

    # if fetch failed, fall back to file
    # relies on semicolons and new lines; do not use these characters in the attributes of the teams
    @staticmethod
    def get_team_list_from_file(filename):
        file = open(filename, 'r', encoding="utf-8")
        dict_list = json.load(file)
        team_list = []
        for dd in dict_list:
            team_list.append(Team(
                dd["name"],
                dd["elo"],
                dd["nationality"],
                dd["group"],
                dd["group_rank"],
                dd["point"],
                dd["goal_difference"],
                dd["goal_for"],
                dd["competition_rank"]))
        file.close()
        return team_list

    @staticmethod
    def get_matrix_from_file(filename):
        file = open(filename, 'r', encoding="utf-8")
        dict_list = json.load(file)[0]
        file.close()
        return dict_list["victory_matrix"], dict_list["play_matrix"]

    # functions to generate url
    @staticmethod
    def convert_date_to_string(day, month, year):
        return str(year) + "-" + str(month) + "-" + str(day)

    @staticmethod
    def get_clubelo_url(str_date):
        return "http://clubelo.com/" + str_date + "/Ranking"

    # set elos and nationalities for all teams
    @staticmethod
    def set_info_from_clubelo(soup, team_list):
        ranking = soup.find("table", attrs={"class": "ranking"})
        for team in team_list:
            Parser.set_info_from_ranking(ranking, team)

    # set elo and nationality for one team
    @staticmethod
    def set_info_from_ranking(ranking, team):
        team_info = ranking.find("a", string=team.name).parent.parent
        # elo is what contain the elo information
        elo = team_info.find("td", attrs={"class": "r"})
        # we find the nationality in the name of the flag on the site
        nationality = team_info.find("img").get("alt")
        # .string to get  only the info
        # then we convert into int
        team.elo = int(elo.string)
        team.nationality = nationality

    # do what you think it does with elo formulas
    @staticmethod
    def victory_probability_1vs2(team1, team2):
        diff_elo = team1.elo - team2.elo
        return 1 / (10 ** (-diff_elo / 400) + 1)

    # set probabilities into a matrix
    @staticmethod
    def victory_matrix(team_list):
        number_of_teams = len(team_list)
        matrix = np.zeros((number_of_teams, number_of_teams))
        for i in range(number_of_teams):
            for j in range(i + 1, number_of_teams):
                matrix[i][j] = Parser.victory_probability_1vs2(team_list[i], team_list[j])
                matrix[j][i] = 1 - matrix[i][j]
        return matrix

    @staticmethod
    def can_1_play_2(team1, team2):
        if team1.group == team2.group or team1.nationality == team2.nationality or team1.group_rank == team2.group_rank:
            return False
        else:
            return True

    @staticmethod
    def playable_match_matrix(team_list):
        number_of_teams = len(team_list)
        matrix = np.empty((number_of_teams, number_of_teams), dtype=bool)
        for i in range(number_of_teams):
            matrix[i][i] = False
            for j in range(i + 1, number_of_teams):
                # symmetric matrix
                matrix[i][j] = Parser.can_1_play_2(team_list[i], team_list[j])
                matrix[j][i] = matrix[i][j]
        return matrix

    @staticmethod
    def get_uefa_group_url(year):
        return "https://www.skysports.com/champions-league-table/" + str(year)

    @staticmethod
    def search_and_fill_team_info(day, month, year, number_of_teams=16):
        # parse on UEFA group site

        # specify the url from the date you want
        http = urllib3.PoolManager()
        url = Parser.get_uefa_group_url(year)
        # get page
        response = http.request('GET', url)
        # make it usable
        soup = BeautifulSoup(response.data, "html.parser")
        team_list = [Team(str(i)) for i in range(number_of_teams)]
        Parser.set_info_from_uefa_groups(soup, team_list)

        Parser.name_converter_from_clubelo_to_uefa_group(team_list)

        # parse on clubelo site

        # specify the url from the date you want
        str_date = Parser.convert_date_to_string(day, month, year)
        url = Parser.get_clubelo_url(str_date)
        # get page
        response = http.request('GET', url, retries=3, timeout=3)
        # make it usable
        soup = BeautifulSoup(response.data, "html.parser")
        Parser.set_info_from_clubelo(soup, team_list)
        return team_list

    @staticmethod
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
        Parser.compare_point(group_winner_list)
        Parser.compare_point(runner_up_list)
        all_tie_case1 = Parser.build_tie_case(team_list)
        # if there are tie cases we compare on Goal Difference
        if len(all_tie_case1) > 0:
            for i in range(len(all_tie_case1)):
                Parser.compare_goal_difference(all_tie_case1[i])
        all_tie_case2 = Parser.build_tie_case(team_list)

        # if there are tie cases we compare on Goal For
        if len(all_tie_case2) > 0:
            for j in range(len(all_tie_case2)):
                Parser.compare_goal_for(all_tie_case2[j])
        # we then hope that all cases are cleared or we should add
        # the other decider rules

    @staticmethod
    def search_tie_case(team_list):
        number_of_teams = len(team_list)
        competition_rank_list = []
        for i in range(number_of_teams):
            competition_rank_list.append(team_list[i].competition_rank)
        unique, counts = np.unique(competition_rank_list, return_counts=True)
        return dict(zip(unique, counts))

    # return lists of tie cases
    @staticmethod
    def build_tie_case(team_list):
        number_of_teams = len(team_list)
        rank_count = Parser.search_tie_case(team_list)
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
    @staticmethod
    def compare_point(team_list):
        number_of_teams = len(team_list)
        for i in range(number_of_teams):
            for j in range(i + 1, number_of_teams):
                if team_list[i].point > team_list[j].point:
                    team_list[j].competition_rank += 1
                elif team_list[i].point < team_list[j].point:
                    team_list[i].competition_rank += 1

    # compare team goal_difference then add rank to the one with lowest point
    @staticmethod
    def compare_goal_difference(team_list):
        number_of_teams = len(team_list)
        for i in range(number_of_teams):
            for j in range(i + 1, number_of_teams):
                if team_list[i].goal_difference > team_list[j].goal_difference:
                    team_list[j].competition_rank += 1
                elif team_list[i].goal_difference < team_list[j].goal_difference:
                    team_list[i].competition_rank += 1

    # compare team goal_for then add rank to the one with lowest point
    @staticmethod
    def compare_goal_for(team_list):
        number_of_teams = len(team_list)
        for i in range(number_of_teams):
            for j in range(i + 1, number_of_teams):
                if team_list[i].goal_for > team_list[j].goal_for:
                    team_list[j].competition_rank += 1
                elif team_list[i].goal_for < team_list[j].goal_for:
                    team_list[i].competition_rank += 1

    # set info for all teams
    @staticmethod
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
                team_list[team_id].group = group_name.string
                team_list[team_id].name = name_list[i].get('data-short-name')
                team_list[team_id].group_rank = int(team_info_list[i * number_of_info_for_each_team_on_the_site].string)
                Parser.set_other_info_from_group(team_info_list, team_list[team_id],
                                                 number_of_info_for_each_team_on_the_site, i)
                team_id += 1

    # set goal for, goal diff, point for one team
    @staticmethod
    def set_other_info_from_group(info_list, team, number_of_info_for_each_team_on_the_site, soup_index):
        team.goal_for = int(info_list[soup_index * number_of_info_for_each_team_on_the_site + 6].string)
        team.goal_difference = int(info_list[soup_index * number_of_info_for_each_team_on_the_site + 8].string)
        team.point = int(info_list[soup_index * number_of_info_for_each_team_on_the_site + 9].string)

    @staticmethod
    def name_converter_from_clubelo_to_uefa_group(team_list):
        conversion_dict = {"Bayern Munich": "Bayern", "Manchester City": "Man City", "Liverpool": "Liverpool",
                           "Chelsea": "Chelsea", "Real Madrid": "Real Madrid",
                           "Paris Saint-Germain": "Paris SG", "Manchester United": "Man United", "Ajax": "Ajax",
                           "Inter Milan": "Inter", "Atletico Madrid": "Atlético", "Arsenal": "Arsenal",
                           "West Ham": "West Ham", "Barcelona": "Barcelona", "Sevilla": "Sevilla",
                           "Borussia Dortmund": "Dortmund", "Juventus": "Juventus",
                           "FC Porto": "Porto", "Napoli": "Napoli", "AC Milan": "Milan", "Atalanta": "Atalanta",
                           "RB Leipzig": "RB Leipzig",
                           "Villarreal": "Villarreal", "Tottenham": "Tottenham", "Real Sociedad": "Real Sociedad",
                           "Red Bull Salzburg": "Salzburg", "Club Brugge": "Brugge",
                           "Sporting Lisbon": "Sporting", "Besiktas": "Beşiktaş", "Sheriff Tiraspol(Mol)": "Sheriff",
                           "Shakhtar Donetsk": "Шахтар", "Benfica": "Benfica",
                           "Dynamo Kiev": "Динамо Київ", "BSC Young Boys Bern": "Young Boys", "Lille": "Lille",
                           "Wolfsburg": "Wolfsburg", "Zenit St. Petersburg": "Зенит",
                           "Malmo FF": "Malmö", "Galatasaray": "Galatasaray", "Tottenham Hotspur": "Tottenham",
                           "Olympiakos FC": "Ολυμπιακός",
                           "Crvena Zvezda": "Crvena Zvezda", "Dinamo Zagreb": "Dinamo Zagreb",
                           "Bayer Leverkusen": "Leverkusen", "Lokomotiv Moscow": "Локомотив Москва",
                           "M'gladbach": "Gladbach", "Marseille": "Marseille", "FC Midtjylland": "Midtjylland",
                           "Krasnodar": "Краснодар", "Rennes": "Rennes", "Lazio": "Lazio",
                           "Ferencvaros": "Ferencváros", "Istanbul Buyuksehir": "Başakşehir", "Genk": "Genk",
                           "Slavia Prague": "Slavia Praha", "Valencia": "Valencia", "Lyon": "Lyon", "Monaco": "Monaco",
                           "PSV Eindhoven": "PSV", "Schalke": "Schalke", "AEK Athens": "AEK",
                           "Hoffenheim": "Hoffenheim", "Roma": "Roma", "FC Viktoria Plzen": "Viktoria Plzeň",
                           "CSKA Moscow": "ЦСКА", "Basel": "Basel", "Celtic": "Celtic", "Anderlecht": "Anderlecht",
                           "Qarabag FK": "Qarabağ", "Spartak Moscow": "Спартак Москва", "Maribor": "Maribor",
                           "Feyenoord": "Feyenoord", "Apoel Nicosia": "ΑΠΟΕΛ", "Ludogorets":"Лудогорец",
                           "FK Rostov": "Ростов", "Legia Warsaw": "Legia", "Leicester City": "Leicester",
                           "FC Copenhagen": "FC København", "Astana": "Астана", "BATE Borisov": "БАТЭ",
                           "Maccabi Tel Aviv": "מכבי תל אביב", "AA Gent ": "Gent", "FC Steaua Bucuresti": "Steaua",
                           "FK Austria Wien": "Austria Wien", "Malaga": "Málaga", "FC Nordsjaelland": " Nordsjælland",
                           "CFR Cluj-Napoca": "CFR Cluj", "Braga": "Braga", "Trabzonspor": " Trabzonspor",
                           "CS Otelul Galati": "Oțelul Galați", "FC Twente": "Twente", "Werder Bremen": "Werder",
                           "Hapoel Tel Aviv": "הפועל תל-אביב", "Rangers": "Rangers", "Bursaspor": "Bursaspor",
                           "Rubin Kazan": "Рубин", "Panathinaikos": "Παναθηναϊκός", "MSK Zilina": "Zilina",
                           "Auxerre": "Auxerre", "Partizan Belgrade": "Partizan"}
        for team in team_list:
            team.name = conversion_dict[team.name]
