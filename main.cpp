#include <iostream>
#include "tools.h"
#include "DoubleTree.h"
#include "json.h"


using namespace std;
using json = nlohmann::json;


int main()
{
    int year = 2021;
    // a coder?
    // cin >> year;
    string fileName;
    getFileName(year,fileName);
    string matrixName = getMatrixFileName(fileName);
    Imagine::Matrix<double> victoryMatrix = getVictoryMatrix(ifstream(matrixName));
    Imagine::Matrix<bool> playMatrix = getPlayMatrix(ifstream(matrixName));
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
    cout << endl << "calculs finis" << endl;
    cout << "qS_win: " << qS_win << endl;

    //X1 = {0,1,2,3,4,5,6,7};
    //X2 = {13,14,12,9,10,15,11,8};
    writeQS(qS_win,qS_final,qS_semifinal,qS_quarterfinal,fileName);
    //writeScenario(X1,X2,fileName,victoryMatrix,playMatrix);
    return 0;
}
