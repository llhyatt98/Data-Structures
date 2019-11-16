from MaxHeap import MaxHeap
import math

class pQueue(object):
    def __init__(self,size) :
        # Build the Constructor
        self.__myHeap = MaxHeap(size)

    def insert(self, data):
        #Inserts a value into the queue, making sure to maintain the Max-Heap property. 
        self.__myHeap.insert(data)
        
    def maximum(self):
        #Returns the maxmimum value from the queue, but doesn't remove it. 
        return self.__myHeap.maximum()
    
    def extractMax(self):
        #Extracts the maximum value of the queue, removing it and returning it. 
        return self.__myHeap.extractMax()

    def isEmpty(self):
        # Return true when the priority queue is empty
        if len(self.__myHeap.getHeap()) == 0:
            return True
        return False
    
    def printQueue(self):
        #Prints the contents of the queue, with each element followed by a comma.
        arr = self.__myHeap.getHeap()
        print("Current Queue:", end = " ")
        i = 1
        while i <= self.__myHeap.getLength():
            if i == self.__myHeap.getLength():
                print(arr[i], end = "\n")
                break
            print(arr[i], end = ",")
            i += 1
        



    