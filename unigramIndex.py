class Node:
        def __init__(self, IDval=None):
                self.IDval = IDval
                self.next = None

class Linkedlist:
        def __init__(self, term=None):
                self.term = term
                self.freq = 0
                self.headptr = None

        def addnode(self, IDdata):
                newNode = Node(IDdata)
                if(self.headptr is None):
                        self.headptr = newNode
                        self.freq = self.freq + 1
                        return
                temp = self.headptr
                while temp.next is not None:
                        temp = temp.next
                temp.next = newNode
                self.freq = self.freq + 1

        def printingl(self):
                printval = self.headptr
                while printval is not None:
                        print(printval.IDval, "-->", end=" ")
                        printval = printval.next
                #print(self.term)
                #print(self.freq)



#if __name__ == '__main__':
        #print('running linkedlist file')

"""list1 = Linkedlist("Accenture")

a = list(map(int, input('Enter input:').strip().split()))
for x in a:
        list1.addnode(x)

list1.printingl()


list2 = Linkedlist("vacant")
b = list(map(int, input('Enter input:').strip().split()))
for y in b:
        list2.addnode(y)

list2.printingl()"""

