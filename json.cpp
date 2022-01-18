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


void writeQS(std::vector<double> qS_win,std::vector<double> qS_final,std::vector<double> qS_semi,std::vector<double> qS_quart,std::vector<double> qS_liste, std::string fileName){
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

    json js2;
    js2 = {
        {"best_final_elo", qS_liste[0]},
        {"best_final_weak", qS_liste[1]},
        {"best_quart_elo", qS_liste[2]},
        {"best_quart_weak", qS_liste[3]},
        {"best_semi_elo", qS_liste[4]},
        {"best_semi_weak", qS_liste[5]}
    };

    {
        std::string prefix2 = srcPath("json_files/best_scenario-");
        std::string qSFileName2 = prefix2 + fileName;
        std::ofstream f2(qSFileName2);
        f2 << js2;
    }
}

void writeScenario(std::vector<std::vector<int>> Liste_X1,std::vector<std::vector<int>> Liste_X2, std::string fileName, const Imagine::Matrix<double>& probability_matrix, const Imagine::Matrix<bool>& play_matrix){
    json js;
    json scenario;
    std::vector<std::string> round = {"quart","semi","final","winner"};
    scenario = {
        {"X1",Liste_X1.back()},
        {"X2",Liste_X2.back()},
    };
    std::vector<json> list_scenario = {scenario};
    std::vector<json> list_scenario_quart;
    std::vector<json> list_scenario_semi;
    std::vector<json> list_scenario_final;
    size_t quart_size = 4;
    size_t semi_size = 2;
    size_t final_size = 1;

    for (size_t i=0; i<Liste_X1.size() ; i++) {;
        scenario = {
            {"X1",Liste_X1.at(i)},
            {"X2",Liste_X2.at(i)},
        };
        if (Liste_X1[i].size() == quart_size) {
            list_scenario_quart.push_back(scenario);
        }
        else if (Liste_X1[i].size() == semi_size) {
            list_scenario_semi.push_back(scenario);
        }
        else if (Liste_X1[i].size() == final_size) {
            list_scenario_final.push_back(scenario);
        }
    }
    js =
    {
        {"round_of_16",list_scenario},
        {"quart", list_scenario_quart},
        {"semi", list_scenario_semi},
        {"final", list_scenario_final},
    };



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

std::string getOfficial16FileName(std::string fileName){
    std::string prefix = srcPath("json_files/round_of_16_official-");
    std::string Official16FileName = prefix + fileName;
    return Official16FileName;
}

void getTDLOG_info(int &year, bool &fast){
    std::string file = srcPath("json_files/execute_info.txt");
    json j = json::parse(std::ifstream(file));
    year = j["year"];
    fast = j["fast"];

}

void readWriteOfficialScenario(std::ifstream inFileName, std::string outFileName, const Imagine::Matrix<double>& probability_matrix){
    json js = json::parse(inFileName);
    json scenario;
    std::vector<std::string> round_before_draw = {"quart_before_draw","semi_before_draw","final_before_draw","winner_before_draw"};
    std::vector<std::string> round = {"quart","semi","final","winner"};

    std::vector<json> list_scenario = {js["round_of_16"][0]};

    std::vector<double> qS_quart(16,0);
    std::vector<double> qS_semi(16,0);
    std::vector<double> qS_final(16,0);
    std::vector<double> qS_win(16,0);

    std::vector<json> list_scenario_next_round;
    for(int i=0; i<3; i++){
        // scenario possible
        for(size_t j=0; j<list_scenario.size(); j++){
            std::vector<std::vector<int>> set_sorted_S;
            std::vector<int> XN1 = list_scenario[j]["X1"];
            std::vector<int> XN2 = list_scenario[j]["X2"];
            std::vector<double> pS = p_S(set_sorted_S,XN1,XN2,probability_matrix);
            for(size_t k=0; k<pS.size(); k++){
                double proba = list_scenario[j]["proba"];
                proba *= pS[k] ;
                if(i < 2){
                    scenario ={
                        {"proba",proba},
                        {"winners",set_sorted_S[k]},
                    };
                    list_scenario_next_round.push_back(scenario);
                }
                if(i==0)
                    for(size_t l=0; l<16; l++)
                        if(std::find(set_sorted_S[k].begin(), set_sorted_S[k].end(), l) != set_sorted_S[k].end())
                            qS_quart[l] += proba;
                if(i==1)
                    for(size_t l=0; l<16; l++)
                        if(std::find(set_sorted_S[k].begin(), set_sorted_S[k].end(), l) != set_sorted_S[k].end())
                            qS_semi[l] += proba;
                if(i==2)
                    for(size_t l=0; l<16; l++)
                        if(std::find(set_sorted_S[k].begin(), set_sorted_S[k].end(), l) != set_sorted_S[k].end()){
                            qS_final[l] += proba;
                            if(set_sorted_S[k][0] != l)
                                qS_win[l] += proba*probability_matrix(l,set_sorted_S[k][0]);
                            else
                                qS_win[l] += proba*probability_matrix(l,set_sorted_S[k][0]);
                        }
            }
        }
        std::cout << "nombre de scenarios en cours de calcul: " << list_scenario_next_round.size() << std::endl;
        list_scenario = list_scenario_next_round;
        list_scenario_next_round = {};
        // tirage au sort du next round
        for(size_t j=0; j<list_scenario.size(); j++){
            std::vector<int> XN = list_scenario[j]["winners"];
            std::vector<std::vector<std::vector<int>>> X1X2;
            X1X2 = draw_round(XN);
            for(size_t k=0; k<X1X2.size(); k++){
                double size = X1X2.size();
                double proba = list_scenario[j]["proba"];
                proba *= 1/size;
                scenario ={
                    {"proba",proba},
                    {"X1",X1X2[k][0]},
                    {"X2",X1X2[k][1]},
                };
                list_scenario_next_round.push_back(scenario);
            }
        }
        list_scenario = list_scenario_next_round;
        list_scenario_next_round = {};
        std::cout << "nombre de scenarios en cours de calcul: " << list_scenario.size() << std::endl;
    }

    js = {
        {"qs_win",qS_win},
        {"qs_final",qS_final},
        {"qs_semi",qS_semi},
        {"qs_quart",qS_quart},
    };

    std::string prefix = srcPath("json_files/official_qs_vector-");
    std::string qSFileName = prefix + outFileName;
    std::ofstream f(qSFileName);
    f << js;

}




void readWriteOfficialScenarioV2(std::ifstream inFileName, std::string outFileName, bool fast, const Imagine::Matrix<double>& probability_matrix){
    // proba_winner_x = proba d'arrive au stade x
    json js = json::parse(inFileName);
    json scenario;
    std::vector<std::string> round_before_draw = {"quart_before_draw","semi_before_draw","final_before_draw","winner_before_draw"};
    std::vector<std::string> round = {"quart","semi","final","winner"};

    std::vector<json> list_scenario_huitieme = js["round_of_16"];
    std::vector<json> list_winner_quart;
    std::vector<json> list_scenario_quart;
    std::vector<json> list_winner_demi;
    std::vector<json> list_scenario_demi;

    std::vector<double> qS_quart(16,0);
    std::vector<double> qS_semi(16,0);
    std::vector<double> qS_final(16,0);
    std::vector<double> qS_win(16,0);

    double best_final_elo = 0;
    double best_final_weak_ranking = 0;

    double best_semi_elo = 0;
    double best_semi_weak_ranking = 0;

    double best_quart_elo = 0;
    double best_quart_weak_ranking = 0;

    size_t taille = list_scenario_huitieme.size();
    double constante = 1;

    if(fast==true){
        taille = 10;
        constante = 100;
    }

    // huitième tiré
    std::cout << list_scenario_huitieme.size() << std::endl;
    for(size_t j=0; j<taille; j++){
        std::cout << j << std::endl;
        std::vector<std::vector<int>> set_sorted_S_huitieme;
        std::vector<int> XN1_huitieme = list_scenario_huitieme[j]["X1"];
        std::vector<int> XN2_huitieme = list_scenario_huitieme[j]["X2"];
        std::vector<double> pS = p_S(set_sorted_S_huitieme,XN1_huitieme,XN2_huitieme,probability_matrix);
        // huitième joué
        for(size_t k=0; k<pS.size(); k++){

            double proba_winner_quart = list_scenario_huitieme[j]["proba"];
            proba_winner_quart *= pS[k]*constante;
            for(size_t i=0; i<16; i++)
                if(std::find(set_sorted_S_huitieme[k].begin(), set_sorted_S_huitieme[k].end(), i) != set_sorted_S_huitieme[k].end())
                    qS_quart[i] += proba_winner_quart;
            std::vector<std::vector<std::vector<int>>> X1X2_quart;
            X1X2_quart = draw_round(set_sorted_S_huitieme[k]);
            double size = X1X2_quart.size();
            double proba_quart = proba_winner_quart;
            proba_quart *= 1/size;
            std::vector<std::vector<int>> set_sorted_S_quart;
            // quart tiré
            for(size_t l=0; l<X1X2_quart.size(); l++){
                std::vector<int> XN1_quart = X1X2_quart[l][0];
                std::vector<int> XN2_quart = X1X2_quart[l][1];
                std::vector<double> pS_quart = p_S(set_sorted_S_quart,XN1_quart,XN2_quart,probability_matrix);
                // quart joué
                for(size_t o=0; o<pS_quart.size(); o++){
                    //std::cout << "test" << std::endl;
                    double proba_winner_semi = proba_quart;
                    proba_winner_semi *= pS_quart[o];
                    for(size_t i=0; i<16; i++)
                        if(std::find(set_sorted_S_quart[o].begin(), set_sorted_S_quart[o].end(), i) != set_sorted_S_quart[o].end())
                            qS_semi[i] += proba_winner_semi;
                    std::vector<std::vector<std::vector<int>>> X1X2_semi;
                    X1X2_semi = draw_round(set_sorted_S_quart[o]);
                    double size_semi = X1X2_semi.size();
                    double proba_semi = proba_winner_semi;
                    proba_semi *= 1/size_semi;
                    std::vector<std::vector<int>> set_sorted_S_semi;
                    // semi tiré
                    for(size_t m=0; m<X1X2_semi.size(); m++){
                        //std::cout << "testsemi" << std::endl;
                        std::vector<int> XN1_semi = X1X2_semi[m][0];
                        std::vector<int> XN2_semi = X1X2_semi[m][1];
                        std::vector<double> pS_semi = p_S(set_sorted_S_semi,XN1_semi,XN2_semi,probability_matrix);
                        // semi joué
                        for(size_t n=0; n<pS_semi.size(); n++){
                            //std::cout << "testwin" << std::endl;
                            double proba_winner_final = proba_semi;
                            proba_winner_final *= pS_semi[n];
                            for(size_t i=0; i<16; i++)
                                if(set_sorted_S_semi[n][0] == i || set_sorted_S_semi[n][1] == i){
                                    qS_final[i] += proba_winner_final;
                                    if(set_sorted_S_semi[n][0] != i)
                                        qS_win[i] += proba_winner_final*probability_matrix(i,set_sorted_S_semi[n][0]);
                                    else
                                        qS_win[i] += proba_winner_final*probability_matrix(set_sorted_S_semi[n][1],i);
                                }
                            if(set_sorted_S_semi[n][0] == 0 || set_sorted_S_semi[n][1] == 1)
                                best_final_weak_ranking += proba_winner_final;
                            //if(set_sorted_S_semi[n][0] == std::min(elo_ranking[0], elo_ranking[1]) || set_sorted_S_semi[n][1] == std::max(elo_ranking[0], elo_ranking[1]))
                            //    best_final_elo += proba_winner_final;
                        }
                    }
                }
            }
        }

    }


    js = {
        {"qs_win",qS_win},
        {"qs_final",qS_final},
        {"qs_semi",qS_semi},
        {"qs_quart",qS_quart},
    };


    json js2 = {
        {"best_final_weak", best_final_weak_ranking},
        {"best_final_elo", best_final_elo},
        {"best_semi_weak", best_semi_weak_ranking},
        {"best_semi_elo", best_semi_elo},
        {"best_quart_weak", best_quart_weak_ranking},
        {"best_quart_elo", best_quart_elo},

    };

    std::string prefix1 = srcPath("json_files/official_qs_vector-");
    std::string qSFileName1 = prefix1 + outFileName;
    std::ofstream f1(qSFileName1);
    f1 << js;

    std::string prefix2 = srcPath("json_files/official_best_scenario-");
    std::string qSFileName2 = prefix2 + outFileName;
    std::ofstream f2(qSFileName2);
    f2 << js2;

}

