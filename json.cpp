#include <iostream>


#include "json.h"
using json = nlohmann::json;


Imagine::Matrix<double> getVictoryMatrix(std::ifstream file){
    json j = json::parse(file);
    std::vector<std::vector<double>> v_matrix = j[0]["victory_matrix"];
    int N = j[0]["victory_matrix"].size();
    Imagine::Matrix<double> M(N,N);
    for(int i=0; i<M.nrow(); i++)
        for(int j=0; j<M.ncol(); j++)
            M(i,j) = v_matrix[i][j];
    return M;
}



Imagine::Matrix<bool> getPlayMatrix(std::ifstream file){
    json j = json::parse(file);
    std::vector<std::vector<bool>> p_matrix = j[0]["play_matrix"];
    int N = j[0]["victory_matrix"].size();
    Imagine::Matrix<bool> M(N,N);
    for(int i=0; i<M.nrow(); i++)
        for(int j=0; j<M.ncol(); j++){
            if(p_matrix[i][j])
                M(i,j) = true;
            else
                M(i,j) = false;
        }
    return M;
}


void writeQS(std::vector<double> qS_win,std::vector<double> qS_final,std::vector<double> qS_semi,std::vector<double> qS_quart, std::string fileName){
    json js;
    js = {
        {"qs_win",qS_win},
        {"qs_final",qS_final},
        {"qs_semi",qS_semi},
        {"qs_quart",qS_quart},
    };

    {
        std::string prefix = srcPath("json_files/qs_vector-");
        std::string qSFileName = prefix + fileName;
        std::ofstream f(qSFileName);
        f << js;
    }
}

void writeScenario(std::vector<int> X1,std::vector<int> X2, std::string fileName, const Imagine::Matrix<double>& probability_matrix, const Imagine::Matrix<bool>& play_matrix){
    json js;
    json scenario;
    std::vector<std::string> round = {"quart","semi","final","winner"};
    std::vector<std::vector<int>> set_sorted_S = {X1,X2};
    scenario ={
        {"proba",1},
        {"X1",X1},
        {"X2",X2},
        {"parent",0}
    };
    std::vector<json> list_scenario = {scenario};
    std::vector<json> list_scenario_next_round;
    js = {"round_of_16",scenario};
    for(int i=0; i<3; i++){
        for(size_t j=0; j<list_scenario.size(); j++){
            std::vector<std::vector<int>> set_sorted_S;
            std::vector<int> XN1 = list_scenario[j]["X1"];
            std::vector<int> XN2 = list_scenario[j]["X2"];
            std::vector<double> pS = p_S(set_sorted_S,XN1,XN2,probability_matrix);
            std::vector<double> qS;
            std::vector<double> dummy1;
            std::vector<double> dummy2;
            std::vector<double> dummy3;
            std::cout << "i: " << i << "j: " << j << std::endl;
            for(size_t k=0; k<pS.size(); k++){
                //std::cout << k;
                std::cout <<set_sorted_S[k];
                algorithm_entire_competition(qS,dummy1,dummy2,dummy3,XN1,XN2,set_sorted_S[k],16,probability_matrix,play_matrix);
                scenario ={
                    {"proba",pS[k]},
                    {"X1",XN1},
                    {"X2",XN2},
                    {"parent",j}
                };
                list_scenario_next_round.push_back(scenario);

            }


        }
        list_scenario = list_scenario_next_round;
        js = {round[i],list_scenario};
    }



    {
        std::string prefix = srcPath("json_files/scenario-");
        std::string qSFileName = prefix + fileName;
        std::ofstream f(qSFileName);
        f << js;
    }
}


int getFileName(int year, std::string &fileName){
    std::string strYear = std::to_string(year);
    DIR *dir; struct dirent *diread;
        std::vector<char *> files;
        //std::cout << srcPath("json_files/") << std::endl;
        if ((dir = opendir(srcPath("json_files/"))) != nullptr) {
            while ((diread = readdir(dir)) != nullptr) {
                std::cout << diread->d_name <<"|";
                files.push_back(diread->d_name);
                std::string name = diread->d_name;
                if(name[name.size()-8] == strYear[0]
                        && name[name.size()-7] == strYear[1]
                        && name[name.size()-6] == strYear[2]
                        && name[name.size()-5] == strYear[3] ){
                    fileName = name.substr(name.size()-14);
                    closedir (dir);
                    return EXIT_SUCCESS;
                }

            }
            closedir (dir);
            std::cout << std::endl;
        } else {
            perror ("opendir");
            return EXIT_FAILURE;
        }

        for (auto file : files) std::cout << file << "| ";
        std::cout << std::endl;

        return EXIT_SUCCESS;
}

std::string getMatrixFileName(std::string fileName){
    std::string prefix = srcPath("json_files/matrix-");
    std::string matrixFileName = prefix + fileName;
    return matrixFileName;
}



void readWriteOfficialScenario(std::ifstream inFileName, std::string outFileName, const Imagine::Matrix<double>& probability_matrix, const Imagine::Matrix<bool>& play_matrix){
    json j = json::parse(inFileName);
    std::vector<std::vector<double>> v_matrix = j[0]["victory_matrix"];
    int N = j[0]["victory_matrix"].size();
    Imagine::Matrix<double> M(N,N);
    for(int i=0; i<M.nrow(); i++)
        for(int j=0; j<M.ncol(); j++)
            M(i,j) = v_matrix[i][j];

    json js;
    json scenario;
    std::vector<std::string> round = {"quart","semi","final","winner"};
    std::vector<std::vector<int>> set_sorted_S = {{},{}};
    scenario ={
        {"proba",1},
        {"X1",0},
        {"X2",0},
        {"parent",0}
    };
    std::vector<json> list_scenario = {scenario};
    std::vector<json> list_scenario_next_round;
    js = {"round_of_16",scenario};
    for(int i=0; i<3; i++){
        for(size_t j=0; j<list_scenario.size(); j++){
            std::vector<std::vector<int>> set_sorted_S;
            std::vector<int> XN1 = list_scenario[j]["X1"];
            std::vector<int> XN2 = list_scenario[j]["X2"];
            std::vector<double> pS = p_S(set_sorted_S,XN1,XN2,probability_matrix);
            std::vector<double> qS;
            std::vector<double> dummy1;
            std::vector<double> dummy2;
            std::vector<double> dummy3;

            for(size_t k=0; k<pS.size(); k++){
                std::vector<int> XNN1;
                std::vector<int> XNN2;
                for(size_t l=0; l<set_sorted_S[k].size()/2; l++){
                    XNN1.push_back(set_sorted_S[k][2*l]);
                    XNN2.push_back(set_sorted_S[k][2*l+1]);
                }
                scenario ={
                    {"proba",pS[k]},
                    {"X1",XNN1},
                    {"X2",XNN2},
                    {"parent",j}
                };
                list_scenario_next_round.push_back(scenario);

            }


        }
        list_scenario = list_scenario_next_round;
        js = {round[i],list_scenario};
    }



    {
        std::string prefix = srcPath("json_files/scenario_officiel-");
        std::string qSFileName = prefix + outFileName;
        std::ofstream f(qSFileName);
        f << js;
    }
}
