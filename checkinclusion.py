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
    input = input_string
    input_hash = get_node_hash(input)
    return input_hash

def load_tree():
    input_tree = []
    with open('merkle.tree','r') as f:
        for line in f:
            input_tree.append(line.rstrip().split(','))
    # print(input_tree)
    return input_tree

# check if input hash is in leaf
def find_in_leaf(tree, input_hash):
    leaf = tree[-1]
    # print(leaf)
    try:
        index = leaf.index(input_hash)
    except ValueError: 
        print("not find")
        return -1
    else: 
        print("find in ",index)
        return index

# return false or return an result array
def find_in_tree(tree, input_hash):
    result = [] # new hashes 
    result2 = [] # hashes get from tree
    index_in_leaf = find_in_leaf(tree,input_hash)
    if(index_in_leaf!=-1):
        # input hash is found in leaf
        result.append(input_hash)
        # start check upper level hash
        # start from the level above leaf
        level_index = len(tree)-1
        curr_hash = "" # current hash of two
        # index1 = the index of current hash
        index1 = index_in_leaf
        while(level_index>0):
            curr_level = tree[level_index]
            if(curr_hash!=""):
                # curr_hash have new generated hash stored
                # find it in the current level
                try:
                    index = curr_level.index(input_hash)
                except ValueError:
                    # not exists, finish return function
                    print("not find")
                    return -1
                else: 
                    print("find in ", index)
                    # find the hash exists
                    index1 = index
                    result.append(curr_hash)
            # check upper level
            # find the new hash of two
            hash1 = curr_level[index1]
            hash2 = "" # index2 = the index of another hash to hash with
            # find index2, hash2
            if((index1 % 2)==0):
                index2 = index1+1
                if(index2<len(tree[curr_level])):
                    hash2 = tree[curr_level][index2]
            else:
                index2 = index1-1
                hash2 = tree[curr_level][index2]
            result2.append(hash2)
            # find new hash to check for the upper level
            curr_hash = get_node_hash(hash1+hash2)
            level_index-=1
        return result
    else:
        print("input is not in the tree")
        return False

if(len(sys.argv)>1):
    check = load_input(sys.argv[1])
    merkle_hash_tree = load_tree()
    find_in_tree(merkle_hash_tree, check)
else:
    print("missing input")

