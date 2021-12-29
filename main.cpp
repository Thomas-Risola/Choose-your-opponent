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
    vector<double> qS_win;
    vector<double> qS_final;
    vector<int> X1,X2,ranking;
    for (int i=0;i<petit_N;i++) ranking.push_back(i);
    algorithm_entire_competition(qS_win,X1,X2,ranking,petit_N,victoryMatrix,playMatrix,false);
    cout << "qS: " << qS_win << endl << "X1: " << X1 << endl << "X2: " << X2 << endl;
    cout << "qS: " << qS_final << endl;
    return 0;
}
