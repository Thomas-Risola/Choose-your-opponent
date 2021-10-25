#include <iostream>
#include "tools.h"
#include "DoubleTree.h"

using namespace std;

const int N=16;

Imagine::Matrix<double> victoryMatrix(N,N);

int main()
{
    setMatrixVictory(victoryMatrix);
    //display(victoryMatrix);
    //const std::vector<int>& XN,const Rank& comp,const Imagine::Matrix<double>& probability_matrix)
    int petit_N=8;
    std::vector<double> qS;
    std::vector<int> X1,X2;
    VectorTree* QOmega=empty_Q_P_N(petit_N);
    std::vector<int> ranking;
    for (int i=0;i<petit_N;i++) ranking.push_back((1+i)%petit_N);
    opponent_choice_optimization_algorithm(qS,X1,X2,QOmega,ranking,victoryMatrix); // On ne récupère jamais nlig ou ncol, donc pas besoin de découper victoryMatrix
    cout << "X1: " << X1 << endl;
    cout << "X2: " << X2 << endl;
    cout << "qS: " << qS << endl;
    return 0;
}
