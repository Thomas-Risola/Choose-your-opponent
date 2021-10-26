#pragma once
#include <Imagine/Graphics.h>
#include "Imagine/LinAlg.h"
#include <Imagine/Graphics.h>
#include <forward_list>
#include <map>

const int N=16;


double p_S(const std::vector<bool>& S,const std::vector<int>& X1,const std::vector<int>& X2,const Imagine::Matrix<double>& probability_matrix);

double qSaj(int j, std::vector<double>& qS, std::vector<int>& X1, std::vector<int>& X2, const Imagine::Matrix<double>& probability_matrix);

void opponent_choice_algorithm(std::vector<int>& X1,std::vector<int>& X2,std::forward_list<double>& ranking, std::vector<double> qS, const Imagine::Matrix<double>& probability_matrix);

void setMatrixVictory(Imagine::Matrix<double> &M);

void display(const Imagine::Matrix<double> &M);

std::vector< std::vector<int> > subsetsOfSizeK(const std::vector<int>& set, unsigned int k);

std::vector<std::vector< std::vector<int>>> constructScenarios(const std::vector<int>& set);

std::vector<std::vector<int>> identifyScenario(std::vector<std::vector<std::vector<int>>> ChoiceOfSmallerSubset, std::vector<int> X1 , std::vector<int> X2);

void chooseEnFonctionDuScenario(int &iChoosed, const int& playerWhoChoose, const int &i, std::vector<std::vector<std::vector<int>>> &ChoiceOfSmallerSubset, std::vector<int> X1, std::vector<int> X2, std::vector<double> QOmega, const Imagine::Matrix<double>& probability_matrix);

void identifyScenarioToSupress(const std::vector<int> &X1, const std::vector<int> &X2, std::vector<std::vector<std::vector<int>>> &ChoiceOfSmallerSubset, const int &iChoosed, const int &playerWhoChoose);

