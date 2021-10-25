#pragma once
#include <Imagine/Graphics.h>
#include "Imagine/LinAlg.h"
#include <Imagine/Graphics.h>
#include <forward_list>
#include "vectortree.h"

struct ComparePlayers {
    std::vector<int> ranking;
    ComparePlayers(const std::vector<int>& rk): ranking(rk) {}
    bool operator()(int i,int j) {
        int arg_i=0;
        int arg_j=0;
        while (arg_i<ranking.size() && ranking.at(arg_i)!=i) arg_i++;
        while (arg_j<ranking.size() && ranking.at(arg_j)!=i) arg_j++;
        return (arg_i<arg_j);
    }
};

VectorTree* empty_Q_P_N(const unsigned int N,int c_player=0);

std::vector<double> p_S(std::vector<std::vector<int>>& set_sorted_S,const std::vector<int>& X1,const std::vector<int>& X2,const Imagine::Matrix<double>& probability_matrix);

double qSj(const int j,const VectorTree* QOmega,const std::vector<int>& X1,const std::vector<int>& X2, const Imagine::Matrix<double>& probability_matrix);

void opponent_choice_optimization_algorithm(std::vector<double>& qS,std::vector<int>& XN1,std::vector<int>& XN2,VectorTree* QOmega,const std::vector<int>& ranking,const Imagine::Matrix<double>& probability_matrix);

void setMatrixVictory(Imagine::Matrix<double> &M);

void display(const Imagine::Matrix<double> &M);
