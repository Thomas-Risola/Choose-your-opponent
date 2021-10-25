#include "DoubleTree.h"
#include <list>
#include <cmath>


// Create a node with given information
DoubleTree::DoubleTree(double d){
    data = d;
}

// Create a binaryTree with depth n where every leftChild has the date of his parent * leftData
// and every rightChild has the date of his parent * rightData
// newdata is the data of the first node
DoubleTree::DoubleTree(int n, double dataLeft, double dataRight, double newData){
    data = newData;
    if(n == 1){
        addAsLastChild(new DoubleTree(data*dataLeft));
        addAsLastChild(new DoubleTree(data*dataRight));
    }
    else{
        addAsLastChild(new DoubleTree(n-1, dataLeft, dataRight, newData*dataLeft));
        addAsLastChild(new DoubleTree(n-1, dataLeft, dataRight, newData*dataRight));
    }
}

// Create a binaryTree with depth n where every leftChild has the date of his parent * leftData[i]
// and every rightChild has the date of his parent * rightData[i]
// newdata is the data of the first node
DoubleTree::DoubleTree(int n, std::vector<double> dataLeft, std::vector<double> dataRight, double newData){
    data = newData;
    if(n == 1){
        addAsLastChild(new DoubleTree(data*dataLeft.at(n-1)));
        addAsLastChild(new DoubleTree(data*dataRight.at(n-1)));
    }
    else{
        addAsLastChild(new DoubleTree(n-1, dataLeft, dataRight, newData*dataLeft.at(n-1)));
        addAsLastChild(new DoubleTree(n-1, dataLeft, dataRight, newData*dataRight.at(n-1)));
    }
}

// Destruct a node and all its descendents
DoubleTree::~DoubleTree(){
    for(double i=0; i< nbChildren(); i++){
        delete children[i];
    }
    // lign for the verification
    // std::cout << "destruction de " << data << std::endl;
}

// Return information of this node
double DoubleTree::getData() const{
    return data;
}

// Set information of this node
void DoubleTree::setData(double d){
    data = d;
}

// Return the number of children of this node
double DoubleTree::nbChildren() const{
    return children.size();
}

// Return the child at pos, if any (left-most child at position 0)
// Return child at position pos if pos is valid
// Throw "out of range" if pos is not valid (between 0 and nbChildren()-1)
DoubleTree* DoubleTree::getChild(double pos) const{
    return children.at(pos);
}

// Replace the exisiting child at pos (left-most child at position 0)
// Return child at position pos if pos is valid
// Throw "out of range" if pos is not valid (between 0 and nbChildren()-1)
void DoubleTree::setChild(double pos, DoubleTree* newChild){
    children.at(pos) = newChild;
}

// Add newChild as supplementary right-most child of this node
// Throw "Same tree trying to be added an infinite ammount of time"
// if newChild == this
void DoubleTree::addAsLastChild(DoubleTree* newChild){
    if (newChild == this){
        throw std::overflow_error("Same tree trying to be added an infinite ammount of time");
    }
    children.push_back(newChild);
}

// Remove right-most child of this node
// If children is empty throw "Empty vector"
void DoubleTree::removeLastChild(){
    if (nbChildren() == 0)
        throw std::length_error("Empty vector");
    children.pop_back();

}

// To see the tree
void DoubleTree::display(std::string prefix, std::string indent) const{
    std::cout << prefix ;
    std::cout << data << std::endl;
    for(double i=0; i<nbChildren(); i++){
        getChild(i)->display(prefix+indent,indent);
    }

}

// Return the depth of the deepest leaf
// on parcourt en profondeur chaque branche car de toute facon il faudra parcourir tout l'arbre pour etre sur
// de ne pas louper une feuille plus profonde
double DoubleTree::maxDepth() const{
    if(nbChildren() == 0){
        return 0;
    }
    else{
        double Depth = 0;
        for(double i = 0; i<nbChildren(); i++){
                Depth = std::max(getChild(i)->maxDepth(), Depth);
        }
        return Depth+1;
    }
}

// Return the depth of the lowest leaf
// on parcourt en largeur car c'est le moyen le plus rapide de dectecter une branche sans enfant
double DoubleTree::minDepth() const{
    std::list<DoubleTree*> thisLevel;
    std::list<DoubleTree*> nextLevel;
    double compteur = 0;
    if(nbChildren() == 0){
        return compteur;
    }
    else if(nbChildren() > 0){
        for(double i=0; i<nbChildren(); i++){
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
        for(double i=0; i<thisLevel.front()->nbChildren(); i++){
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
std::vector<double> DoubleTree::getLevel(int level){
    std::list<DoubleTree*> thisLevel;
    std::list<DoubleTree*> nextLevel;
    std::vector<double> dataLevel(std::pow(2,level));
    double compteur = 0;

    for(double i=0; i<nbChildren(); i++){
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
        for(double i=0; i<thisLevel.front()->nbChildren(); i++){
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
