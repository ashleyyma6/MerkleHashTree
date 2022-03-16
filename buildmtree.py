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
    def __init__(self, data, hash, left_child, right_child, parent):
        self.data = data
        self.hashv = hash
        self.parent = parent
        self.left = left_child
        self.right = right_child
        
    def update_hash(self, right=None):
        left_h=""
        right_h=""
        if self.left.hashv:
            left_h = self.left.hashv
        if self.right.hashv:
            right_h = self.right.hashv
        else:
            right_h = right
        self.hashv = get_node_hash(left_h+right_h)
        
class MerkleTree:
    def __init__(self):
        self.root = None
        self.tree = []
        self.leafNodes = []
        print("creat tree")
    
    def add_leaf(self, data_strings):
        for data in data_strings:
            n = Node(data,get_node_hash(data),None,None,None)
            self.leafNodes.append(n)
        print("add leaf: ",len(self.leafNodes))
        self.printLeaf()

    def get_tree_level(self):
        return get_largest_power_2(len(self.leafNodes))
            
    def build_tree(self):
        tree = []
        tree.append(self.leafNodes) #add leaf node hashes to tree
        curr_nodes = self.leafNodes
        print("curr_nodes loaded")
        while(len(curr_nodes)!=1):
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
                    # no right sibling child
                    print("no right child")
                    # Empty intermediate node, no hash should be update
                    # only for link to the left child at lower level
                    parent = Node(None,None,left_child,None,None)
                    left_child.parent = parent
                    new_upper_nodes.append(parent)
                else:
                    # right sibling child is not none
                    # if right child is a Empty intermediate node, need to reach to lower level to get hash
                    # new parent
                    parent = Node(None,None,left_child,right_child,None)
                    # add parent to child
                    left_child.parent = parent
                    right_child.parent = parent 
                    # keep empty intermediate node in the tree
                    # while -> find the real right child hash
                    while(right_child.hashv==None):
                        print("right sibling child is none")
                        right_child = right_child.left
                    print("left_hash: ",left_child.hashv[0:5])
                    print("right_hash: ",right_child.hashv[0:5])
                    parent.update_hash(right_child.hashv)
                    print("parent hash: ",parent.hashv[0:5])          
                    new_upper_nodes.append(parent)    
                node_index+=1
            print("add upper level nodes: ",len(new_upper_nodes))      
            tree.insert(0,new_upper_nodes)
            curr_nodes=new_upper_nodes
        return tree

    def printTree(self):
        for level in self.tree:
            print("=====")
            for node in level:
                print(node.hashv)
    
    def printLeaf(self):
        for node in self.leafNodes:
            print(node.hashv[0:5])

# ./buildmtree.py [alice,bob,carlol,david]
# ./buildmtree.py [0,1,2,3,4,5,6,7]
def load_input(input_string):
    input = input_string[1:-1]
    input_list = input.split(',')
    print("load input: ",input_list)
    return input_list

def export_tree(tree):
    with open('merkle.tree','w') as f:
        f.write("===Compeleted Tree Hash in every tree level===\n")
        for i in range(0,len(tree)):
            hashes = []
            for j in range(0,len(tree[i])):
                s = ""
                if(tree[i][j].hashv): 
                    s+=str(tree[i][j].hashv)
                else:
                    s+='-1'
                # s+=':'
                # if(tree[i][j].data):
                #     s+=str(tree[i][j].data)
                # else:
                #     s+='None'
                hashes.append(s)
            line = ','.join(hashes)
            f.write(line+'\n')
        # friendly view
        f.write("=== Tree structure with trimed hash ===\n")
        f.write(export_tree_structure(tree[0][0],0))
        #print_tree_structure(tree[0][0],0)

def export_tree_structure(root, level):
    line = ""
    spaces = '|     ' * level
    if(root.hashv):
        line +=(spaces+'-'+root.hashv[0:5]+"\n")
    else: 
        line +=(spaces+'-'+"none"+"\n")
    if not root.data:
        if(root.left):
            str=export_tree_structure(root.left, level+1)
            if str:
                line+=str
        if(root.right):
            str=export_tree_structure(root.right, level+1)
            if str:
                    line+=str
    return line

def print_tree_structure(root, level):
    spaces = '|    '*level
    if(root):
        if(root.hashv):
            print(spaces+'-'+root.hashv[0:5])
        else: 
            print(spaces+'-'+"none")
    if not root.data:
        if(root.left):
            print_tree_structure(root.left, level+1)
        if(root.right):
            print_tree_structure(root.right, level+1)
        
def main():
    input_list = test_data
    if(len(sys.argv)>1):
        input_list = load_input(sys.argv[1])
    merkle_hash_tree = MerkleTree()
    merkle_hash_tree.add_leaf(input_list)
    merkle_hash_tree.tree= merkle_hash_tree.build_tree()
    merkle_hash_tree.printTree()
    # print("===merkle_hash_tree===")
    # print(merkle_hash_tree)
    export_tree(merkle_hash_tree.tree)
    # print("export!!")

main()