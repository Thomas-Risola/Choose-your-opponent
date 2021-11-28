#include <iostream>
#include "tools.h"
#include "DoubleTree.h"

using namespace std;

const int N=16;

Imagine::Matrix<double> victoryMatrix(N,N);
Imagine::Matrix<bool> playMatrix(N,N);

int main()
{
    setMatrixVictory(victoryMatrix);
    setPlayMatrix(playMatrix);
    //display(victoryMatrix);
    //display(playMatrix);
    int petit_N=8;
    vector<double> qS;
    vector<int> X1,X2,ranking;
    for (int i=0;i<petit_N;i++) ranking.push_back(i);
    algorithm_entire_competition(qS,X1,X2,ranking,victoryMatrix,playMatrix);
    cout << "qS: " << qS << endl << "X1: " << X1 << endl << "X2: " << X2 << endl;
    return 0;
}
