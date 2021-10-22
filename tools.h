#pragma once
#include <Imagine/Graphics.h>
#include "Imagine/LinAlg.h"
#include <Imagine/Graphics.h>
#include <forward_list>

const int N=16;


double p_S(const std::vector<bool>& S,const std::vector<int>& X1,const std::vector<int>& X2,const Imagine::Matrix<double>& probability_matrix);

void opponent_choice_algorithm(std::vector<int>& X1,std::vector<int>& X2,std::forward_list<double>& ranking,const Imagine::Matrix<double>& probability_matrix);

void setMatrixVictory(Imagine::Matrix<double> &M);

void display(const Imagine::Matrix<double> &M);
