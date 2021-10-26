#pragma once

#include <vector>
#include <iostream>


// Node of a tree containing an std::vector<double> at each node
class VectorTree {
private:
    // Node information
    std::vector<double> data;
    // Sequence of children (empty if none)
    std::vector<VectorTree*> children;
public:
    // Create a node with given information
    VectorTree(std::vector<double> d);
    // Create a Tree with all possible scenario and the vector probability associated as the last leaf
    // n == Card(S) and , numberOfPlayer = Card(Sa)
    VectorTree(int numberOfPlayer, std::vector<double> newData);
    // Create a binaryTree with depth n where every leftChild has the vector data of his parent + leftData[n]
    // and every rightChild has the vector data of his parent + rightData[n]
    // newdata is the data of the first node (= empty vector usually)
    VectorTree(int n, std::vector<double> dataLeft, std::vector<double> dataRight, std::vector<double> newData);
    // Destruct a node and all its descendents
    ~VectorTree();
    // Return information of this node
    std::vector<double> getData() const;
    // Set information of this node
    void setData(std::vector<double> d);
    // Return the number of children of this node
    int nbChildren() const;
    // Return the child at pos, if any (left-most child at position 0)
    VectorTree* getChild(int pos) const;
    // Replace the exisiting child at pos (left-most child at position 0)
    void setChild(int pos, VectorTree* newChild);
    // Add newChild as supplementary right-most child of this node
    void addAsLastChild(VectorTree* newChild);
    // Remove right-most child of this node
    void removeLastChild();
    // To see the tree
    void display(std::string prefix = "", std::string indent = "  ") const;
    // Return the depth of the deepest leaf
    int maxDepth() const;
    // Return the depth of the lowest leaf
    int minDepth() const;
    // Return the vector data of the level;
    std::vector<std::vector<double>> getLevel(int level);
};
