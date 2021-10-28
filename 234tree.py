#demonstrates 234 tree
import sys

# IMPORTANTE
# Apenas o método de inserção está pronto


class DataItem:

	def __init__(self, dd):	#special method to create object
        #with instances customized to a specific initial state
		self.dData = dd#one piece of data

	def displayItem(self):	#format " /27"
		print('/', self.dData)
        #end class DataItem

class Node:
	#as private instance variables don't exist in Python,
	#hence using a convention: name prefixed with an underscore, to treat them as non-public part
	_ORDER = 4
	def __init__(self):
		self._numItems = 0
		self._pParent = None
		self._childArray = []	#array of nodes
		self._itemArray = []	#array of data

		for j in range(self._ORDER):	#initialize arrays
			self._childArray.append(None)
		for k in range(self._ORDER - 1):
			self._itemArray.append(None)

	#connect child to this node
	def connectChild(self, childNum, pChild):
		self._childArray[childNum] = pChild
		if pChild:
			pChild._pParent = self

	#disconnect child from this node, return it
	def disconnectChild(self, childNum):
		pTempNode = self._childArray[childNum]
		self._childArray[childNum] = None
		return pTempNode

	def getChild(self, childNum):
		return self._childArray[childNum]

	def getParent(self):
		return self._pParent

	def getSibling(self, childNum):
		return (self._pParent).getChild(childNum)

	def isLeaf(self):
		return not self._childArray[0]

	def getNumItems(self):
		return self._numItems

	def getItem(self, index):	#get DataItem at index
		return self._itemArray[index]

	def getChildNum(self): 	#find what child this node is
		parent = self.getParent
		if(parent):	#if current node is not root
			tempValue = self._itemArray[0]
			for i in reversed(range(parent.getNumItems())):
				if tempValue < parent._itemArray[i]:
					childNum = i
				else:
					childNum = parent.getNumItems() + 1
					return childNum
		else:
			return -1
		
		return childNum

	def isFull(self):
		return self._numItems==self._ORDER - 1

	def findItem(self, key):	#return index of
		for j in range(self._ORDER-1):	#item (within node)
			if not self._itemArray[j]:	#if found,
				break	#otherwise,
			elif self._itemArray[j].dData == key:	#return -1
				return j
		return -1
	#end findItem

	def insertItem(self, pNewItem):
		#assumes node is not full
		self._numItems += 1#will add new item
		newKey = pNewItem.dData	#key of new item

		for j in reversed(range(self._ORDER-1)):	#start on right,	#examine items
			if self._itemArray[j] == None:	#if item null,
				pass	#go left one cell
			else:	#not null,
				itsKey = self._itemArray[j].dData	#get its key
				if newKey < itsKey:	#if it's bigger
					self._itemArray[j+1] = self._itemArray[j]	#shift it right
				else:
					self._itemArray[j+1] = pNewItem	#insert new item
					return j+1#return index to new item
			#end else (not null)
		#end for 	#shifted all items,
		self._itemArray[0] = pNewItem	#insert new item
		return 0
	#end insertItem()

	def removeLargestItem(self):	#remove largest item
		#assumes node not empty
		pTemp = self._itemArray[self._numItems-1]	#save item
		self._itemArray[self._numItems-1] = None	#disconnect it
		self._numItems -= 1#one less item
		return pTemp#return item

	def removeItem(self, index): #remove specific item 
		pTemp = self._itemArray[index]	#save item
		self._itemArray[index] = None	#disconnect it
		self._numItems -= 1				#one less item
		return pTemp					#return item

	def displayNode(self):	#format "/24/56/74"
		for j in range(self._numItems):
			self._itemArray[j].displayItem()	#format "/56"
		#print('/')	#final "/"

#end class Node

class Tree234:
	#as private instance variables don't exist in Python,
	#hence using a convention: name prefixed with an underscore, to treat them as non-public part
	def __init__(self):
		self._pRoot = Node()	#root node

	def inOrder(self, node):
		for (i, item) in enumerate([node._childArray, node._itemArray]):
			if node._childArray[i]: 
				self.inOrder(node._childArray[i])
			yield item
		if node._childArray[-1]: 
			self.inOrder(node._childArray[-1])

	def find(self, key):
		pCurNode = self._pRoot	#start at root
		while True:
			childNumber=pCurNode.findItem(key)
			if childNumber != -1:
				return childNumber	#found it
			elif pCurNode.isLeaf():
				return -1#can't find it
			else:	#search deeper
				pCurNode = self.getNextChild(pCurNode, key)
		#end while

	def insert(self, dValue):	#insert a DataItem
		pCurNode = self._pRoot
		pTempItem = DataItem(dValue)

		while True:
			if pCurNode.isFull():	#if node full,
				self.split(pCurNode)	#split it
				pCurNode = pCurNode.getParent()	#back up
					#search once
				pCurNode = self.getNextChild(pCurNode, dValue)
			#end if(node is full)

			elif pCurNode.isLeaf():	#if node is leaf,
				break	#go insert
			#node is not full, not a leaf; so go to lower level
			else:
				pCurNode = self.getNextChild(pCurNode, dValue)
		#end while
		pCurNode.insertItem(pTempItem)	#insert new item
	#end insert()

	def remove(self, dValue):
		root = self._pRoot		#start from root
		pCurNode = self._pRoot		#start from root

		while True: 				#find node
			index = pCurNode.findItem(dValue)

			if index != -1: 		#found it
				break 				#proceed to remove	
			elif pCurNode.isLeaf():	#can't find it
				return -1			#finish remove
			else:					#search deeper
				pCurNode = self.getNextChild(pCurNode, dValue)
		#end while
		
		numItems = pCurNode.getNumItems()

		parent = pCurNode.getParent()

		#case 1.1
		if pCurNode.isLeaf() and pCurNode._numItems > 2: #proceed with remove
			pCurNode.removeItem(index)
			return dValue
			
		#case 1.2.1 - If the node containing x has 3-node or 4-node siblings

		#case 1.2.2 - If both the siblings are 2-node but the parent node is either a 3-node or a 4-node
		elif pCurNode.isLeaf() and pCurNode._numItems == 1:
			childNum = pCurNode.getChildNum()
			rightSibling = pCurNode.getSibling(childNum +1)	#get siblings
			leftSibling = pCurNode.getSibling(childNum -1)
			
			#moving elements from sibling to parent and from parent to current node
			if leftSibling.getNumItems() >= 2:
				tempSibling = leftSibling.removeLargestItem()
				temp = parent.removeItem(childNum)
				pCurNode.insertItem(temp)
				parent.insertItem(tempSibling)
			elif rightSibling.getNumItems() >= 2:
				tempSibling = rightSibling.removeItem(0)
				temp = parent.removeItem(childNum)
				pCurNode.insertItem(temp)
				parent.insertItem(tempSibling)
			elif parent.getNumItems() >= 2:
				if(rightSibling):
					temp = parent.removeItem(childNum)
					tempSibling = rightSibling.removeItem(0)
					parent.disconnectChild(childNum +1)
				elif(leftSibling):
					temp = parent.removeItem(childNum -1)
					tempSibling = leftSibling.removeItem(0)
					parent.disconnectChild(childNum -1)
				
				pCurNode.insertItem(temp)
				pCurNode.insertItem(tempSibling)
			#end if
			index = find(dValue)			
			pCurNode.removeItem(index)
			return dValue

		#case 1.2.3 - If both siblings and the parent node are a 2-node
		elif parent != None and parent.getChild(0).getNumItems() == 1 and parent.getChild(1).getNumItems() == 1 and parent.getNumItems() == 1:
			valueA = parent.getChild(0).removeLargestItem()
			valueB = parent.getChild(1).removeLargestItem()

			parent.insertItem(valueA)
			parent.insertItem(valueB)
		

		#case 2 - If dValue is in an internal node and 
		if pCurNode.isLeaf() == False:

			#2.1 - If the element's left child has at least 2 keys, replace the element with its predecessor, p, and then recursively delete p.
			if pCurNode.getChild(index).getNumItems() == 2:
				pCurNode._itemArray[index] = pCurNode.getChild(0).removeLargestItem()

			#2.2 - If the element's right child has at least 2 keys, replace the element with its successor, s, and then recursively delete s.
			elif pCurNode.getChild(index + 1).getNumItems() == 2:
				pCurNode._itemArray[index] = pCurNode.getChild(index + 1).removeItem(0)

			#2.3 - If both children have only 1 key (the minimum), merge the right child into the left child and include the element, k, in the left child. Free the right child and recursively delete k from the left 
			elif pCurNode.getChild(index).getNumItems() == 1 and pCurNode.getChild(index + 1).getNumItems() == 1:
				valueA = pCurNode.getChild(index).removeLargestItem()
				valueB = pCurNode.getChild(index + 1).removeLargestItem()

				pCurNode.insertItem(valueA)
				pCurNode.insertItem(valueB)

				for i in pCurNode._itemArray:
					if pCurNode._itemArray[i] == dValue:
						pCurNode._itemArray[i] = None
		
	def split(self, pThisNode):	#split the node
		#assumes node is full
		
		pItemC = pThisNode.removeLargestItem()	#remove items from
		pItemB = pThisNode.removeLargestItem()	#this node
		pChild2 = pThisNode.disconnectChild(2)	#remove children
		pChild3 = pThisNode.disconnectChild(3)	#from this node

		pNewRight = Node()	#make new node

		if pThisNode == self._pRoot:	#if this is the root,
			self._pRoot = Node()	#make new root
			pParent = self._pRoot	#root is our parent
			self._pRoot.connectChild(0, pThisNode)	#connect to parent
		else:	#this node not the root
			pParent = pThisNode.getParent()	#get parent

		#deal with parent
		itemIndex = pParent.insertItem(pItemB)	#item B to parent
		n = pParent.getNumItems()	#total items?

		j = n-1#move parent's
		while j > itemIndex:	#connections
			pTemp = pParent.disconnectChild(j)	#one child
			pParent.connectChild(j+1, pTemp)	#to the right
			j -= 1
				#connect newRight to parent
		pParent.connectChild(itemIndex+1, pNewRight)

		#deal with newRight
		pNewRight.insertItem(pItemC)	#item C to newRight
		pNewRight.connectChild(0, pChild2)	#connect to 0 and 1
		pNewRight.connectChild(1, pChild3)	#on newRight
	#end split()

	#gets appropriate child of node during search of value
	def getNextChild(self, pNode, theValue):
		#assumes node is not empty, not full, not a leaf
		numItems = pNode.getNumItems()
		
		for j in range(numItems):	#for each item in node
			if theValue < pNode.getItem(j).dData:	#are we less?
				return pNode.getChild(j)	#return left child
		else:	#end for 	#we're greater, so
			return pNode.getChild(j + 1)	#return right child

	def displayTree(self):
		self.recDisplayTree(self._pRoot, 0, 0)

	def recDisplayTree(self, pThisNode, level, childNumber):
		print('level=', level, 'child=', childNumber)	#display this node
		pThisNode.displayNode()

		#call ourselves for each child of this node
		numItems = pThisNode.getNumItems()
		for j in range(numItems+1):
			pNextNode = pThisNode.getChild(j)
			if pNextNode:
				self.recDisplayTree(pNextNode, level+1, j)
			else:
				return
	#end recDisplayTree()
#end class Tree234

pTree = Tree234()
pTree.insert(50)
pTree.insert(40)
pTree.insert(60)
pTree.insert(30)
pTree.insert(70)


#as Python doesn't support switch, simulating the same with dictionary and functions
def show():
	pTree.displayTree()

def insert():
	value = int(input('Enter value to insert: '))
	pTree.insert(value)

def find():
	value = int(input('Enter value to find: '))
	found = pTree.find(value)
	if found != -1:
		print('Found', value)
	else:
		print ('Could not find', value)

def remove():
	value = int(input('Enter value to delete: '))
	removed = pTree.remove(value)
	if removed != -1:
		print('Removed ', value)
	else:
		print('Can\'t find ', value, ' -> Remove unsuccessful')

def exit():
	confirm = input('Confirm exit (y/n)? ')
	if confirm == 'y':
		sys.exit()
	elif confirm == 'n':
		return
	else:
		exit()


case = {
	's' : show,
	'i' : insert,
	'f' : find,
    'r': remove,
	'e': exit
}
#switch simulation completed

while True:
	choice = input('Enter first letter of show, insert, find, remove or exit: \ns to show\ni to insert\nf to find\nr to remove\ne to exit\n')
	if case.get(choice, None):
		case[choice]()
	else:
		print ('Invalid entry')
#end while
del pTree
#end
