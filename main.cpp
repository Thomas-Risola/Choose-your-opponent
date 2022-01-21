#include <iostream>
#include "tools.h"
#include "DoubleTree.h"
#include "json.h"


using namespace std;
using json = nlohmann::json;


int main()
{
    for(int year = 2021; year<2022; year++){
    //int year;
    bool fast = true;
    //getTDLOG_info(year,fast);
    string fileName;
    getFileName(year,fileName);
    string matrixName = getMatrixFileName(fileName);
    string official16Name = getOfficial16FileName(fileName);
    Imagine::Matrix<double> victoryMatrix = getVictoryMatrix(ifstream(matrixName));
    Imagine::Matrix<bool> playMatrix = getPlayMatrix(ifstream(matrixName));
    int petit_N=16;
    vector<double> qS_win;
    vector<double> qS_final;
    vector<double> qS_semifinal;
    vector<double> qS_quarterfinal;
    vector<double> qS_liste_result(6);

    vector<vector<int>> Liste_X1,Liste_X2;
    vector<int> X1,X2,ranking;
    for (int i=0;i<petit_N;i++) ranking.push_back(i);
    algorithm_entire_competition(qS_win,qS_final,qS_semifinal,qS_quarterfinal,qS_liste_result,Liste_X1,Liste_X2,X1,X2,ranking,16,victoryMatrix,playMatrix,false);
    writeQS(qS_win,qS_final,qS_semifinal,qS_quarterfinal,qS_liste_result,fileName);
    //writeScenario(Liste_X1,Liste_X2,fileName,victoryMatrix,playMatrix);
    readWriteOfficialScenarioV2(ifstream(official16Name), fileName, fast, victoryMatrix);
}
    return 0;
}
