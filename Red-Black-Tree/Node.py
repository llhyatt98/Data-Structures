# TreeNode is a class used to represent nodes in a BST
class RB_Node(object):
    def __init__(self, key, left = None, right = None, parent = None, color = 'red'):
        self.key = key
        self.leftChild = left
        self.rightChild = right
        self.parent = parent
        self.color = color

    def print_(self):
        print("*"*40)
        print('''
        key     = {}
        parent  = {}
        left    = {}
        right   = {}
        color   = {}
        '''.format(self.key, self.parent.key, self.leftChild.key, self.rightChild.key, self.color))
        print("*"*40)

    def hasLeftChild(self):
        return self.leftChild.parent == self and self.leftChild != self

    def hasRightChild(self):
        return self.rightChild.parent == self and self.rightChild != self

    def isLeftChild(self):
        return self.parent.leftChild == self and self.parent != self

    def isRightChild(self):
        return self.parent.rightChild == self and self.parent != self

    def isRoot(self):
        return self.parent != self and self.parent == self.parent.parent

    def isLeaf(self):
        return not (self.hasLeftChild() or self.hasRightChild())

    def hasOnlyOneChild(self):
        return bool(self.leftChild) ^ bool(self.rightChild)

    def hasAnyChildren(self):
        return bool(self.hasLeftChild() or self.hasRightChild())

    def hasBothChildren(self):
        return self.hasLeftChild() and self.hasRightChild()

    def replaceNodeData(self, key, left = None, right = None, color = 'red'):
        self.key = key
        self.leftChild = left
        self.rightChild = right
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self
        self.color = color

    def findSuccessor(self):
        # successor's key is the next highest key from the current node

        succ = None
        # if node has a right child
        if self.hasRightChild():
            # then successor is the min of the right subtree
            succ = self.rightChild.findMin()
        elif self.parent: # node has no right child, but has a parent
            if self.isLeftChild(): # node is a left child
                succ = self.parent # then succ is the parent
            else: # node is right child, and has not right child
                # remove parent's rightChild reference
                self.parent.rightChild = None
                # recursively find call findSuccessor on parent
                succ = self.parent.findSuccessor()
                # replace parent's rightChild reference
                self.parent.rightChild = self
        return succ

    def findMin(self):
        # findMin travels across the leftChild of every node, and returns the
        # node who has no leftChild. This is the min value of a subtree

        currentNode = self
        while currentNode.hasLeftChild():
            currentNode = currentNode.leftChild
        return currentNode

    def __iter__(self):
        # __iter__ defines an iterator for objects of the RB_Node class
        # allows for operations like:
        # for node in Tree:
        # ... print( Tree.get(node) )

        if self:
            if self.hasLeftChild():
                for elem in self.leftChild:
                    yield elem
            yield self.key
            if self.hasRightChild():
                for elem in self.rightChild:
                    yield elem
