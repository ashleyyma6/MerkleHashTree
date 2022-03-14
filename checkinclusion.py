# ./checkinclusion.py richard
#  yes [12345, 67890, 10111]

# To verify d3
# send hash h34, h1
# compute d3 d4 hash h2
# compare h1234 with root

# 1. hash input
# 2. find hash in the leaf
# 3. find which sub tree input at, get hashes
# 4. get hashes, compute new root, compare with old root

from logging import exception
import sys
from hashlib import sha256

def get_node_hash(data):
    return sha256(data.encode('utf-8')).hexdigest()

def load_input(input_string):
    return get_node_hash(input_string)

def load_tree():
    input_tree = []
    with open('merkle.tree','r') as f:
        for line in f:
            input_tree.append(line.rstrip().split(','))
    # print("load tree", input_tree)
    return input_tree

# check if input hash is in leaf
def find_in_leaf(tree, input_hash):
    leaf = tree[-1]
    # print("leaf nodes: ", leaf)
    try:
        index = leaf.index(input_hash)
    except ValueError: 
        print("not find in leaf")
        return -1
    else: 
        print("find in leaf at: ",index)
        return index

# return false or return an result array
def find_in_tree(tree, input_hash):
    result = [] # hashes to hash with
    
    index_in_leaf = find_in_leaf(tree,input_hash)
    if(index_in_leaf != -1):
        # input hash is found in leaf
        result.append(input_hash)
        # check upper level hash
        curr_level_index = len(tree)-2 # start from the level above leaf
        curr_hash = "" # current hash of two
        index1 = index_in_leaf # index1 = the index of current hash
        while(curr_level_index>-1):
            curr_level_nodes = tree[curr_level_index]
            print("curr_level_index: ",curr_level_index)
            print("curr_level_nodes: ",curr_level_nodes)
     
            # find the new hash of two in lower level
            lower_level_index = curr_level_index+1
            hash1 = tree[lower_level_index][index1]
            hash2 = "" # index2 = the index of another hash to hash with
            two_hash_to_hash = ""
            # find index2, hash2
            if((index1 % 2)==0):
                print("index 1 even")
                index2 = index1+1
                if(index2<len(tree[lower_level_index])):
                    hash2 = tree[lower_level_index][index2]
                two_hash_to_hash = hash1+hash2
            else:
                print("index 1 odd")
                hash2 = tree[lower_level_index][index1-1]
                two_hash_to_hash = hash2+hash1
            print("hash1: ",hash1)
            print("hash2: ",hash2)
            result.append(hash2)
            # find new hash to check for the upper level
            curr_hash = get_node_hash(two_hash_to_hash)
            print("get new hash: ",curr_hash)
            
            # check current level
            # curr_hash have new generated hash stored
            # find it in the current level
            try:
                index1 = curr_level_nodes.index(curr_hash)
            except ValueError:
                # not exists, finish return function
                print("not find in current level: ",curr_level_index)
                return -1
            else: 
                print("find at ", index1)
                curr_level_index-=1
                # find the hash exists
            
        return result
    else:
        print("input is not in the tree")
        return -1

if(len(sys.argv)>1):
    check = load_input(sys.argv[1])
    merkle_hash_tree = load_tree()
    result = find_in_tree(merkle_hash_tree, check)
    if(result != -1):
        print("Yes", result)
    else:
        print("No")
else:
    print("missing input")

