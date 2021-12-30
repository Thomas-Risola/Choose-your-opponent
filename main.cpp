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
    vector<double> qS_semifinal;
    vector<double> qS_quarterfinal;
    vector<int> X1,X2,ranking;
    for (int i=0;i<petit_N;i++) ranking.push_back(i);
    algorithm_entire_competition(qS_win,qS_final,qS_semifinal,qS_quarterfinal,X1,X2,ranking,16,victoryMatrix,playMatrix,false);
    cout << "qS: " << qS_win << endl << "X1: " << X1 << endl << "X2: " << X2 << endl;
    cout << "qS_final: " << qS_final << endl;
    cout << "qS_semifinal: " << qS_semifinal << endl;
    cout << "qS_quarterfinal: " << qS_quarterfinal << endl;
    return 0;
}
