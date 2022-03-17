# old merkle tree hash is a subset of the new merkle tree hash
# the new merkle tree hash is the concatenation of the old merkle tree hash 
# plus all the intermediate node hashes of the newly appended strings
# ./checkconsitency.py [alice,bob,carlol,david] [alice,bob,carlol,david,eve,fred]
# ./checkconsitency.py [alice,bob,carlol,david] [alice,bob,david,eve,fred]
import math
from quopri import encode
import sys
from hashlib import sha256
from tkinter import N

def get_node_hash(data):
    return sha256(data.encode('utf-8')).hexdigest()

def get_largest_power_2(num):
    power = int(math.log(num,2))
    return int(pow(2,power))

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
        self.tree = []
        self.leafNodes = []
        print("creat tree")
    
    def add_leaf(self, data_strings):
        for data in data_strings:
            n = Node(data,get_node_hash(data),None,None,None)
            self.leafNodes.append(n)
        print("add leaf: ",len(self.leafNodes))
        self.printLeaf()
            
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
            print_tree_structure(tree[0][0],0)
        return tree

    def printTree(self):
        for level in self.tree:
            print("=====")
            for node in level:
                print(node.hashv)
    
    def printLeaf(self):
        for node in self.leafNodes:
            print(node.hashv[0:5])

def proof(m, newTree):
    print("proof")
    return subProof(m,newTree ,True, newTree) # subProof(m,D[n],True)

def subProof(m, subTree, b, newTree):
    n = len(subTree)# tree(len) = n for now
    print("subproof: ",b)
    if(m==n):
        if b:
            return "" # SUBPROOF(m, D[m], true) = {}
        else:
            return get_subtree_hash(newTree,0,m) # SUBPROOF(m, D[m], false) = {MTH(D[m])}
    if(m<n):
        k = get_largest_power_2(n)
        if(m<=k):
            # SUBPROOF(m, D[n], b) = SUBPROOF(m, D[0:k], b) : MTH(D[k:n])
            return subProof(m, D[0:K],b)+MTH(D[k:n])
        else:
            # SUBPROOF(m, D[n], b) = SUBPROOF(m - k, D[k:n], false) : MTH(D[0:k])
            return subProof(m-k, D[k:n], False)+MTH(D[0:k])

def get_subtree_hash(tree,start,end):
    subTree = MerkleTree()
    subTree.leafNodes=tree.leafNodes[start:end]
    subTree.tree = subTree.build_tree()
    subTree_hash = subTree.tree[0][0].hashv
    print(subTree_hash[0:5])

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

def check_leaf_subset(old, new): #finished, just in case
    for i in range(0,len(old)):
        if(old[i].hashv != new[i].hashv):
            return False
    return True

def load_input(input_string):
    input = input_string[1:-1]
    #print(input)
    input_list = input.split(',')
    #print(input_list)
    return input_list

# ./checkconsitency.py [0,1,2,3] [0,1,2,3,4]
if(len(sys.argv)>2):
        #print(sys.argv[1])
        old_list = load_input(sys.argv[1])
        new_list = load_input(sys.argv[2])
        old_tree = MerkleTree()
        old_tree.add_leaf(old_list)
        new_tree = MerkleTree()
        new_tree.add_leaf(new_list)
        old_tree.build_tree()
        new_tree.build_tree()
        # is_subset = check_leaf_subset(old_tree.leafNodes,new_tree.leafNodes)
        # print(is_subset)
        get_subtree_hash(new_tree,2,4)