# import libraries
import json


class Result:
    def __init__(self, day, month, fileprefix1="json_files/qs_vector", fileprefix2="json_files/scenario",
                 fileprefix3="json_files/official_qs_vector", fileprefix4="json_files/best_scenario",
                 fileprefix5="json_files/official_best_scenario"):
        self.qs_year = dict()
        self.scenario_year = dict()
        self.official_qs_year = dict()
        self.best_scenario_year = dict()
        self.official_best_scenario_year = dict()
        for year in range(2010, 2022):
            try:
                filename1 = fileprefix1 + "-" + str(day) + "-" + str(month) + "-" + str(year) + ".txt"
                filename2 = fileprefix2 + "-" + str(day) + "-" + str(month) + "-" + str(year) + ".txt"
                filename3 = fileprefix3 + "-" + str(day) + "-" + str(month) + "-" + str(year) + ".txt"
                filename4 = fileprefix4 + "-" + str(day) + "-" + str(month) + "-" + str(year) + ".txt"
                filename5 = fileprefix5 + "-" + str(day) + "-" + str(month) + "-" + str(year) + ".txt"
                self.qs_year[year] = self.get_qs(filename1)
                self.scenario_year[year] = self.get_scenario(filename2)
                self.official_qs_year[year] = self.get_qs(filename3)
                self.best_scenario_year[year] = self.get_best_scenario(filename4)
                self.official_best_scenario_year[year] = self.get_best_scenario(filename5)
            except:
                continue

    @staticmethod
    def get_qs(filename):
        file = open(filename, 'r', encoding="utf-8")
        dict_list = json.load(file)
        qs_win = dict_list["qs_win"]
        qs_final = dict_list["qs_final"]
        qs_semi = dict_list["qs_semi"]
        qs_quart = dict_list["qs_quart"]
        file.close()
        return [qs_win, qs_final, qs_semi, qs_quart]

    @staticmethod
    def get_scenario(filename):
        file = open(filename, 'r', encoding="utf-8")
        dict_list = json.load(file)
        round_of_16 = dict_list["round_of_16"]
        quart = dict_list["quart"]
        semi = dict_list["semi"]
        final = dict_list["final"]
        file.close()
        return [final, semi, quart, round_of_16]

    @staticmethod
    def get_best_scenario(filename):
        file = open(filename, 'r', encoding="utf-8")
        dict_list = json.load(file)
        final_elo = dict_list["best_final_elo"]
        final_weak = dict_list["best_final_weak"]
        quart_elo = dict_list["best_quart_elo"]
        quart_weak = dict_list["best_quart_weak"]
        semi_elo = dict_list["best_semi_elo"]
        semi_weak = dict_list["best_semi_weak"]
        file.close()
        return [final_elo, final_weak, semi_elo, semi_weak, quart_elo, quart_weak]


