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
    int petit_N=4;
    vector<double> qS;
    vector<int> X1,X2,ranking;
    for (int i=0;i<petit_N;i++) ranking.push_back((2+i)%petit_N);
    algorithm_entire_competition(qS,X1,X2,ranking,victoryMatrix);
    return 0;
}
