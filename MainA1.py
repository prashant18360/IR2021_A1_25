import glob
import os.path
from os import path
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from unigramIndex import Linkedlist
from os.path import split
from os.path import basename
import ntpath
import pickle
import sys
sys.setrecursionlimit(10000)



class Mainfun:
    def __init__(self):
        self.postinglist = {}
        self.docID = 0
        self.docname = []

    def preprocessing(self, content):
        #normalisation
        result1 = content.lower()
        result2 = result1.translate(str.maketrans("","", string.punctuation))

        #tokenization
        tokens = word_tokenize(result2)

        #removing the stopping words
        stop_words = set(stopwords.words('english'))
        result3 = [w for w in tokens if w not in stop_words]

        #Stemming
        ps = PorterStemmer()
        result4dict = {}
        for word in result3:
            stword = ps.stem(word)
            if(stword not in result4dict):
                result4dict[stword] = self.docID

        return(result4dict)


    def invertedindex(self, resultlist):
        for term in resultlist:
            if(term not in self.postinglist):
                linkedlistobject = Linkedlist(term)
                self.postinglist[term] = linkedlistobject
                linkedlistobject.addnode(resultlist.get(term))
            else:
                tempobject = self.postinglist.get(term)
                tempobject.addnode(resultlist.get(term))

        #return(postinglist)



    def printpostlist(self):
        for t in self.postinglist:
            print(t, end=" ")
            #objlit = postlist[t]
            #objlit.printingl()
            self.postinglist.get(t).printingl()
            print()



    def fnamebypath(self, fpath):
        first, last = ntpath.split(fpath)
        return last or ntpath.basename(first)



if __name__ == '__main__':
    # set the directory path of dataset
    directorypath = 'D:\IIITD\SEMESTER 6\Information Retrieval\Assignment\A1\stories\**\*'
    #ind = 0
    #postinglist = {}
    mainobj = Mainfun()
    
    count = 0
    for filepath in glob.glob(directorypath, recursive=True):
        if (path.isfile(filepath) and not filepath.endswith('.html')):
            count = count +1
            filename = mainobj.fnamebypath(filepath)
            mainobj.docname.append(filename)
            #print(filepath)
            with open(filepath, 'rb') as file:
                filecontent = file.read().decode(errors='replace')
            
            #print(len(filecontent))
            #preprocessing(filecontent)
            
            preprocessresult = {}

            preprocessresult = mainobj.preprocessing(filecontent)
            mainobj.invertedindex(preprocessresult)

            mainobj.docID = mainobj.docID+1
    
    #print(count)
    #print(len(postinglist))
    print("Normal Finished")

    with open('store.dat' , 'wb') as fp:
        pickle.dump(mainobj, fp)
    
    print("Writing finished")

    '''with open('store.dat' , 'rb') as fr:
        tempomainobj = pickle.load(fr)

    print("Reading finished")'''

    #tempomainobj.printpostlist()
    print(len(mainobj.postinglist))

    #mainobj.printpostlist()
    #print(mainobj)
    print("complete Finished")



