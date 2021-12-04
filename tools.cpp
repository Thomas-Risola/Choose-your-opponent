#include "tools.h"
#include "DoubleTree.h"

VectorTree* empty_Q_P_N(const unsigned int N,int c_player) {
    // Initializes the set of tournament win probabilities for each possible player set (with 0 values)
    // Each node can be read as: "Is c_player in contention? If yes, descend left, if not, descend right"
    // The final probabilities will be in the bottom leftmost leaf
    if (N!=0) {
        VectorTree* c1=empty_Q_P_N(N-1,c_player+1);
        VectorTree* c2=empty_Q_P_N(N-1,c_player+1);
        return new VectorNode(c1,c2,c_player);
    }
    else {
        std::vector<double> QS(c_player,0);
        return new VectorLeaf(QS);
    }
}

std::vector<double>& VectorTree::operator()(const std::vector<int>& sorted_S,unsigned int pos=0) {
    // Gets the probabilities for each player corresponding to the scenario sorted_S
    // Assumes sorted_S is sorted according to player ID (not ranking)
    // pos is only used for recursivity, giving it an explicit value will yield the wrong result
    if (isLeaf()) {
        assert(sorted_S.size()<=value().size());
        return value();
    }
    else {
        if (sorted_S.size()!=pos && sorted_S.at(pos)==player())
            return child(0)->operator()(sorted_S,pos+1); // Si le joueur en question joue, on regarde le cas où il est là
        else
            return child(1)->operator()(sorted_S,pos);
    }
}std::vector<double> VectorTree::operator()(const std::vector<int>& sorted_S,unsigned int pos=0) const { // idem const
    if (isLeaf()) {
        assert(sorted_S.size()<=value().size());
        return value();
    }
    else {
        if (sorted_S.size()!=pos && sorted_S.at(pos)==player())
            return child(0)->operator()(sorted_S,pos+1);
        else
            return child(1)->operator()(sorted_S,pos);
    }
}

void S_kN(std::vector<int>& S,VectorTree* tree,int k,VectorTree* QOmega,const ComparePlayers& comp,const Imagine::Matrix<double>& probability_matrix, const Imagine::Matrix<bool>& play_matrix,bool greedy) {
    // Calls the algorithm on all scenarii in tree with k players
    if (tree->isLeaf()) {if (k==0) {
        // Cas d'arrêt (appel de la fonction pour le scénario S
        std::vector<double> qS;
        std::vector<int> X1,X2;
        std::vector<int> ranking=S;
        std::sort(ranking.begin(),ranking.end(),comp);
        opponent_choice_optimization_algorithm(qS,X1,X2,QOmega,ranking,probability_matrix,play_matrix,greedy);
    }}
    else {
        // Descente dans l'arbre tout en garantissant qu'il y a k joueurs
        if (k!=0) {
            // Descente à gauche
            S.push_back(tree->player());
            S_kN(S,tree->child(0),k-1,QOmega,comp,probability_matrix,play_matrix,greedy);
            S.pop_back();
        }
        // Descente à droite
        S_kN(S,tree->child(1),k,QOmega,comp,probability_matrix,play_matrix,greedy);
    }
}

std::vector<double> p_S_rec(const DoubleTree* probaOnLeaf,std::vector<std::vector<int>>& set_sorted_S,
           const std::vector<int>& X1,const std::vector<int>& X2,std::vector<int>& current_unsorted_S,unsigned int pos=0) {
    if (probaOnLeaf->nbChildren()==0) {
        // Cas d'arrêt, on ajoute le scénario et sa probabilité à l'output
        std::vector<int> sorted_S=current_unsorted_S;
        std::sort(sorted_S.begin(),sorted_S.end()); // comparaison selon le numéro de joueur donc opérateur de comparaison implicite
        set_sorted_S.push_back(sorted_S);
        return std::vector<double>(1,probaOnLeaf->getData());
    }
    // On descend de manière récursive dans l'arbre pour parcourir les scénarios
    current_unsorted_S.push_back(X1.at(pos));
    std::vector<double> pS=p_S_rec(probaOnLeaf->getChild(0),set_sorted_S,X1,X2,current_unsorted_S,pos+1);
    current_unsorted_S.back()=X2.at(pos);
    std::vector<double> p2=p_S_rec(probaOnLeaf->getChild(1),set_sorted_S,X1,X2,current_unsorted_S,pos+1);
    current_unsorted_S.pop_back();
    for (unsigned int i=0;i<p2.size();i++)
        pS.push_back(p2.at(i)); // On concatène les probabilités
    return pS;
}

std::vector<double> p_S(std::vector<std::vector<int>>& set_sorted_S,const std::vector<int>& X1,const std::vector<int>& X2,const Imagine::Matrix<double>& probability_matrix) {
    // Fills set_sorted_S with the scenarii and returns pS with the probabilities of each scenario; the scenarii are the possible sets of winners from X1 and X2
    // set_sorted_S shall be empty as argument
    // Each scenario is sorted according to player ID

    // utile pour creer l'arbre, il faut considerer les vecteurs comme etant un multiplicateur sur les branches
    // J1 à gauche, J2 à droite
    // se referer a la classe DoubleTree pour plus d'infos
    std::vector<double> probaMatchJ1(X1.size());
    std::vector<double> probaMatchJ2(X1.size());
    for(unsigned int i=0; i<X1.size();i++){
        probaMatchJ1[i] = probability_matrix(X1.at(i),X2.at(i));
        probaMatchJ2[i] = probability_matrix(X2.at(i),X1.at(i));
    }
    // on cree un arbre avec 2^(N/2) proba qui correspondent à pS pour S in Omega(X,X')
    // c'est la collection de tous les sets de winner possibles
    DoubleTree probaOnLeaf(X1.size(),X1.size(), probaMatchJ1, probaMatchJ2, 1);
    // on recupert notre information (tout à gauche tous le set X1 a gagné, à droite le set X2)
    // chaque level correspond à un match entre X1[level] et X2[level], en haut X1[n-1] et X2[n-1]
    // tout en bas entre X1[0] et X2[0]
    std::vector<int> S_player_stack;
    return p_S_rec(&probaOnLeaf,set_sorted_S,X1,X2,S_player_stack);
}

std::vector<double> base_case_opponent_choice_optimization_algorithm_rec(
        std::vector<int>& XN1,std::vector<int>& XN2,std::vector<int>& X1,std::vector<int>& X2,
        const std::vector<int>& ranking,const VectorTree* QOmega,const std::vector<int>& XN,
        const Imagine::Matrix<double>& probability_matrix) {
    assert(ranking.size()%2 == 0);
    if(ranking.size() == 0)
        return std::vector<double>(XN.size(),0);
    X1.push_back(ranking.front()); // Construction de la solution
    X2.push_back(ranking.back());
    std::vector<double> qX;
    for (unsigned int i=0;i<XN.size();i++)
        qX.push_back(qSj(XN.at(i),QOmega,X1,X2,probability_matrix));
    XN1=X1; // Stockage des solutions
    XN2=X2;
    X1.pop_back(); // Restauration de l'intégrité de X1,X2
    X2.pop_back();
    return qX;
}

std::vector<double> opponent_choice_optimization_algorithm_rec(std::vector<int>& XN1,std::vector<int>& XN2,std::vector<int>& X1,std::vector<int>& X2,const std::vector<int>& ranking,const VectorTree* QOmega,const std::vector<int>& XN,const Imagine::Matrix<double>& probability_matrix,const Imagine::Matrix<bool>& play_matrix,bool greedy);
std::vector<double> maximization_function_optimization_algorithm(
        std::vector<int>& XN1,std::vector<int>& XN2,std::vector<int>& X1,std::vector<int>& X2,
        const std::vector<int>& ranking,const VectorTree* QOmega,const std::vector<int>& XN,
        int current_player,int ind_curr_player,
        const Imagine::Matrix<double>& probability_matrix,const Imagine::Matrix<bool>& play_matrix) {
    assert(XN.at(ind_curr_player)==current_player);
    std::vector<int> XN1_candidate;
    std::vector<int> XN2_candidate;
    std::vector<double> qXmax(XN.size(),0);
    std::vector<int> new_ranking;
    for (unsigned int i=1;i<ranking.size();i++) {
        int chosen_player=ranking.at(i); // Choix du joueur i
        if(XN.size() != 8 || play_matrix(current_player,chosen_player)) { // si on est pas a la premiere etape du tournoi !!!LE 8 EST A CHANGER!!!
            for (unsigned int j=1;j<ranking.size();j++)
                if (i!=j)
                    new_ranking.push_back(ranking.at(j)); // Contruction du ranking sans les joueurs déjà fixés
            X2.push_back(chosen_player); // Construction de la solution
            std::vector<double> qX=opponent_choice_optimization_algorithm_rec(XN1_candidate,XN2_candidate,X1,X2,new_ranking,QOmega,XN,probability_matrix,play_matrix,false);
            X2.pop_back(); // Restauration de l'intégrité de X2
            if(qXmax.at(ind_curr_player)<qX.at(ind_curr_player)) {
                XN1=XN1_candidate; // Stockage des solutions
                XN2=XN2_candidate;
                qXmax=qX;
            }
            new_ranking.clear();
        }
    }
    return qXmax;
}

std::vector<double> recursive_step_opponent_choice_optimization_algorithm_rec(
        std::vector<int>& XN1,std::vector<int>& XN2,std::vector<int>& X1,std::vector<int>& X2,
        const std::vector<int>& ranking,const VectorTree* QOmega,const std::vector<int>& XN,
        const Imagine::Matrix<double>& probability_matrix,const Imagine::Matrix<bool>& play_matrix,bool greedy) {
    if(ranking.size() == 0)
        return std::vector<double>(XN.size(),0);
    int current_player=ranking.front(); // On prend le 1er joueur
    int ind_curr_player=0;
    while (XN.at(ind_curr_player)!=current_player) ind_curr_player++; // On trouve l'indice qui correspond à ce joueur
    X1.push_back(current_player); // Construction de la solution
    std::vector<double> qX;
    if (greedy)
        ;
    else
        qX=maximization_function_optimization_algorithm(XN1,XN2,X1,X2,ranking,QOmega,XN,current_player,ind_curr_player,probability_matrix,play_matrix);
    X1.pop_back(); // Restauration de l'intégrité de X1
    return qX;
}

std::vector<double> opponent_choice_optimization_algorithm_rec(std::vector<int>& XN1,std::vector<int>& XN2,
                    std::vector<int>& X1,std::vector<int>& X2,const std::vector<int>& ranking,const VectorTree* QOmega,
                    const std::vector<int>& XN,const Imagine::Matrix<double>& probability_matrix,const Imagine::Matrix<bool>& play_matrix,bool greedy) {
    // X1,X2: For all i, X1[i] will play against X2[i]. Used only by recursion, shall be empty as argument
    // ranking: players who haven't chosen yet. Read ranking[j]: Player ranked j+1 among those who haven't chosen
    // Returns: win probabilities for each player in XN
    assert(XN.size()>=2);
    assert(X1.size()==X2.size());
    //std::cout << ranking.size() << std::endl;
    if (X1.size()==XN.size()/2-1)
        return base_case_opponent_choice_optimization_algorithm_rec(XN1,XN2,X1,X2,ranking,QOmega,XN,probability_matrix);  
    return recursive_step_opponent_choice_optimization_algorithm_rec(XN1,XN2,X1,X2,ranking,QOmega,XN,probability_matrix,play_matrix,greedy);
}

void opponent_choice_optimization_algorithm(
        std::vector<double>& qS,std::vector<int>& XN1,std::vector<int>& XN2,VectorTree* QOmega,const std::vector<int>& ranking,
        const Imagine::Matrix<double>& probability_matrix,const Imagine::Matrix<bool>& play_matrix,bool greedy) {
    // qS: Win probabilities for each player (Output)
    // XN1,XN2: Optimal matching (Output)
    // ranking: Players that play this round, must be sorted according to player RANKING
    // QOmega: Tree containing the tournament win probabilities for each player in all scenarii, will be updated
    // probability_matrix: Matrix containing all win probabilities between players
    // play_matrix: Matrix of possible match
    // greedy: true if players use a greedy algorithm to choose their opponent, false if they use the comprehensive algorithm to maximize their chances of winning the tournament
    std::vector<int> X1,X2;
    if (ranking.size()==1) {
        // S'il n'y a qu'un joueur, il a déjà gagné
        qS=std::vector<double>(1,ranking.front());
        (*QOmega)(ranking).at(ranking.front())=1;
        return;}
    // S'il y a plus de joueurs
    std::vector<int> XN(ranking);
    std::sort(XN.begin(),XN.end()); // Tri des joueurs selon leur numéro
    qS=opponent_choice_optimization_algorithm_rec(XN1,XN2,X1,X2,ranking,QOmega,XN,probability_matrix,play_matrix,greedy);
    std::vector<double>& store_qS=(*QOmega)(XN); // Enregistrement des probabilités dans QOmega
    for (unsigned int i=0;i<XN.size();i++)
        store_qS.at(XN.at(i))=qS.at(i);
}

void algorithm_entire_competition(std::vector<double>& qS,std::vector<int>& X1,std::vector<int>& X2,const std::vector<int>& ranking,
                                  const Imagine::Matrix<double>& probability_matrix, const Imagine::Matrix<bool>& play_matrix,bool greedy) {
    // qS: Tournament win probabilities for each player (Output)
    // X1,X2: Optimal pairings at each round (Output)
    // ranking: All players, must be sorted according to player RANKING (Input)
    // probability_matrix: Matrix containing all win probabilities between players (Input)
    // greedy: true if players use a greedy algorithm to choose their opponent, false if they use the comprehensive algorithm to maximize their chances of winning the tournament
    VectorTree* QOmega=empty_Q_P_N(ranking.size()); // Arbre de probabilités de victoire dans chaque scénario
    ComparePlayers comp(ranking);
    int n=log2(ranking.size());
    assert(pow(2,n)==ranking.size());assert(n>0);assert(n<5);
    std::vector<int> S;
    for (int i=0;i<n;i++)
        S_kN(S,QOmega,pow(2,i),QOmega,comp,probability_matrix,play_matrix,greedy); // Appel de l'algorithme en finale, demi finale, quart de fnale, etc. afin de remplir QOmega
    opponent_choice_optimization_algorithm(qS,X1,X2,QOmega,ranking,probability_matrix,play_matrix,greedy); // Appel de l'algorithme pour le niveau souhaité
    QOmega->display();
}

double qSj(const int j,const VectorTree* QOmega,const std::vector<int>& X1,const std::vector<int>& X2, const Imagine::Matrix<double>& probability_matrix) {
    // Computes undiscovered values of QOmega
    // Assumes all players are in X1,X2
    if(X1.size() == 1 && X2.size() == 1){
        // on est en finale
        if(j == X1.at(0))
            return probability_matrix(X1.front(),X2.front());
        else
            return probability_matrix(X2.front(),X1.front());
    }
    else{
        double sum = 0;
        std::vector<std::vector<int>> set_sorted_S;
        std::vector<double> pS
        =p_S(set_sorted_S,X1,X2,probability_matrix); // Calcul des probabilités de remporter ce match
        for(unsigned int i=0; i<pS.size(); i++)
            sum += pS.at(i)*(*QOmega)(set_sorted_S.at(i)).at(j); // Calcul des probabilités de gagner le tournoi
    return sum;
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

void display(const Imagine::Matrix<bool> &M) {
    for(int i = 0; i<M.nrow(); i++){
        std::cout << "( ";
        for(int j=0; j<M.ncol(); j++)
            std::cout << M(i,j) << " ";
        std::cout << " )" << std::endl;
    }
}


void setPlayMatrix(Imagine::Matrix<bool> &M){
    for(int i = 0; i<M.nrow(); i++)
        for(int j=0; j<M.ncol(); j++)
            M(i,j) = true;
    for(int i = 0; i<M.nrow()/4; i++)
        for(int j=0; j<M.ncol()/4; j++){
            M(i,j) = false;
            M(j,i) = false;
        }
    M(0,6) = false;
    M(6,0) = false;
}
