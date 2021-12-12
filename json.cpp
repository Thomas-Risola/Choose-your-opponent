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


void writeQS(std::vector<double>){

}
