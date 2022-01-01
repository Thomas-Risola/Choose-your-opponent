# import libraries
import json
import numpy as np

class Result:
    def __init__(self, day, month, year, qs_win, qs_final, qs_semi, qs_quart, scenario, fileprefix1="json_files/team_list", fileprefix2="json_files/matrix"):
        filename1 = fileprefix1 + "-" + str(day) + "-" + str(month) + "-" + str(year) + ".txt"
        filename2 = fileprefix2 + "-" + str(day) + "-" + str(month) + "-" + str(year) + ".txt"
        self.qs_win = qs_win
        self.qs_final = qs_final
        self.qs_semi = qs_semi
        self.qs_quart = qs_quart
        self.scenario = scenario

    @staticmethod
    def get_qs(self,filename):
        return


