#include "tools.h"

double p_S(const std::vector<bool>& S,const std::vector<int>& X1,const std::vector<int>& X2,const Imagine::FMatrix<double,N,N>& probability_matrix) {
    // S: For all i, whether X1[i] wins agains X2[i]
    // This function computes P(S) given X1 and X2, under the assumption of independence
    assert(S.size()==X1.size());
    double rep=1;
    for (unsigned int i=0;i<S.size();i++) {
        int x1=X1.at(i);
        int x2=X2.at(i);
        if (x1<x2)
            rep*=probability_matrix(x1,x2);
    }
}

void opponent_choice_algorithm(std::vector<int>& X1,std::vector<int>& X2,std::deque<double>& ranking,const Imagine::FMatrix<double,N,N>& probability_matrix) {
    // X1,X2: For all i, X1[i] will play against X2[i].
    // X1.size(): Number of pairs already decided
    // probability_matrix: Matrix containing all win probabilities between players
    // ranking: players who haven't chosen yet. Read ranking[j]: Player ranked j+1 among those who haven't chosen (after execution, only the 2 last players stay in ranking)
    if (X1.size()==N/2-1) {
        X1.push_back(ranking.front());
        X2.push_back(ranking.back());
    }
    else {
        int current_player=ranking.front();
        ranking.pop_front();
    }
}
