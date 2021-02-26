from MainA1 import Mainfun
from unigramIndex import Linkedlist
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import pickle




class QueryProcess:
    def __init__(self):
        self.Totdocmatch = 0
        self.comparison = 0
        self.fnamelist = []

    def preprocess(self, query):
        #normalisation
        result1 = query.lower()
        result2 = result1.translate(str.maketrans("","", string.punctuation))

        #tokenization
        tokens = word_tokenize(result2)
        
        #removing the stopping words
        stop_words = set(stopwords.words('english'))
        result3 = [w for w in tokens if w not in stop_words]

        #Stemming
        ps = PorterStemmer()
        result4query = []
        for word in result3:
            stword = ps.stem(word)
            result4query.append(stword)

        return(result4query)






    def MergingAlgo(self, postlink, operatorseq, maxDocID, filename):
        length = len(operatorseq)
        post1 = postlink[0]
        for i in range(length):
            
            operator = operatorseq[i]
            post2 = postlink[i+1]
            
            if (operator == 'AND'):
                p1 = post1.headptr
                p2 = post2.headptr
                post1 = self.MergeAND(p1, p2)
            elif(operator == 'OR'):
                p1 = post1.headptr
                p2 = post2.headptr
                post1 = self.MergeOR(p1, p2)
            elif(operator == 'AND NOT'):
                tp2 = post2.headptr
                resulttp = self.ListCompliment(tp2, maxDocID)
                p1 = post1.headptr
                p2 = resulttp.headptr
                post1 = self.MergeAND(p1, p2)
            elif(operator == 'OR NOT'):
                tp2 = post2.headptr
                resulttp = self.ListCompliment(tp2, maxDocID)
                p1 = post1.headptr
                p2 = resulttp.headptr
                post1 = self.MergeOR(p1, p2)
                


        self.Totdocmatch = post1.freq
        pt = post1.headptr
        while(pt is not None):
            self.fnamelist.append(filename[pt.IDval])
            pt = pt.next
        #post1.printingl()




        

    def MergeAND(self, ptr1, ptr2):
        answer = Linkedlist()
        while(ptr1 is not None and ptr2 is not None):
            if(ptr1.IDval == ptr2.IDval):
                answer.addnode(ptr1.IDval)
                ptr1 = ptr1.next
                ptr2 = ptr2.next
                self.comparison = self.comparison + 1
            elif(ptr1.IDval < ptr2.IDval):
                ptr1 = ptr1.next
                self.comparison = self.comparison + 2
            else:
                ptr2 = ptr2.next
                self.comparison = self.comparison + 2

        return answer



    def MergeOR(self, ptr1, ptr2):
        answer = Linkedlist()
        while(ptr1 is not None and ptr2 is not None):
            if(ptr1.IDval < ptr2.IDval):
                answer.addnode(ptr1.IDval)
                ptr1 = ptr1.next
                self.comparison = self.comparison + 1
            elif(ptr1.IDval > ptr2.IDval):
                answer.addnode(ptr2.IDval)
                ptr2 = ptr2.next
                self.comparison = self.comparison + 2
            else:
                answer.addnode(ptr1.IDval)
                ptr1 = ptr1.next
                ptr2 = ptr2.next
                self.comparison = self.comparison + 2

        while(ptr1 is not None):
            answer.addnode(ptr1.IDval)
            ptr1 = ptr1.next

        while(ptr2 is not None):
            answer.addnode(ptr2.IDval)
            ptr2 = ptr2.next

        return answer




    def ListCompliment(self, ptr, maxDocID):
        i = 0
        answer = Linkedlist()
        while(i < maxDocID and ptr is not None):
            if(i == ptr.IDval):
                i = i+1
                ptr = ptr.next
            elif(i < ptr.IDval):
                answer.addnode(i)
                i=i+1

        while(i < maxDocID):
            answer.addnode(i)
            i=i+1

        return(answer)





if __name__ == '__main__':
    with open('store.dat' , 'rb') as fr:
        tempomainobj = pickle.load(fr)
    #print(tempomainobj.docID)
    dictlist = tempomainobj.postinglist
    filename = tempomainobj.docname

    maxDocID = tempomainobj.docID
    
    
    n = int(input("Enter the number of Query: "))
    for i in range(n):
        query = input("Input Query: ")
        queryoperatorseq = input("Input Query operator: ").split(', ')
        
        Queryobj = QueryProcess()
        prepresult = Queryobj.preprocess(query)

        postlink = []
        for qword in prepresult:
            print(qword)
            LinkL = dictlist.get(qword)
            postlink.append(LinkL)

        Queryobj.MergingAlgo(postlink, queryoperatorseq, maxDocID, filename)

        print('Number of document matched: ', end=' ')
        print(Queryobj.Totdocmatch)
        #print()
        print('Number of comparison required: ', end=' ')
        print(Queryobj.comparison)
        #print()
        print('List of matched document name:')
        print(Queryobj.fnamelist)
        


