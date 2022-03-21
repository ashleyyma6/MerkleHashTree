# old merkle tree hash is a subset of the new merkle tree hash
# the new merkle tree hash is the concatenation of the old merkle tree hash 
# plus all the intermediate node hashes of the newly appended strings
# ./checkconsitency.py [alice,bob,carlol,david] [alice,bob,carlol,david,eve,fred]
# ./checkconsitency.py [alice,bob,carlol,david] [alice,bob,david,eve,fred]
# ./checkconsitency.py [alice,bob,carlol,david] [alice,bob,carol,eve,fred,davis]
# cat merkle.trees

import math
import sys
from hashlib import sha256

def get_node_hash(data):
    return sha256(data.encode('utf-8')).hexdigest()

def get_largest_power_2(num):
    power = int(math.log(num,2))
    if(pow(2,power) == num):
        power -= 1
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
        #print("creat tree")
    
    def add_leaf(self, data_strings):
        for data in data_strings:
            n = Node(data,get_node_hash(data),None,None,None)
            self.leafNodes.append(n)
        #print("add leaf: ",len(self.leafNodes))
        #self.printLeaf()
            
    def build_tree(self):
        tree = []
        tree.append(self.leafNodes) #add leaf node hashes to tree
        curr_nodes = self.leafNodes
        #print("curr_nodes loaded")
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
                    #print("no right child")
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
                        #print("right sibling child is none")
                        right_child = right_child.left
                    #print("left_hash: ",left_child.hashv[0:5])
                    #print("right_hash: ",right_child.hashv[0:5])
                    parent.update_hash(right_child.hashv)
                    #print("parent hash: ",parent.hashv[0:5])          
                    new_upper_nodes.append(parent)    
                node_index+=1
            #print("add upper level nodes: ",len(new_upper_nodes))      
            tree.insert(0,new_upper_nodes)
            curr_nodes=new_upper_nodes
            #print_tree_structure(tree[0][0],0)
        return tree

    def printTree(self):
        for level in self.tree:
            print("=====")
            for node in level:
                print(node.hashv)
    
    def printLeaf(self):
        for node in self.leafNodes:
            print(node.hashv[0:5])

def proof(m, tree_leaves):
    # result array holds hashes
    result = []
    #print("proof")
    # PROOF(m, D[n]) = SUBPROOF(m, D[n], true)
    subProof(m,tree_leaves,True,result)
    return result

def subProof(m, inputs, b, result):
    n = len(inputs) # tree(len) = n for now
    #print("subproof, n =",n)
    if(m==n):
        #print("m=n")
        if b:
            return # SUBPROOF(m, D[m], true) = {}
        else:
            return get_subtree_hash(inputs,0,m)# SUBPROOF(m, D[m], false) = {MTH(D[m])}
    if(m<n):
        k = get_largest_power_2(n)
        #print("m<n, k =",k)
        if(m<=k):
            # SUBPROOF(m, D[n], b) = SUBPROOF(m, D[0:k], b) : MTH(D[k:n])
            r = subProof(m, inputs[0:k], b, result)
            if r:
                result.append(r)
            result.append(get_subtree_hash(inputs,k,n))
        else:
            # SUBPROOF(m, D[n], b) = SUBPROOF(m - k, D[k:n], false) : MTH(D[0:k])
            r = subProof(m-k, inputs[k:n], False, result)
            if r:
                result.append(r)
            result.append(get_subtree_hash(inputs,0,k))

def get_subtree_hash(tree_leaves,start,end):
    if((end-start)==1):
        #print("get_subtree_hash: ",tree_leaves[start].hashv[0:5])
        return tree_leaves[start].hashv
    else:
        subTree = MerkleTree()
        subTree.leafNodes=tree_leaves[start:end]
        subTree.tree = subTree.build_tree()
        subTree_hash = subTree.tree[0][0].hashv
        #print("get_subtree_hash: ",subTree_hash[0:5])
    return subTree_hash

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

def check_leaf_subset(old, new):
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

def find_in_tree(tree,hash):
    print("start find: ", hash)
    for i in range(0,len(tree.tree)):
        for j in range(0,len(tree.tree[i])):
            if tree.tree[i][j].hashv == hash:
                return [i,j]
    return [-1]

def verification(old_tree, new_tree, proof_result):
    tree_hash = ""
    result = proof_result
    k = get_largest_power_2(len(new_tree.leafNodes))
    if(len(old_tree.leafNodes) == k):
        #print("pass k")
        tree_hash = get_node_hash(old_tree.tree[0][0].hashv+proof_result[0])
        if tree_hash == new_tree.tree[0][0].hashv:
            #print("verified - k")
            result.insert(0,old_tree.tree[0][0].hashv)
            result.append(new_tree.tree[0][0].hashv)
    else:
        #print("notpass k")
        tree_hash = proof_result[0]
        for i in range(1,len(proof_result)):
            find1 = find_in_tree(new_tree, proof_result[i])#[node index]
            find2 = find_in_tree(new_tree, tree_hash)#[node index]
            if(find1[0]!=-1):
                #print("find at", find2)
                if(find2[0] == find1[0]):
                    if (find1[1]%2)==0:
                        #print("find is even")
                        tree_hash = get_node_hash(proof_result[i]+tree_hash)
                    else:
                        tree_hash = get_node_hash(tree_hash+proof_result[i])
                        #print("find is odd")
                else: 
                    tree_hash = get_node_hash(tree_hash+proof_result[i])
                    #print("find is seperated in multiple level")
            #print("loop i: ",i," tree hash: ",tree_hash)
        #print("final tree hash: ",tree_hash)
        if tree_hash == new_tree.tree[0][0].hashv:
            #print("verified - find")
            result.append(new_tree.tree[0][0].hashv)
        else: 
            print("error in verification")
            return False
    return result

def export_tree(tree1,tree2):
    with open('merkle.tree','w') as f:
        # f.write("=== Compeleted Tree Hash in every tree level for old version tree ===\n")
        # for i in range(0,len(tree1)):
        #     hashes = []
        #     for j in range(0,len(tree1[i])):
        #         s = ""
        #         if(tree1[i][j].hashv): 
        #             s+=str(tree1[i][j].hashv)
        #         else:
        #             s+='-1'
        #         hashes.append(s)
        #     line = ','.join(hashes)
        #     f.write(line+'\n')
        # friendly view
        f.write("=== Tree structure with trimed hash for old version tree ===\n")
        f.write(export_tree_structure(tree1[0][0],0))
        # f.write("=== Compeleted Tree Hash in every tree level for new version tree ===\n")
        # for i in range(0,len(tree2)):
        #     hashes = []
        #     for j in range(0,len(tree2[i])):
        #         s = ""
        #         if(tree2[i][j].hashv): 
        #             s+=str(tree2[i][j].hashv)
        #         else:
        #             s+='-1'
        #         hashes.append(s)
        #     line = ','.join(hashes)
        #     f.write(line+'\n')
        # friendly view
        f.write("=== Tree structure with trimed hash for new version tree ===\n")
        f.write(export_tree_structure(tree2[0][0],0))
        #print_tree_structure(tree[0][0],0)
        #print("exported!")

def export_tree_structure(root, level):
    line = ""
    spaces = '|     ' * level
    if(root.hashv):
        d=''
        if(root.data):
            d = root.data
            line +=(spaces+'-'+root.hashv+"\n")
        else:
            line +=(spaces+'-'+root.hashv+"\n")
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

def main():
    if(len(sys.argv)>2):
        #print(sys.argv[1])
        old_list = load_input(sys.argv[1])
        new_list = load_input(sys.argv[2])
        old_tree = MerkleTree()
        old_tree.add_leaf(old_list)
        new_tree = MerkleTree()
        new_tree.add_leaf(new_list)
        old_tree.tree = old_tree.build_tree()
        new_tree.tree = new_tree.build_tree()
        #print_tree_structure(new_tree.tree[0][0],0)
        is_subset = check_leaf_subset(old_tree.leafNodes,new_tree.leafNodes)
        if(is_subset):
            #print("Yes")
            proof_result = proof(len(old_list),new_tree.leafNodes)
            #print("proof_result: ",proof_result)
            verify = verification(old_tree, new_tree,proof_result)
            if(verify!=False):
                print("Yes",verify)
            else: 
                print("No")
        else:
            print("No")
        export_tree(old_tree.tree,new_tree.tree)
        # get_subtree_hash(new_tree,2,4)
    else:
        print("missing input")

# ./checkconsitency.py [0,1,2,3] [0,1,2,3,4]
main()