from pytokr import pytokr
s=pytokr()

'''
This time, the tree is encoded differently; first we have our current node, immediately after we have the size OF OUR LEFT SUBTREE and THEN we have the our left child. A 0 can mean one of 2 things; there is no left subtree or, its a 0 in the node. Empty trees are omitted .
'''

def reading_input(size):        #define the tree according to the size we get
    if size == 0:   #if the size is 0, then our left subtree is empty;
        return tuple()  #return an empty tuple
    l=int(s())  #take from the input the node we are on as integer
    sizeleft=int(s())   #take its size as int 
        # recursively build the tree by giving the sizeleft to the left child and to the right the total size -1 because of the node we are on and -sizeleft because we are on the right tree
    return (l, reading_input(sizeleft), reading_input(size-1-sizeleft))
    
    
def post_order(inp):    #our first order of business
    if not inp:     #if there is no more inout or it is empty
        return []   # return an empty list
    else:   #if thre is  input
        left=post_order(inp[1]) #assign the left node as the first one right after our current node since we are working with binary trees 
        right=post_order(inp[2])    #assign the right tree as the secode node after the one we are currently on 
        return left+ right + [inp[0]]       # return the order of first the left child, then the right and then the root so the node we currently on
    
    
def inorder(inp):       #for inorder, second order of business
    if not inp: #if the input is empty  
        return []   #return an empty list
    else:   #otherwise
        left= inorder(inp[1])   #assign as always the left child as the first one right after our current node
        right= inorder(inp[2])  #assign the right one as the one after the left one 
        return left+ [inp[0]] + right   #return the left child first, then the root and then the right child
        

size = int(s())     #the first number is the size of our tree
inp=reading_input(size)              #define the tree
print('post:', *post_order(inp), '')    #run the post_order and print res
print('in:', *inorder(inp), '')     #run the inorder and print res
