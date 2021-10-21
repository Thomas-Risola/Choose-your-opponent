#include <iostream>
#include "tools.h"


using namespace std;

const int N = 16;
Imagine::Matrix<double> victoryMatrix(N,N);

int main()
{

    setMatrixVictory(victoryMatrix);
    display(victoryMatrix);
    return 0;
}
