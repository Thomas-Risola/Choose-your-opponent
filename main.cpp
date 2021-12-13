#include <iostream>
#include "tools.h"
#include "DoubleTree.h"
#include "json.h"


using namespace std;
using json = nlohmann::json;


int main()
{
    Imagine::Matrix<double> victoryMatrix = getVictoryMatrix(ifstream(srcPath("json_files/matrix-12-11-2021.txt")));
    Imagine::Matrix<bool> playMatrix = getPlayMatrix(ifstream(srcPath("json_files/matrix-12-11-2021.txt")));
    //setMatrixVictory(victoryMatrix);
    //setPlayMatrix(playMatrix);
    //display(victoryMatrix);
    //display(playMatrix);
    int petit_N=16;
    vector<double> qS;
    vector<int> X1,X2,ranking;
    for (int i=0;i<petit_N;i++) ranking.push_back(i);
    algorithm_entire_competition(qS,X1,X2,ranking,victoryMatrix,playMatrix,false);
    cout << "qS: " << qS << endl << "X1: " << X1 << endl << "X2: " << X2 << endl;
    return 0;
}
