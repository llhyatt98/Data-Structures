
# BinarySearchTree is a class for a binary search tree (BST)
# when called, a BST is initialized with no root and size 0.
# size keeps track of the number of nodes in the tree
from Node import RB_Node

class RedBlackTree:
    # initialize root and size
    def __init__(self):
        self.root = None
        self.size = 0
        
        # All leaf nodes point to self.sentinel, rather than 'None'
        # Parent of root should also be self.sentinel
        self.sentinel = RB_Node(None, color = 'black')
        self.sentinel.parent = self.sentinel
        self.sentinel.leftChild = self.sentinel
        self.sentinel.rightChild = self.sentinel

    '''
    Free Methods
    '''

    def sentinel(self):     
        return self.sentinel

    def root(self):
        return self.root

    def __iter__(self):
        # in-order iterator for your tree
        return self.root.__iter__()

    def getKey(self, key):
        # expects a key
        # returns the key if the node is found, or else raises a KeyError

        if self.root:
            # use helper function _get to find the node with the key
            res = self._get(key, self.root)
            if res: # if res is found return the key
                return res.key
            else:
                raise KeyError('Error, key not found')
        else:
            raise KeyError('Error, tree has no root')

    
    def getNode(self, key):
        # expects a key
        # returns the RB_Node object for the given key
        
        if self.root:
            res = self._get(key, self.root)
            if res:
                return res
            else:
                raise KeyError('Error, key not found')
        else:
            raise KeyError('Error, tree has no root')

    # helper function _get receives a key and a node. Returns the node with
    # the given key
    def _get(self, key, currentNode):
        if currentNode is self.sentinel: # if currentNode does not exist return None
            print("couldnt find key: {}".format(key))
            return None
        elif currentNode.key == key:
            return currentNode
        elif key < currentNode.key:
            # recursively call _get with key and currentNode's leftChild
            return self._get( key, currentNode.leftChild )
        else: # key is greater than currentNode.key
            # recursively call _get with key and currentNode's rightChild
            return self._get( key, currentNode.rightChild )

    
    def __contains__(self, key):
        # overloads the 'in' operator, allowing commands like
        # if 22 in rb_tree:
        # ... print('22 found')

        if self._get(key, self.root):
            return True
        else:
            return False
    
    #Call this method within delete, 
    def __transplant(self, nodeA, nodeB):
        '''
        Replaces the node rooted at A with the node rooted at B. 
        '''
        if (nodeA.parent == None):
            self.root = nodeB
        elif (nodeA == nodeA.parent.leftChild):
            nodeA.parent.leftChild = nodeB
        else:
            nodeA.parent.rightChild = nodeB

        if nodeB != None:
            if nodeB.parent == None:
                nodeB.parent = nodeA.parent


    def delete(self, key):
        # Same as binary tree delete, except we call rb_delete fixup at the end.
       	# Code goes through and checks all the testcases of RB Trees and does corresponding
       		# operation to maintain properties. 

        z = self.getNode(key)
        if z.leftChild is self.sentinel or z.rightChild is self.sentinel:
            y = z
        else:
            y = z.findSuccessor()
        
        if y.leftChild is not self.sentinel:
            x = y.leftChild
        else:
            x = y.rightChild
        
        if x is not self.sentinel:
            x.parent = y.parent

        if y.parent is self.sentinel:
            self.root = x

        else:
            if y == y.parent.leftChild:
                y.parent.leftChild = x
            else:
                y.parent.rightChild = x
        
        if y is not z:
            z.key = y.key
    
        if y.color == 'black':
            if x is self.sentinel: #Fixup the other node, else fixup x 
                self._rb_Delete_Fixup(y)
            else:
                self._rb_Delete_Fixup(x)
        

    def traverse(self, order = "in-order"):
        # Same a BST traverse 
        self.walk(order, self.root)


    '''
    Required Methods Begin Here
    '''

    def insert(self, key):
        # add a key to the tree. Don't forget to fix up the tree and balance the nodes.
        #Drawn from the pseudocode in the CLRS

        z = RB_Node(key)

        y = self.sentinel
        x = self.root

        if x == None: 
        	z.parent = self.sentinel
        	z.leftChild = self.sentinel 
        	z.rightChild = self.sentinel 
        	z.color = 'black'
        	self.root = z

        else: 
	        while x != self.sentinel:
	        	y = x 
	        	if z.key < x.key:
	        		x = x.leftChild
	        	else:
	        		x = x.rightChild

	        z.parent = y

	        if y == self.sentinel:
	        	self.root = z 
	        elif z.key < y.key:
	        	y.leftChild = z 
	        else: 
	        	y.rightChild = z
	        z.leftChild = self.sentinel
	        z.rightChild = self.sentinel
	        z.color = "red"

	        self._rbInsertFixup(z) #Last step is to fixup the new node, calling our insert fixup. 


    def _rbInsertFixup(self, z):
        # write a function to balance your tree after inserting
        #Drawn from the pseudocode in the CLRS
        	#This function is meant to be called after we insert a node into the tree. 
        while z.parent.color == 'red':
        	if z.parent == z.parent.parent.leftChild:
        		y = z.parent.parent.rightChild
        		if y.color == "red":
        			z.parent.color = "black"
        			y.color = "black"
        			z.parent.parent.color = "red"
        			z = z.parent.parent
        		else: 
        			if z == z.parent.rightChild:
        				z = z.parent
        				self.leftRotate(z)
        			z.parent.color = "black"
        			z.parent.parent.color = "red"
        			self.rightRotate(z.parent.parent)
        	else: 
        		y = z.parent.parent.leftChild
        		if y.color == "red":
        			z.parent.color = "black"
        			y.color = "black"
        			z.parent.parent.color = "red"
        			z = z.parent.parent
        		else: 
        			if z == z.parent.leftChild:
        				z = z.parent
        				self.rightRotate(z)
        			z.parent.color = "black"
        			z.parent.parent.color = "red"
        			self.leftRotate(z.parent.parent)

        self.root.color = "black" #Maintain this property after every insertion. 


    def _rb_Delete_Fixup(self, x):
        # receives a node, x, and fixes up the tree, balancing from x.
        #Drawn from the pseudocode in the CLRS
        	#Called directly after we delete. 

        while x != self.root and x.color == 'black':
        	if x == x.parent.leftChild:
        		w = x.parent.rightChild
        		if w.key == None:
        			break
        		if w.color == "red":
        			w.color = "black"
        			x.parent.color = "red"
        			self.leftRotate(x.parent)
        			w = x.parent.rightChild
        		if w.leftChild.color == "black" and w.rightChild.color == "black":
        			w.color = "red"
        			x = x.parent
        		else: 
        			if w.rightChild.color == "black":
        				w.leftChild.color = "black"
        				w.color = "red"
        				self.rightRotate(w)
        				w = x.parent.rightChild
        			w.color = x.parent.color
        			x.parent.color = "black"
        			w.rightChild.color = "black"
        			self.leftRotate(x.parent)
        			x = self.root
        	else: 
        		w = x.parent.leftChild
        		if w.key == None:
        			break
        		if w.color == "red":
        			w.color = "black"
        			x.parent.color = "red"
        			self.rightRotate(x.parent)
        			w = x.parent.leftChild
        		if w.rightChild.color == "black" and w.leftChild.color == "black":
        			w.color = "red"
        			x = x.parent
        		else: 
        			if w.leftChild.color == "black":
        				w.rightChild.color = "black"
        				w.color = "red"
        				self.leftRotate(w)
        				w = x.parent.leftChild
        			w.color = x.parent.color
        			x.parent.color = "black"
        			w.leftChild.color = "black"
        			self.rightRotate(x.parent)
        			x = self.root

        x.color = "black"


    def leftRotate(self, currentNode):
        # perform a left rotation from a given node
        # Current node will be of type RB_Node 
        #Drawn from the pseudocode in the CLRS

        y = currentNode.rightChild
        currentNode.rightChild = y.leftChild

        if y.leftChild != self.sentinel:
        	y.leftChild.parent = currentNode

        y.parent = currentNode.parent

        if currentNode.parent == self.sentinel:
        	self.root = y
        elif currentNode == currentNode.parent.leftChild:
        	currentNode.parent.leftChild = y
        else: 
        	currentNode.parent.rightChild = y

        y.leftChild = currentNode
        currentNode.parent = y



    def rightRotate(self, currentNode):
        # perform a right rotation from a given node
        # Current node will be of type RB_Node
        #Drawn from the pseudocode in the CLRS

        y = currentNode.leftChild
        currentNode.leftChild = y.rightChild

        if y.rightChild != self.sentinel:
        	y.rightChild.parent = currentNode

        y.parent = currentNode.parent

        if currentNode.parent == self.sentinel:
        	self.root = y
        elif currentNode == currentNode.parent.rightChild:
        	currentNode.parent.rightChild = y
        else: 
        	currentNode.parent.leftChild = y

        y.rightChild = currentNode
        currentNode.parent = y

    '''
    Optional handy methods that you can imagine can start here
    '''

    #Made this to use 
    def walk(self, order, top): 
        '''
        Implements recursive based calls to traverse the tree, printing the node data in the specified 
        depth first traversals. 

        This was drawn and adapted from my traversal in BST. 
        '''
        if top != self.sentinel:
            if order == "pre-order":
                print(top.key),
                self.walk("pre-order", top.leftChild) #Recursion used to print first, then recurse
                self.walk("pre-order", top.rightChild)

            elif order == "in-order":
                self.walk("in-order", top.leftChild) #Here the recursion happens first, (inorder)
                print(top.key),
                self.walk("in-order", top.rightChild)

            elif order == "post-order":
                self.walk("post-order", top.leftChild) #Here we print last for postorder, after recursion
                self.walk("post-order", top.rightChild)
                print(top.key),
                
            else:
                print("Error, order {} undefined".format(order))


    #This function is required to search the tree (called within lab4.py main())
    def search(self, data):
        '''
        Searches the tree to see if it contains a particular value within a node. Returns true if there is an 
        occurence, false otherwise. 
        '''
        tmp = self.root
        while(tmp != self.sentinel):
            if tmp.key == data:
                return True
            else: 
                if data < tmp.key:
                    tmp = tmp.leftChild
                else:
                    tmp = tmp.rightChild
        return False



