import math

class MaxHeap(object):

    def __init__(self, size):
        # finish the constructor, given the following class data fields:
        self.__maxSize = size
        self.__length = 0 #Use this as the index to insert (starts at 1 for convention)
        self.__heap = [None]*(size+1) #Initializing the heap as empty (full of None)

    def getHeap(self):
        return self.__heap    

    def getMaxSize(self):
        return self.__maxSize
    
    def setMaxSize(self, ms):
        self.__maxSize = ms
        # May need to add more code here if you want to use this method

    def getLength(self):
        return self.__length
    
    def setLength(self, l):
        self.__length = l
    
    ''' Required Methods '''
    def insert(self, data):
        #Inserts a value into the heap and adjusts the heap to maintain property.
        self.__length += 1 #Happens regardless
        self.__heap[self.__length] = data

        parent_idx = self.__parent(self.__length)
        child_idx = self.__length

        # "Bubble" up to the top
        while(self.__heap[child_idx] > self.__heap[parent_idx]):
            self.__swap(child_idx, parent_idx)
            child_idx = parent_idx
            parent_idx = self.__parent(child_idx)


    def maximum(self):
        # return the max value in the heap
        return self.__heap[1]

    def extractMax(self):
        #Removes and returns the maximum value in the heap
        if self.__length < 1:
            print("Error: Nothing to extract")

        max_val = self.__heap[1] #Max value is stored at the first index
        self.__heap[1] = self.__heap[self.__length]
        self.__heap[self.__length] = None
        self.__length -= 1
        self.__heapify(1)

        return max_val
    
    def __heapify(self, node):
    	# Helper function for reshaping the array, maintaining the heap property
        
        while node < self.__length: 
            l = self.__lchild(node)
            r = self.__rchild(node)

            #Goals is to find the largest (rp) among the children, and adjust node
            rp = l
            if self.__heap[r] != None: 
                if self.__heap[r] > self.__heap[l]:
                    rp = r
            
            if rp > self.__length:
                break 

            if self.__heap[rp] > self.__heap[node]:
                self.__swap(rp, node)
                node = rp
            else: 
                break



    ''' Optional Private Methods can go after this line '''

    def __swap(self, idx1, idx2):
        #Used to swap values at corresponding indexes (idx1 and idx2)
        tmp1 = self.__heap[idx1]
        self.__heap[idx1] = self.__heap[idx2]
        self.__heap[idx2] = tmp1

    def __parent(self, node):
        #Returns the index of the parent of a node
        assert node >= 1
        if node == 1:
            return 1
        return node//2

    def __lchild(self, node):
        #Returns the index of the left child of a node
        return 2 * node

    def __rchild(self, node):
        #Returns the index of the right child of a node
        return (2 * node) + 1
