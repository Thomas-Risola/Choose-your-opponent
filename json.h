#pragma once
#include <iostream>
#include <fstream>
#include <dirent.h>
#include <Imagine/Graphics.h>
#include "Imagine/LinAlg.h"
#include <Imagine/Graphics.h>
#include "json-develop/single_include/nlohmann/json.hpp"
#include "tools.h"
#include "official.h"


Imagine::Matrix<double> getVictoryMatrix(std::ifstream file);

Imagine::Matrix<bool> getPlayMatrix(std::ifstream file);

void writeQS(std::vector<double> qS_win,std::vector<double> qS_final,std::vector<double> qS_semi,std::vector<double> qS_quart, std::string fileName);

void writeScenario(std::vector<std::vector<int>> Liste_X1,std::vector<std::vector<int>> Liste_X2, std::string fileName, const Imagine::Matrix<double>& probability_matrix, const Imagine::Matrix<bool>& play_matrix);

int getFileName(int year, std::string &fileName);

std::string getMatrixFileName(std::string fileName);

std::string getOfficial16FileName(std::string fileName);

void readWriteOfficialScenarioV2(std::ifstream inFileName, std::string outFileName, const Imagine::Matrix<double>& probability_matrix);

