#pragma once
#include <vector>
#include <stdexcept>
#include <iostream>

template <typename T> std::ostream& operator<<(std::ostream& flux,std::vector<T> v) {
    for (unsigned int i=0;i<v.size();i++)
        flux << v.at(i) << ' ';
    flux << ' ';
    return flux;
}

// Cette classe réutilise du code du TP zipimage © Renaud Marlet 2011-2018

// Arbre binaire de vecteurs de double
class VectorTree {
public:
    virtual ~VectorTree()=default;

    // Tell if this tree is a leaf
    virtual bool isLeaf() const = 0;

    // Tell if this tree is a node
    bool isNode() const {return !isLeaf();}

    // Return the number of leaves in this tree
    virtual int nLeaves() const = 0;

    // Return the number of nodes in this tree (excluding leaves)
    virtual int nNodes() const = 0;

    // Return the number of (sub)trees in this tree (nodes and leaves)
    virtual int nTrees() const = 0;

    std::vector<double> operator()(const std::vector<int>&,unsigned int) const;
    std::vector<double>& operator()(const std::vector<int>&,unsigned int);

    // For debugging
    /// Display a tree on standard output
    void display(std::string prefix = "", void(*prt)(std::vector<double>) = 0){
        if(! this) // Null tree
            std::cout << prefix << " ." << std::endl;
        else {
            if (this->isLeaf()) { // If tree is leaf
                std::cout << prefix << " = ";
                if (prt)
                    (*prt)(this->value());
                else
                    std::cout << this->value();
                std::cout << std::endl;
            } else { // If tree is a branch node
                const std::string dirName[2] = {"OUI", "NON"};
                for (int d = 0; d < 2; d++)
                    child(d)->display(prefix+"-"+dirName[d]);
            }
        }
    }

    ///// VectorLeaf methods

    // Return the value of this Tree
    // Throw domain_error if not a Leaf
    virtual std::vector<double> value() const = 0;

    // Return a reference to the value of this Leaf (for assignments)
    // Throw domain_error if not a Leaf
    virtual std::vector<double>& value() = 0;

    ///// VectorNode methods

    // Return the player in the node
    // Throw domain_error if not a Node
    virtual unsigned int player() const = 0;

    // Return the child of this tree in direction d
    // Throw domain_error if not a Node
    virtual const VectorTree* child(int d) const = 0;

    // Return a reference to the child of this tree in direction d
    // Throw domain_error if not a Node
    virtual VectorTree*& child(int d) = 0;
};

class VectorLeaf : public VectorTree {
    std::vector<double> val; // The value contained in this leaf
public:
    bool isLeaf() const {return true;}

    // Construct a Leaf with the given value
    VectorLeaf(std::vector<double> value) : val(value) {}

    // Return the number of leaves in this tree
    int nLeaves() const {return 1;}

    // Return the number of nodes in this tree (excluding leaves)
    int nNodes() const {return 0;}

    // Return the number of (sub)trees in this tree (nodes and leaves)
    int nTrees() const {return 1;}

    ///// VectorLeaf methods

    // Return the value of this Leaf
    std::vector<double> value() const {return val;}

    // Return a reference to the value of this Leaf (for assignments)
    std::vector<double>& value() {return val;}

    ///// VectorNode methods

    // Supposed to return the player in the node
    // But throw domain_error as not a Node
    virtual unsigned int player() const {
        throw new std::domain_error("Not a Node");}

    // Supposed to return the child of this tree in direction d
    // But throw domain_error as not a Node
    VectorTree* child(int) const {
        throw new std::domain_error("Not a Node");}

    // Return a reference to the child of this quadtree in direction d
    // But throw domain_error as not a QuadNode
    VectorTree*& child(int) {
        throw new std::domain_error("Not a Node");}
};

class VectorNode : public VectorTree {
    int j_player;
    VectorTree* children[2];
public:
    ~VectorNode() {delete children[0];delete children[1];}

    // Tell if this tree is a leaf
    bool isLeaf() const {return false;}

    // Construct a new branching node given an array of 2 trees
    VectorNode(VectorTree* qtrees[2],int J): j_player(J) {
        for (int i = 0; i < 2; i++) children[i] = qtrees[i];
    }

    // Construct a new branching node with empty (null) children
    VectorNode(): j_player(0) {
        for (int i = 0; i < 2; i++) children[i] = 0;
    }

    // Construct a new branching node given 2 children
    VectorNode(VectorTree* child0,
             VectorTree* child1,int J): j_player(J) {
        children[0] = child0;children[1] = child1;
    }

    // Return the number of leaves in this tree
    int nLeaves() const {
        int n = 0;
        for(int i=0; i<2; i++)
            if(children[i])
                n += children[i]->nLeaves();
        return n;
    }

    // Return the number of nodes in this tree (excluding leaves)
    int nNodes() const {
        int n = 1;
        for(int i=0; i<2; i++)
            if (children[i])
                n += children[i]->nNodes();
        return n;
    }

    // Return the number of (sub)trees in this tree (nodes and leaves)
    int nTrees() const {
        int n = 1;
        for(int i=0; i<2; i++)
            if(children[i])
                n += children[i]->nTrees();
        return n;
    }

    ///// VectorLeaf methods

    // Supposed to return the value of this Tree
    // But throw a domain_error as it is not a Leaf
    std::vector<double> value() const { throw new std::domain_error("Not a Leaf"); }

    // Supposed to return a reference to the value of this Tree
    // But throw a domain_error as it is not a Leaf
    std::vector<double>& value() { throw new std::domain_error("Not a Leaf"); }

    ///// VectorNode methods

    // Return the player in this node
    virtual unsigned int player() const {return j_player;};

    // Return the child of this tree in direction d
    const VectorTree* child(int d) const {
        if(!(0 <= d && d < 2))
            throw new std::out_of_range("Not a valid direction");
        return children[d];
    }

    // Return a reference to the child of this tree in direction d
    VectorTree*& child(int d) {
        if (!(0 <= d && d < 2))
            throw std::out_of_range("Not a valid direction");
        return children[d];
    }
};
