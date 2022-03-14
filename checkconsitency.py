# old merkle tree hash is a subset of the new merkle tree hash
# the new merkle tree hash is the concatenation of the old merkle tree hash 
# plus all the intermediate node hashes of the newly appended strings
# ./checkconsitency.py [alice,bob,carlol,david] [alice,bob,carlol,david,eve,fred]
# ./checkconsitency.py [alice,bob,carlol,david] [alice,bob,david,eve,fred]
import sys

def check_leaf_subset(old, new):
    for i in range(0,len(old)):
        if(old[i] != new[i]):
            return False
    return True

def load_input(input_string):
    input = input_string[1:-1]
    #print(input)
    input_list = input.split(',')
    #print(input_list)
    return input_list

# if(len(sys.argv)>2):
#         #print(sys.argv[1])
#         old_list = load_input(sys.argv[1])
#         new_list = load_input(sys.argv[2])
#         is_subset = check_leaf_subset(old_list,new_list)
#         print(is_subset)