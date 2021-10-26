#include "VectorTree.h"
#include <list>
#include <cmath>


// Create a node with given information
VectorTree::VectorTree(std::vector<double> d){
    data = d;
}

// Create a Tree with all possible scenario and the vector probability associated as the last leaf
// newData.size() == Card(S) and , numberOfPlayer = Card(Sa)
VectorTree::VectorTree(int numberOfPlayer, std::vector<double> newData){
    data = newData;

}


// Create a binaryTree with depth n where every leftChild has the vector data of his parent + leftData[n]
// and every rightChild has the vector data of his parent + rightData[n]
// newdata is the data of the first node (= empty vector usually)
VectorTree::VectorTree(int n, std::vector<double> dataLeft, std::vector<double> dataRight, std::vector<double> newData){
    data = newData;
    if(n == 1){
        std::vector<double> dataAugmentedLeft;
        std::vector<double> dataAugmentedRight;
        dataAugmentedLeft = newData;
        dataAugmentedLeft.push_back(dataLeft[n-1]);
        dataAugmentedRight = newData;
        dataAugmentedLeft.push_back(dataRight[n-1]);
        addAsLastChild(new VectorTree(dataAugmentedLeft));
        addAsLastChild(new VectorTree(dataAugmentedRight));
    }
    else{
        std::vector<double> dataAugmentedLeft;
        std::vector<double> dataAugmentedRight;
        dataAugmentedLeft = newData;
        dataAugmentedLeft.push_back(dataLeft[n-1]);
        dataAugmentedRight = newData;
        dataAugmentedLeft.push_back(dataRight[n-1]);
        addAsLastChild(new VectorTree(n-1, dataLeft, dataRight, dataAugmentedLeft));
        addAsLastChild(new VectorTree(n-1, dataLeft, dataRight, dataAugmentedRight));
    }
}



// Destruct a node and all its descendents
VectorTree::~VectorTree(){
    for(int i=0; i< nbChildren(); i++){
        delete children[i];
    }
    // lign for the verification
    // std::cout << "destruction de " << data << std::endl;
}

// Return information of this node
std::vector<double> VectorTree::getData() const{
    return data;
}

// Set information of this node
void VectorTree::setData(std::vector<double> d){
    data = d;
}

// Return the number of children of this node
int VectorTree::nbChildren() const{
    return children.size();
}

// Return the child at pos, if any (left-most child at position 0)
// Return child at position pos if pos is valid
// Throw "out of range" if pos is not valid (between 0 and nbChildren()-1)
VectorTree* VectorTree::getChild(int pos) const{
    return children.at(pos);
}

// Replace the exisiting child at pos (left-most child at position 0)
// Return child at position pos if pos is valid
// Throw "out of range" if pos is not valid (between 0 and nbChildren()-1)
void VectorTree::setChild(int pos, VectorTree* newChild){
    children.at(pos) = newChild;
}

// Add newChild as supplementary right-most child of this node
// Throw "Same tree trying to be added an infinite ammount of time"
// if newChild == this
void VectorTree::addAsLastChild(VectorTree* newChild){
    if (newChild == this){
        throw std::overflow_error("Same tree trying to be added an infinite ammount of time");
    }
    children.push_back(newChild);
}

// Remove right-most child of this node
// If children is empty throw "Empty vector"
void VectorTree::removeLastChild(){
    if (nbChildren() == 0)
        throw std::length_error("Empty vector");
    children.pop_back();

}

// To see the tree
void VectorTree::display(std::string prefix, std::string indent) const{
    std::cout << prefix ;
    for(unsigned int i=0; i<data.size(); i++)
        std::cout << data[i] << indent;
    std::cout << std::endl;
    for(int i=0; i<nbChildren(); i++){
        getChild(i)->display(prefix+indent,indent);
    }

}

// Return the depth of the deepest leaf
// on parcourt en profondeur chaque branche car de toute facon il faudra parcourir tout l'arbre pour etre sur
// de ne pas louper une feuille plus profonde
int VectorTree::maxDepth() const{
    if(nbChildren() == 0){
        return 0;
    }
    else{
        int Depth = 0;
        for(int i = 0; i<nbChildren(); i++){
                Depth = std::max(getChild(i)->maxDepth(), Depth);
        }
        return Depth+1;
    }
}

// Return the depth of the lowest leaf
// on parcourt en largeur car c'est le moyen le plus rapide de dectecter une branche sans enfant
int VectorTree::minDepth() const{
    std::list<VectorTree*> thisLevel;
    std::list<VectorTree*> nextLevel;
    int compteur = 0;
    if(nbChildren() == 0){
        return compteur;
    }
    else if(nbChildren() > 0){
        for(int i=0; i<nbChildren(); i++){
            nextLevel.push_back(getChild(i));
        }
        compteur ++;
        thisLevel = nextLevel;
        nextLevel.erase(nextLevel.begin(),nextLevel.end());
    }
    while (thisLevel.empty() == false) {
        if(thisLevel.front()->nbChildren() == 0){
            return compteur;
        }
        for(int i=0; i<thisLevel.front()->nbChildren(); i++){
            nextLevel.push_back(thisLevel.front()->getChild(i));
        }
        thisLevel.pop_front();
        if(thisLevel.empty() == true){
            compteur ++;
            thisLevel = nextLevel;
            nextLevel.erase(nextLevel.begin(),nextLevel.end());
        }
    }
    // normalement on arrive jamais jusque la mais le warning jaune m'embetait
    return 0;
}

// Return the vector data of the level;
std::vector<std::vector<double>> VectorTree::getLevel(int level){
    std::list<VectorTree*> thisLevel;
    std::list<VectorTree*> nextLevel;
    std::vector<std::vector<double>> dataLevel(std::pow(2,level));
    int compteur = 0;

    for(int i=0; i<nbChildren(); i++){
        nextLevel.push_back(getChild(i));
    }
    compteur ++;
    thisLevel = nextLevel;
    nextLevel.erase(nextLevel.begin(),nextLevel.end());
    if(compteur == level){
        for(unsigned int i=0; i<thisLevel.size();i++){
            dataLevel[i] = thisLevel.front()->getData();
            thisLevel.pop_front();
        }
        return dataLevel;
    }

    while (thisLevel.empty() == false) {
        for(int i=0; i<thisLevel.front()->nbChildren(); i++){
            nextLevel.push_back(thisLevel.front()->getChild(i));
        }
        thisLevel.pop_front();
        if(thisLevel.empty() == true){
            compteur ++;
            thisLevel = nextLevel;
            nextLevel.erase(nextLevel.begin(),nextLevel.end());
            if(compteur == level){
                int size = thisLevel.size();
                for(int i=0; i<size;i++){
                    dataLevel[i] = thisLevel.front()->getData();
                    thisLevel.pop_front();
                }
                return dataLevel;
            }
        }
    }
    // normalement on arrive jamais jusque la mais le warning jaune m'embetait
    return dataLevel;
}
