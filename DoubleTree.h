#pragma once
#include <vector>
#include <iostream>


// Node of a tree containing an doubleeger at each node
class DoubleTree {
private:
    // Node information
    double data;
    // Sequence of children (empty if none)
    std::vector<DoubleTree*> children;
public:
    // Create a node with given information
    DoubleTree(double d);
    // Create a binaryTree with depth n where every leftChild has the date of his parent * leftData
    // and every rightChild has the date of his parent * rightData
    // newdata is the data of the first node
    DoubleTree(int n, double dataLeft, double dataRight, double newData);
    // Create a binaryTree with depth n where every leftChild has the date of his parent * leftData[i]
    // and every rightChild has the date of his parent * rightData
    // newdata is the data of the first node
    DoubleTree(int n, std::vector<double> dataLeft, std::vector<double> dataRight, double newData);
    // Destruct a node and all its descendents
    ~DoubleTree();
    // Return information of this node
    double getData() const;
    // Set information of this node
    void setData(double d);
    // Return the number of children of this node
    double nbChildren() const;
    // Return the child at pos, if any (left-most child at position 0)
    DoubleTree* getChild(double pos) const;
    // Replace the exisiting child at pos (left-most child at position 0)
    void setChild(double pos, DoubleTree* newChild);
    // Add newChild as supplementary right-most child of this node
    void addAsLastChild(DoubleTree* newChild);
    // Remove right-most child of this node
    void removeLastChild();
    // To see the tree
    void display(std::string prefix = "", std::string indent = "  ") const;
    // Return the depth of the deepest leaf
    double maxDepth() const;
    // Return the depth of the lowest leaf
    double minDepth() const;
    // Return the vector data of the level;
    std::vector<double> getLevel(int level);
};
