from sys import argv
from pQueue import pQueue

def main(argv):
	file_name = argv[1]

	file_object1 = open(file_name, 'r')

	#Wasn't sure how large to make the heap so this is dependent on the number of lines in the file
	count = 0 
	for line in file_object1: 
		count += 1

	file_object1.close()

	queue = pQueue(count)

	# Look through the file and execute the corresponding instructions
	file_object = open(file_name, 'r')
	for line in file_object:
		args = line.strip().split(' ')
		if args[0] == 'insert':
			queue.insert(int(args[1]))
		elif args[0] == 'print':
			queue.printQueue()
		elif args[0] == 'isEmpty':
			if(queue.isEmpty()):
				print("Empty")
			else:
				print("Not Empty")
		elif args[0] == 'maximum':
			print(queue.maximum())
		elif args[0] == 'extractMax':
			print(queue.extractMax())

	file_object.close()

if __name__ == "__main__":
    main(argv)
