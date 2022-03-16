# generate merkle hash tree
# print the content of the three into a file
# representing a list of hashed data as a binary tree of pairs of hashes 
# converging to a single hash， root
# SHA_256
# output file called merkle.tree containing the printout of the built tree.

import math
import sys
from hashlib import sha256

test_data = ["alice", "bob", "carlol", "david"]

def get_largest_power_2(num):
    power = int(math.log(num,2))
    return int(pow(2,power))

def get_node_hash(data):
    # print("data to hash: ",data)
    return sha256(data.encode('utf-8')).hexdigest()

class Node:
    def __init__(self, data, left_child, right_child, parent, level):
        self.data = data
        self.hashv = None
        self.parent = parent
        self.left = left_child
        self.right = right_child
        self.level = level
    
    def add_left_child(self, left):
        self.left = left
    
    def add_right_child(self, right):
        self.right = right
    
    def add_parent(self, parent):
        self.parent = parent
    
    def update_hash(self):
        if self.data:
            # print("leaf")
            self.hashv = get_node_hash(self.data)
        else:
            print("node")
            left_h=""
            right_h=""
            if self.left:
                left_h = self.left.hashv
            if self.right:
                right_h = self.right.hashv
            self.hashv = get_node_hash(left_h+right_h)
        
class MerkleTree:
    def __init__(self):
        self.root = None
        self.tree = []
        self.leafNodes = []
    
    def add_leaf(self, data_strings):
        for data in data_strings:
            n = Node(data,None,None,None,None)
            n.update_hash()
            self.leafNodes.append(n)

    def get_tree_level(self):
        return get_largest_power_2(len(self.leafNodes))
            
    def build_tree(self):
        tree = []
        tree.append(self.leafNodes) #add leaf node hashes to tree
        # print("===leaf_node_hashes===")
        # print(leaf_node_hashes)
        curr_nodes = self.leafNodes
        while(len(curr_nodes)!=1):
            #print(curr_hashes)
            node_index = 0
            new_upper_nodes = []
            while(node_index<len(curr_nodes)):
                left_child = curr_nodes[node_index]
                node_index+=1
                right_child = None
                #print(hash_index)
                if(node_index<len(curr_nodes)):
                    # left +　right
                    right_child = curr_nodes[node_index]  
                # set up parent, link to child         
                if(right_child == None):
                    # no right child
                    print("no right child")
                    # Empty intermediate node, no hash should be update
                    # only for link to the left child at lower level
                    parent = Node(None,left_child,None,None,None)
                    left_child.parent = parent
                    new_upper_nodes.append(parent)
                else:
                    # right_child is not none
                    # if right child is a Empty intermediate node, need to reach to lower level to get hash
                    while(right_child.hashv==None):
                        right_child = right_child.left
                    # new parent
                    print("left_hash: ",left_child.hashv)
                    print("right_hash: ",right_child.hashv)
                    parent = Node(None,left_child,right_child,None,None)
                    parent.update_hash()
                    print("new_hash: ",parent.hashv)
                    # add parent to child
                    left_child.parent = parent
                    right_child.parent = parent                
                    new_upper_nodes.append(parent)    
                node_index+=1
            # print(len(new_hashes))
            # print("===new_hashes===")
            # print(new_hashes)        
            tree.insert(0,new_upper_nodes)
            curr_nodes=new_upper_nodes
        return tree

    def printTree(self):
        for level in self.tree:
            print("=====")
            for node in level:
                print(node.hashv)

# def insert_node(tree, data_string):
#     if(len(tree)==0):
#         leaf_level = [get_node_hash(data_string)]
#         tree.append(leaf_level)

# ./buildmtree.py [alice,bob,carlol,david]
# no space
def load_input(input_string):
    input = input_string[1:-1]
    input_list = input.split(',')
    #print(input_list)
    # print("load input")
    return input_list

# def export_tree(tree):
#     with open('merkle.tree','w') as f:
#         for level in tree:
#             # print(level)
#             line = ','.join(level)
#             f.write(line+'\n')

def main():
    input_list = test_data
    if(len(sys.argv)>1):
        #print(sys.argv[1])
        input_list = load_input(sys.argv[1])
    merkle_hash_tree = MerkleTree()
    merkle_hash_tree.add_leaf(input_list)
    merkle_hash_tree.build_tree()
    merkle_hash_tree.printTree()
    # print("===merkle_hash_tree===")
    # print(merkle_hash_tree)
    # export_tree(merkle_hash_tree)
    # print("export!!")

main()