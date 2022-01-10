#pragma once
#include <Imagine/Graphics.h>
#include "Imagine/LinAlg.h"
#include <Imagine/Graphics.h>
#include "vectortree.h"


struct ComparePlayers {
    std::vector<int> inv_ranking;
    ComparePlayers(const std::vector<int>& ranking): inv_ranking(ranking.size()) {
        for (unsigned int i=0;i<ranking.size();i++)
            inv_ranking.at(ranking.at(i))=i;}
    bool operator()(int i,int j) {return (inv_ranking.at(i)<inv_ranking.at(j));}
};

VectorTree* empty_Q_P_N(const unsigned int N,int c_player=0);

std::vector<double> p_S(std::vector<std::vector<int>>& set_sorted_S,const std::vector<int>& X1,const std::vector<int>& X2,const Imagine::Matrix<double>& probability_matrix);

double qSj_win(const int j,const VectorTree* QOmega_win,const std::vector<int>& X1,const std::vector<int>& X2, const Imagine::Matrix<double>& probability_matrix);

double qSj_final(const int j,const VectorTree* QOmega_final,const std::vector<int>& X1,const std::vector<int>& X2, const Imagine::Matrix<double>& probability_matrix);

double qSj_semifinal(const int j,const VectorTree* QOmega_semifinal,const std::vector<int>& X1,const std::vector<int>& X2, const Imagine::Matrix<double>& probability_matrix);

double qSj_quarterfinal(const int j,const VectorTree* QOmega_quarterfinal,const std::vector<int>& X1,const std::vector<int>& X2, const Imagine::Matrix<double>& probability_matrix);

void opponent_choice_optimization_algorithm(std::vector<double>& qS,std::vector<double>& qS_final,std::vector<double>& qS_semifinal,std::vector<double>& qS_quarterfinal,std::vector<int>& XN1,std::vector<int>& XN2,VectorTree* QOmega_win,VectorTree* QOmega_final,VectorTree* QOmega_semifinal,VectorTree* QOmega_quarterfinal,const std::vector<int>& ranking,const int nb_player_first_round,const Imagine::Matrix<double>& probability_matrix,const Imagine::Matrix<bool>& play_matrix,bool greedy);

void algorithm_entire_competition(std::vector<double>& qS,std::vector<double>& qS_final,std::vector<double>& qS_semifinal,std::vector<double>& qS_quarterfinal,std::vector<std::vector<int>>& Liste_X1,std::vector<std::vector<int>>& Liste_X2,std::vector<int>& X1,std::vector<int>& X2,const std::vector<int>& ranking,const int nb_player_first_round,const Imagine::Matrix<double>& probability_matrix, const Imagine::Matrix<bool>& play_matrix,bool greedy);

void setMatrixVictory(Imagine::Matrix<double> &M);

void display(const Imagine::Matrix<double> &M);

void display(const Imagine::Matrix<bool> &M);

void setPlayMatrix(Imagine::Matrix<bool> &M);
