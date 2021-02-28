from MainA1 import Mainfun
from unigramIndex import Linkedlist
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pickle




class QueryProcess:
    def __init__(self):
        '''Attribute for each Query processing results, Totdocmatch for total documentmatch,
        comparison for total comparison done in a merging algo, and fnamelist for list of all matched file'''
        self.Totdocmatch = 0
        self.comparison = 0
        self.fnamelist = []


    '''function  for preprocessing of a query including converting into
    lower letter, remove punctuation, tokenization, remove stopping words and Lemmatization'''
    def preprocess(self, query):
        #normalisation
        result1 = query.lower()
        result2 = result1.translate(str.maketrans("","", string.punctuation))

        #tokenization
        tokens = word_tokenize(result2)
        
        #removing the stopping words
        stop_words = set(stopwords.words('english'))
        result3 = [w for w in tokens if w not in stop_words]

        #Lemmatization
        lem = WordNetLemmatizer()
        result4query = []
        for word in result3:
            lmword = lem.lemmatize(word)
            result4query.append(lmword)

        return(result4query)






    def MergingAlgo(self, postlink, operatorseq, maxDocID, filename):
        length = len(operatorseq)
        #retrieve first posting list 
        post1 = postlink[0]

        #Process the query from Left to Right, Iterate the query starting from query operator list
        for i in range(length):

            #REtrieve the operator and second postinglist
            operator = operatorseq[i]
            post2 = postlink[i+1]
            
            if (operator == 'AND'):
                p1 = post1.headptr
                p2 = post2.headptr
                
                #Calling the specific intersection Merge Algo
                post1 = self.MergeAND(p1, p2)

                '''checking the resultant postinglist will be null or not,
                if it is null then this post1 will move further to the next index in query list'''
                if(post1.freq == 0):
                    post1 = postlink[i+1]
                    i=i+1
            elif(operator == 'OR'):
                p1 = post1.headptr
                p2 = post2.headptr
                
                #Calling the specific Union Merge Algo
                post1 = self.MergeOR(p1, p2)

                '''checking the resultant postinglist will be null or not,
                if it is null then this post1 will move further to the next index in query list'''
                if(post1.freq == 0):
                    post1 = postlink[i+1]
                    i=i+1
            elif(operator == 'AND NOT'):
                tp2 = post2.headptr
                #Computing the complement of second posting list
                resulttp = self.ListCompliment(tp2, maxDocID)
                p1 = post1.headptr
                p2 = resulttp.headptr
                
                #Calling the specific intersection Merge Algo
                post1 = self.MergeAND(p1, p2)
                
                '''checking the resultant postinglist will be null or not,
                if it is null then this post1 will move further to the next index in query list'''
                if(post1.freq == 0):
                    post1 = postlink[i+1]
                    i=i+1
            elif(operator == 'OR NOT'):
                tp2 = post2.headptr
                #Computing the complement of second posting list 
                resulttp = self.ListCompliment(tp2, maxDocID)
                p1 = post1.headptr
                p2 = resulttp.headptr
                
                #Calling the specific Union Merge Algo
                post1 = self.MergeOR(p1, p2)

                '''checking the resultant postinglist will be null or not,
                if it is null then this post1 will move further to the next index in query list'''
                if(post1.freq == 0):
                    post1 = postlink[i+1]
                    i=i+1



        '''After completing the merging Algo, the final resultant posting list will be post1
        retreiving the Document name acc. to the docID present in the final posting list'''
        self.Totdocmatch = post1.freq
        pt = post1.headptr
        while(pt is not None):
            self.fnamelist.append(filename[pt.IDval])
            pt = pt.next


        

    def MergeAND(self, ptr1, ptr2):
        answer = Linkedlist()
        #ptr1 and ptr2 , iterate the both pointer till the end of the linkedlist, both linkedlist are already in sorted form
        while(ptr1 is not None and ptr2 is not None):
            if(ptr1.IDval == ptr2.IDval):
                
                #here when both pointer node value matches, then add the nodevalue to the answer linked list
                answer.addnode(ptr1.IDval)
                
                #move both pointer by one node
                ptr1 = ptr1.next
                ptr2 = ptr2.next
                
                #here counting the comarison, in this algo this is the first comparison so just add 1 to the comparison variable
                self.comparison = self.comparison + 1
                
            elif(ptr1.IDval < ptr2.IDval):
                
                #here the ptr1 is behind the ptr2, so just move ptr1 by one node
                ptr1 = ptr1.next
                
                #here counting the comarison, in this algo this is the second comparison so just add 2 to the comparison variable
                self.comparison = self.comparison + 2
                
            else:
                #here in the else, the ptr2 is behind the ptr1, so just move ptr2 by one node
                ptr2 = ptr2.next
                
                #here counting the comarison, in this algo 2 comparison are already done in above, so just add 2 to the comparison variable
                self.comparison = self.comparison + 2

        return answer



    def MergeOR(self, ptr1, ptr2):
        answer = Linkedlist()
        
        #ptr1 and ptr2 , iterate the both pointer till the end of the linkedlist, both linkedlist are already in sorted form
        while(ptr1 is not None and ptr2 is not None):
            
            if(ptr1.IDval < ptr2.IDval):
                #add the nodevalue to the answer linked list
                answer.addnode(ptr1.IDval)
                
                #here the ptr1 is behind the ptr2, so just move ptr1 by one node
                ptr1 = ptr1.next
                
                #here counting the comarison, in this algo this is the first comparison so just add 1 to the comparison variable
                self.comparison = self.comparison + 1
                
            elif(ptr1.IDval > ptr2.IDval):
                #add the nodevalue to the answer linked list
                answer.addnode(ptr2.IDval)
                
                #the ptr2 is behind the ptr1, so just move ptr2 by one node
                ptr2 = ptr2.next
                
                #here counting the comarison, in this algo this is the second comparison so just add 2 to the comparison variable
                self.comparison = self.comparison + 2
            else:
                #here in the else, when both pointer node value matches, then add the nodevalue to the answer linked list
                answer.addnode(ptr1.IDval)
                
                #move both pointer by one node
                ptr1 = ptr1.next
                ptr2 = ptr2.next
                
                #here counting the comarison, in this algo 2 comparison are already done in above, so just add 2 to the comparison variable
                self.comparison = self.comparison + 2

        #if ptr2 becomes none but ptr1 is not none, so just add the remaining node value of ptr1 to the answer linkedlsit 
        while(ptr1 is not None):
            answer.addnode(ptr1.IDval)
            ptr1 = ptr1.next

        #if ptr1 becomes none but ptr2 is not none, so just add the remaining node value of ptr2 to the answer linkedlsit
        while(ptr2 is not None):
            answer.addnode(ptr2.IDval)
            ptr2 = ptr2.next

        return answer



    #Function for finding the complement of a linkedlist
    def ListCompliment(self, ptr, maxDocID):
        i = 0
        answer = Linkedlist()
        #here maxDOCID is representing the number that the max docID that allocate to the document(0-maxdocID) 
        while(i < maxDocID and ptr is not None):
            #if the docID present in the list, so just move to the next node
            if(i == ptr.IDval):
                i = i+1
                ptr = ptr.next
            #if the docID not present in the list, so just add to the answer linkedlist
            elif(i < ptr.IDval):
                answer.addnode(i)
                i=i+1
        #adding the remaining docID to the answer linkedlist
        while(i < maxDocID):
            answer.addnode(i)
            i=i+1

        return(answer)





if __name__ == '__main__':
    #Deserailization of MainA1 class object, in which unigram data structure has stored
    with open('store.dat' , 'rb') as fr:
        tempomainobj = pickle.load(fr)
    
    #retriving the unigram data structure, list of all doc, max doc ID
    dictlist = tempomainobj.postinglist
    filename = tempomainobj.docname
    maxDocID = tempomainobj.docID
    
    #Input the no. of query from the User
    n = int(input("Enter the number of Query: "))
    
    for i in range(n):
        #input the query and query operator 
        query = input("Input Query: ")
        queryoperatorseq = input("Input Query operator: ").split(', ')

        #Preprocessing of Query
        Queryobj = QueryProcess()
        prepresult = Queryobj.preprocess(query)

        #Retriving the postinglist of each tokenize word of a query in postlink[] list 
        postlink = []
        for qword in prepresult:
            LinkL = dictlist.get(qword)
            postlink.append(LinkL)

        #Process the Query and query operator by merging Algoruthm
        Queryobj.MergingAlgo(postlink, queryoperatorseq, maxDocID, filename)
        

        #print the desirable result of a query
        print('Number of document matched: ', end=' ')
        print(Queryobj.Totdocmatch)
        print('Number of comparison Done in Merging Algorithm: ', end=' ')
        print(Queryobj.comparison)
        print('List of matched document name:')
        print(Queryobj.fnamelist)
        


