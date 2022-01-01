# import libraries
import json


class Result:
    def __init__(self, day, month, year, fileprefix1="json_files/qs_vector", fileprefix2="json_files/matrix"):
        filename1 = fileprefix1 + "-" + str(day) + "-" + str(month) + "-" + str(year) + ".txt"
        filename2 = fileprefix2 + "-" + str(day) + "-" + str(month) + "-" + str(year) + ".txt"
        self.qs_win, self.qs_final, self.qs_semi, self.qs_quart = self.get_qs(filename1)
        self.scenario = self.get_scenario(filename2)

    @staticmethod
    def get_qs(filename):
        file = open(filename, 'r', encoding="utf-8")
        dict_list = json.load(file)
        qs_win = dict_list["qs_win"]
        qs_final = dict_list["qs_final"]
        qs_semi = dict_list["qs_semi"]
        qs_quart = dict_list["qs_quart"]
        file.close()
        return qs_win, qs_final, qs_semi, qs_quart

    @staticmethod
    def get_scenario(filename):
        file = open(filename, 'r', encoding="utf-8")
        dict_list = json.load(file)

        file.close()
        return []
