#include "tools.h"

#include "DoubleTree.h"

std::vector<double> p_S(const std::vector<int>& X1,const std::vector<int>& X2,const Imagine::Matrix<double>& probability_matrix) {
    // utile pour creer l'arbre, il faut considerer les vecteurs comme etant un multiplicateur sur les branches
    // J1 à gauche, J2 à droite
    // se referer a la classe DoubleTree pour plus d'infos
    std::vector<double> pS(std::pow(2,X1.size()));
    std::vector<double> probaMatchJ1(X1.size());
    std::vector<double> probaMatchJ2(X1.size());
    for(unsigned int i=0; i<X1.size();i++){
        probaMatchJ1[i] = probability_matrix(X1.at(i),X2.at(i));
        probaMatchJ2[i] = probability_matrix(X2.at(i),X1.at(i));
    }
    // on cree un arbre avec 2^(N/2) proba qui correspondent à pS pour S in Omega(X,X')
    // c'est la collection de tous les sets de winner possibles
    DoubleTree probaOnLeaf(1, probaMatchJ1, probaMatchJ2, 1);
    // on recupert notre information (tout à gauche tous le set X1 a gagné, à droite le set X2)
    // chaque level correspond à un match entre X1[level] et X2[level], en haut X1[n-1] et X2[n-1]
    // tout en bas entre X1[0] et X2[0]
    return pS = probaOnLeaf.getLevel(X1.size());
}


void opponent_choice_optimization_algorithm(std::vector<int>& X1,std::vector<int>& X2,std::forward_list<double>& ranking,int n,std::vector<double> qS, const Imagine::Matrix<double>& probability_matrix) {
    // X1,X2: For all i, X1[i] will play against X2[i].
    // n: Total number of players this round
    // probability_matrix: Matrix containing all win probabilities between players
    // ranking: players who haven't chosen yet. Read ranking[j]: Player ranked j+1 among those who haven't chosen (after execution, only the 2 last players stay in ranking)
    assert(n>=2);
    if (X1.size()==n/2-1) {
        std::forward_list<double>::iterator pos=ranking.begin();
        X1.push_back(*pos);
        pos++;
        X2.push_back(*pos);
    }
    else {
        std::vector<double> qSa; // GROS PROBLÈME: Variable locale, perdue au niveau suivant
        int current_player=ranking.front();
        ranking.pop_front();
        std::forward_list<double>::iterator before_argmax_q_j=ranking.before_begin();
        std::forward_list<double>::iterator nxt_pos=ranking.begin();
        double qmax_j=0;
        double q_j;
        for (std::forward_list<double>::iterator pos=ranking.before_begin();nxt_pos!=ranking.end();++pos,++nxt_pos) {
            q_j = qSaj(*nxt_pos, qS, X1, X2, probability_matrix); // Utiliser nxt_pos
            if(qmax_j<q_j) {
                before_argmax_q_j=pos;
                qmax_j=q_j;
                qSa.push_back(qmax_j);
            }
        }
        nxt_pos=before_argmax_q_j;
        nxt_pos++;
        int chosen_player=*nxt_pos;
        ranking.erase_after(before_argmax_q_j);
        X1.push_back(current_player);
        X2.push_back(chosen_player);
        opponent_choice_optimization_algorithm(X1,X2,ranking,n,qSa,probability_matrix);
    }
}



// qS etape precedente (exemple finale)
// qSa etape suivante (exemple demi)
double qSaj(int j, std::vector<double>& qS, std::vector<int>& X1, std::vector<int>& X2, const Imagine::Matrix<double>& probability_matrix){
    if(X1.size() == 1 && X2.size() == 1){
        // on est en finale
        if(j == X1.at(0))
            return probability_matrix(X1.front(),X2.front());
        else
            return probability_matrix(X2.front(),X1.front());
    }
    else{
        double sum = 0;
        std::vector<double> pS;
        pS = p_S(X1, X2, probability_matrix);
        for(unsigned int i=0; i<pS.size(); i++){
            sum += pS[i]*qS[j];
            return sum;
        }
    }
}

void setDiagonalVictory(Imagine::Matrix<double> &M){
    for(int i=0; i<M.nrow(); i++){
        M(i,i) = 0;
    }
}

void setMatrixVictory(Imagine::Matrix<double> &M){
    setDiagonalVictory(M);
    // Matchup J1
    M(0,1) = 0.554;
    M(0,2) = 0.657;
    M(0,3) = 0.665;
    M(0,4) = 0.727;
    M(0,5) = 0.713;
    M(0,6) = 0.763;
    M(0,7) = 0.721;
    M(0,8) = 0.763;
    M(0,9) = 0.795;
    M(0,10) = 0.783;
    M(0,11) = 0.813;
    M(0,12) = 0.806;
    M(0,13) = 0.886;
    M(0,14) = 0.813;
    M(0,15) = 0.773;
    // Matchup J2
    M(1,2) = 0.669;
    M(1,3) = 0.690;
    M(1,4) = 0.621;
    M(1,5) = 0.630;
    M(1,6) = 0.603;
    M(1,7) = 0.670;
    M(1,8) = 0.784;
    M(1,9) = 0.650;
    M(1,10) = 0.650;
    M(1,11) = 0.844;
    M(1,12) = 0.718;
    M(1,13) = 0.833;
    M(1,14) = 0.817;
    M(1,15) = 0.773;
    // Matchup J3
    M(2,3) = 0.436;
    M(2,4) = 0.549;
    M(2,5) = 0.617;
    M(2,6) = 0.626;
    M(2,7) = 0.578;
    M(2,8) = 0.650;
    M(2,9) = 0.438;
    M(2,10) = 0.633;
    M(2,11) = 0.548;
    M(2,12) = 0.703;
    M(2,13) = 0.583;
    M(2,14) = 0.735;
    M(2,15) = 0.690;
    // Matchup J4
    M(3,4) = 0.503;
    M(3,5) = 0.506;
    M(3,6) = 0.667;
    M(3,7) = 0.636;
    M(3,8) = 0.533;
    M(3,9) = 0.750;
    M(3,10) = 0.412;
    M(3,11) = 0.538;
    M(3,12) = 0.733;
    M(3,13) = 0.593;
    M(3,14) = 0.607;
    M(3,15) = 0.815;
    // Matchup J5
    M(4,5) = 0.484;
    M(4,6) = 0.607;
    M(4,7) = 0.333;
    M(4,8) = 0.512;
    M(4,9) = 0.667;
    M(4,10) = 0.600;
    M(4,11) = 0.634;
    M(4,12) = 0.688;
    M(4,13) = 0.500;
    M(4,14) = 0.667;
    M(4,15) = 0.545;
    // Matchup J6
    M(5,6) = 0.519;
    M(5,7) = 0.560;
    M(5,8) = 0.448;
    M(5,9) = 0.567;
    M(5,10) = 0.596;
    M(5,11) = 0.643;
    M(5,12) = 0.500;
    M(5,13) = 0.560;
    M(5,14) = 0.643;
    M(5,15) = 0.722;
    // Matchup J7
    M(6,7) = 0.409;
    M(6,8) = 0.583;
    M(6,9) = 0.617;
    M(6,10) = 0.579;
    M(6,11) = 0.565;
    M(6,12) = 0.385;
    M(6,13) = 0.545;
    M(6,14) = 0.500;
    M(6,15) = 0.583;
    // Matchup J8
    M(7,8) = 0.483;
    M(7,9) = 0.532;
    M(7,10) = 0.643;
    M(7,11) = 0.379;
    M(7,12) = 0.385;
    M(7,13) = 0.455;
    M(7,14) = 0.583;
    M(7,15) = 0.706;
    // Matchup J9
    M(8,9) = 0.583;
    M(8,10) = 0.455;
    M(8,11) = 0.615;
    M(8,12) = 0.500;
    M(8,13) = 0.545;
    M(8,14) = 0.583;
    M(8,15) = 0.385;
    // Matchup J10
    M(9,10) = 0.545;
    M(9,11) = 0.706;
    M(9,12) = 0.357;
    M(9,13) = 0.545;
    M(9,14) = 0.545;
    M(9,15) = 0.583;
    // Matchup J11
    M(10,11) = 0.500;
    M(10,12) = 0.583;
    M(10,13) = 0.583;
    M(10,14) = 0.385;
    M(10,15) = 0.357;
    // Matchup J12
    M(11,12) = 0.615;
    M(11,13) = 0.667;
    M(11,14) = 0.667;
    M(11,15) = 0.357;
    // Matchup J13
    M(12,13) = 0.500;
    M(12,14) = 0.545;
    M(12,15) = 0.417;
    // Matchup J14
    M(13,14) = 0.500;
    M(13,15) = 0.500;
    // Matchup J15
    M(14,15) = 0.583;
    // Contre Matchup
    for(int i = 0; i<M.nrow(); i++)
        for(int j=0; j<i; j++)
            M(i,j) = 1 - M(j,i);
}

void display(const Imagine::Matrix<double> &M) {
    for(int i = 0; i<M.nrow(); i++){
        std::cout << "( ";
        for(int j=0; j<M.ncol(); j++)
            std::cout << M(i,j) << " ";
        std::cout << " )" << std::endl;
    }
}
