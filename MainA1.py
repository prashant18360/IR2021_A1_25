import glob
import os.path
from os import path
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from unigramIndex import Linkedlist
from os.path import split
from os.path import basename
import ntpath
import pickle
import sys
#this is only for serializing the class object by pickle dump 
sys.setrecursionlimit(10000)



class Mainfun:
    '''Attribute are postinglist which is dictionary type data structure which is used for
    each unique words and their linkedlist containing all the docID in which word are present,
    docname which is a list of all document names, and docID maintaining the ID of document'''  
    def __init__(self):
        self.postinglist = {}
        self.docID = 0
        self.docname = []

    '''function  for preprocessing of a document content including converting into
    lower letter, remove punctuation, tokenization, remove stopping words and Lemmatization'''
    def preprocessing(self, content):
        #normalisation
        result1 = content.lower()
        result2 = result1.translate(str.maketrans("","", string.punctuation))

        #tokenization
        tokens = word_tokenize(result2)

        #removing the stopping words
        stop_words = set(stopwords.words('english'))
        result3 = [w for w in tokens if w not in stop_words]

        #Lemmatization
        lem = WordNetLemmatizer()
        result4dict = {}
        for word in result3:
            lmword = lem.lemmatize(word)
            #here just only store the unique words of a file, 
            if(lmword not in result4dict):
                result4dict[lmword] = self.docID

        #now returning the result4dict, it is a dictionary type which contain all words from all document and their docID (key is words, value is docID)
        return(result4dict)

    '''Function for creating the unigram data structure containing all unique words and their linked list containing docID'''
    def Unigraminvertedindex(self, resultlist):
        #iterate all words in a resultlist
        for term in resultlist:
            
            #checking the particular words is present or not in a unigram data structure (postling list)
            if(term not in self.postinglist):
                
                #Here word is not present then creating the new linked list of a new entry
                linkedlistobject = Linkedlist(term)

                #adding the docID in a linkedlist
                linkedlistobject.addnode(resultlist.get(term))#resultlist.get(term) will give the docID

                #storing the word and linkedlist in a unigram data structure
                self.postinglist[term] = linkedlistobject
                
            else:
                #Here word is present then retrieving the particular word's linkedlist
                tempobject = self.postinglist.get(term)
                #adding the docID in a linkedlist
                tempobject.addnode(resultlist.get(term))



    #Extracting the Document name from path of a document
    def fnamebypath(self, fpath):
        first, last = ntpath.split(fpath)
        return last or ntpath.basename(first)



if __name__ == '__main__':
    # set the directory's path of dataset
    directorypath = 'D:\IIITD\SEMESTER 6\Information Retrieval\Assignment\A1\stories\**\*'

    #creating the class object
    mainobj = Mainfun()
    
    #Here golb is used for the finding the all file path in a directory and also the inner directory file path
    for filepath in glob.glob(directorypath, recursive=True):
        if (path.isfile(filepath) and not filepath.endswith('.html')):

            #Calling the function which extract filename from path of a file and then store in a docname list 
            filename = mainobj.fnamebypath(filepath)
            mainobj.docname.append(filename)

            #Reading of file
            with open(filepath, 'rb') as file:
                filecontent = file.read().decode(errors='replace')
            
            preprocessresult = {}
            #Calling the function of preprocessing of file content
            preprocessresult = mainobj.preprocessing(filecontent)

            #Calling the function of creating the unigram data structure of each unique words of all file 
            mainobj.Unigraminvertedindex(preprocessresult)

            mainobj.docID = mainobj.docID+1

    #Serialize the MainA1 class object in store.dat file 
    with open('store.dat' , 'wb') as fp:
        pickle.dump(mainobj, fp)




