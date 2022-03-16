# ./checkinclusion.py richard
#  yes [12345, 67890, 10111]

# assume buildmtree.py saved a tree in merkle.tree
# To verify d3
# send hash h34, h1
# compute d3 d4 hash h2
# compare h1234 with root

# 1. hash input
# 2. find hash in the leaf
# 3. find which sub tree input at, get hashes
# 4. get hashes, compute new root, compare with old root

from logging import exception
from operator import truediv
from re import I
import sys
from hashlib import sha256

def get_node_hash(data):
    return sha256(data.encode('utf-8')).hexdigest()

class Node:
    def __init__(self, hash, left_child, right_child, parent):
        self.hashv = hash
        self.parent = parent
        self.left = left_child
        self.right = right_child

class MerkleTree:
    def __init__(self):
        self.tree = []
        self.leafNodes = []
        print("creat tree")
    
    def load_hashes(self): #finished
        input_hashes = []
        with open('merkle.tree','r') as f:
            line=f.readline()
            if(line.find("Comp")>0):
                line=f.readline()
                while(len(line)>0):
                    if(line.find("structure")>0):
                        print("finish load")
                        break
                    #print(line[:-1])
                    input_hashes.append(line[:-1].rstrip().split(','))
                    line=f.readline()
            else:
                print("error in file")
            #print(input_hashes)
        return input_hashes

    def add_leaf(self, input_hashes): # finished
        for hash in input_hashes[-1]:
            n = Node(hash,None,None,None)
            self.leafNodes.append(n)
        print("leaf added")

    def rebuild_tree(self,input_hashes): # finished
        tree = []
        tree.append(self.leafNodes) #add leaf node to tree
        curr_nodes = self.leafNodes
        curr_level = len(input_hashes)-1
        print("curr_nodes loaded")
        while(len(curr_nodes)!=1):
            parent_level=curr_level-1
            node_index = 0
            upper_nodes = []
            while(node_index<len(curr_nodes)):
                parent_index = int(node_index/2)
                parent_hash = input_hashes[parent_level][parent_index]
                # set up parent, link to child         
                if(parent_hash == "-1"):
                    # no right sibling child
                    print("parent have no right child")
                    # Empty intermediate node, no hash should be update
                    # only for link to the left child at lower level
                    left_child = curr_nodes[node_index]
                    parent = Node(None,left_child,None,None)
                    left_child.parent = parent
                    upper_nodes.append(parent)
                else:
                    # right sibling child is not none
                    # if right child is a Empty intermediate node, need to reach to lower level to get hash
                    # new parent
                    left_child = curr_nodes[node_index]
                    right_child = curr_nodes[node_index+1]
                    parent = Node(parent_hash,left_child,right_child,None)
                    # add parent to child
                    left_child.parent = parent
                    right_child.parent = parent         
                    upper_nodes.append(parent)    
                node_index+=2
            print("rebuild upper level nodes: ",len(upper_nodes))      
            tree.insert(0,upper_nodes)
            curr_nodes=upper_nodes
            curr_level=parent_level
        #print_tree_structure(tree[0][0],0)
        return tree

    # check if input hash is in leaf
    def find_in_leaf(self, input):
        leaves = self.tree[-1]
        for i in range(0,len(leaves)):
            if (leaves[i].hashv == input):
                print("find in leaf at: ",i)
                return i
        print("not find in leaf")
        return -1
    
    # return false or return an result array
    def find_in_tree(self, tree, input_hash):
        result = [] # hashes to hash with
        index_in_leaf = self.find_in_leaf(input_hash)
        if(index_in_leaf != -1):
            # input hash is found in leaf
            result.append(input_hash)
            # check upper level hash
            curr_hash = "" # current hash of two
            node1 = tree[(len(tree)-1)][index_in_leaf] # leaf node
            while(node1.parent!=None):
                # find the new hash of two in lower level
                parent_node = node1.parent
                node2 = None 
                two_hashes = ""
                if(parent_node.left == node1):
                    print("node 1 left child")
                    node2 = parent_node.right
                    if(node2 == None):
                        print("no right sibiling")
                        node1 = parent_node
                        # no anther node to hash with, go to upper level find another node
                        # then from intermediate note, get to a node to hash
                        continue
                    while(node2.hashv == None):
                        # empty intermediate node, go to bottom
                        node2 = node2.left
                    two_hashes = node1.hashv+node2.hashv
                else:
                    print("node 1 right child, must have left sibling")
                    node2 = parent_node.left
                    while(node1.hashv == None):
                        node1 = node1.left
                    two_hashes = node2.hashv+node1.hashv
                print("hash1: ",node1.hashv)
                print("hash2: ",node2.hashv)
                result.append(node2.hashv)
                # find new hash to check for the upper level
                # curr_hash have new generated hash stored
                curr_hash = get_node_hash(two_hashes)
                print("get new hash: ",curr_hash)
                if(parent_node.hashv == curr_hash):
                    print("find parent hash match")
                    node1 = parent_node
                else:
                    print("not match")
                    return -1
            return result
        else:
            print("input is not in the tree")
            return -1

    def printTree(self):
        for level in self.tree:
            print("=====")
            for node in level:
                print(node.hashv)
    
    def printLeaf(self):
        for node in self.leafNodes:
            print(node.hashv[0:5])

def load_input(input_string):
    return get_node_hash(input_string)

# for test
def print_tree_structure(root, level):
    spaces = '|    '*level
    if(root):
        if(root.hashv):
            print(spaces+'-'+root.hashv[0:5])
        else: 
            print(spaces+'-'+"none")
        if(root.left):
            print_tree_structure(root.left, level+1)
        if(root.right):
            print_tree_structure(root.right, level+1)

if(len(sys.argv)>1):
    hash = load_input(sys.argv[1])
    merkle_hash_tree = MerkleTree()
    input_hashes = merkle_hash_tree.load_hashes()
    merkle_hash_tree.add_leaf(input_hashes)
    # merkle_hash_tree.printLeaf()
    merkle_hash_tree.tree = merkle_hash_tree.rebuild_tree(input_hashes)
    # merkle_hash_tree.printTree()
    result = merkle_hash_tree.find_in_tree(merkle_hash_tree.tree, hash)
    if(result != -1):
        print("Yes", result)
        result_trimmed = []
        for h in result:
            result_trimmed.append(h[0:5])
        print("trimmed version: ",result_trimmed)
    else:
        print("No")
else:
    print("missing input")

