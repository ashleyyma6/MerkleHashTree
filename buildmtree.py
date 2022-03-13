# generate merkle hash tree
# print the content of the three into a file
# representing a list of hashed data as a binary tree of pairs of hashes 
# converging to a single hash， root
# SHA_256
# output file called merkle.tree containing the printout of the built tree.

import sys
from hashlib import sha256

test_data = ["alice", "bob", "carlol", "david"]

def get_node_hash(data):
    print("data to hash: ",data)
    return sha256(data.encode('utf-8')).hexdigest()

def build_tree(data_strings):
    tree = []
    data_index = 0
    leaf_node_hashes = []
    while(data_index<len(data_strings)):
        leaf_node_hashes.append(get_node_hash(data_strings[data_index]))
        data_index+=1
    tree.append(leaf_node_hashes) #add leaf node hashes to tree
    # print("===leaf_node_hashes===")
    # print(leaf_node_hashes)
    
    curr_hashes = leaf_node_hashes
    while(len(curr_hashes)!=1):
        #print(curr_hashes)
        hash_index = 0
        new_hashes = []
        while(hash_index<len(curr_hashes)):
            left_hash = curr_hashes[hash_index]
            hash_index+=1
            right_hash = ""
            #print(hash_index)
            if(hash_index<len(curr_hashes)):
                # left +　right
                right_hash = curr_hashes[hash_index]
            print("left_hash: ",left_hash)
            print("right_hash: ",right_hash)
            new_hash = get_node_hash(left_hash+right_hash)
            print("new_hash: ",new_hash)
            new_hashes.append(new_hash)
            hash_index+=1
        # print(len(new_hashes))
        # print("===new_hashes===")
        # print(new_hashes)        
        tree.insert(0,new_hashes)
        curr_hashes=new_hashes
    return tree

# ./buildmtree.py [alice,bob,carlol,david]
# no space
def load_input(input_string):
    input = input_string[1:-1]
    #print(input)
    input_list = input.split(',')
    #print(input_list)
    return input_list

def export_tree(tree):
    with open('merkle.tree','w') as f:
        for level in tree:
            # print(level)
            line = ','.join(level)
            f.write(line+'\n')

def main():
    input_list = test_data
    if(len(sys.argv)>1):
        #print(sys.argv[1])
        input_list = load_input(sys.argv[1])
    merkle_hash_tree = build_tree(input_list)
    # print("===merkle_hash_tree===")
    # print(merkle_hash_tree)
    export_tree(merkle_hash_tree)
    print("export!!")

main()