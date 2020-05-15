# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 15:24:44 2020

@author: Mohammad Osama Rajput
"""
from nltk.stem import PorterStemmer



'''KINDLY EXECUTE THE MAIN_EXECUTION() METHOD IN THE END TO BEGIN WITH'''




#PREPROCESSING
def return_stopwords(): #removal of stop words by stop list
    stopfile = open("\Stopword-list.txt","r")
    stopwords = []
    for line in stopfile:
        stopwords+=line.split()
    return stopwords

def preprocessing_list(terms):
        i=0
        stemmer = PorterStemmer()
        stop_list=[]
        stop_list = return_stopwords()
        f1 = open("\checker.txt","w")
        while i<len(terms):
            terms[i][0]=terms[i][0].casefold() #CASEFOLDING    
            terms[i][0]=terms[i][0].replace(':','') #DATA CLEANING
            terms[i][0]=terms[i][0].replace("'",'')
            terms[i][0]=terms[i][0].replace('"','')
            
            
            if(terms[i][0].find('...')>-1): #ELIMINATING TRIPLE DOTS
                tripdot_splitter=terms[i][0].split('...')
                terms[i][0]=tripdot_splitter[0]
                terms[i].append(tripdot_splitter[1])
                    
            if(terms[i][0].find(']')>-1 and terms[i][0].find('[')>-1): #ELIMINATING BRACKET SEPARATION
                terms[i][0]=terms[i][0].replace('[','')
                square_splitter=terms[i][0].split(']')
                terms[i][0]=square_splitter[0]
                terms[i].append(square_splitter[1])
                
            if(terms[i][0].find('.')>-1 and terms[i][0][-1]!='.'): #ELIMINATING DOT SEPARATION
                dot_splitter=terms[i][0].split('.')
                terms[i][0]=dot_splitter[0]
                terms[i].append(dot_splitter[1])
        
            terms[i][0]=terms[i][0].replace('.','') #DATA CLEANING
            terms[i][0]=terms[i][0].replace('?','')
            terms[i][0]=terms[i][0].replace(',','')
            
            if(terms[i][0] in stop_list): #REMOVAL OF STOPWORDS
                terms[i][0]=''
                if(terms[i][-1]!=terms[i][0] and terms[i][-1] in stop_list):
                    terms[i][-1]=''
                
            
            terms[i][0]=stemmer.stem(terms[i][0]) #PORTER STEMMER
            if(terms[i][-1]!=terms[i][0]):
                terms[i][-1]=stemmer.stem(terms[i][-1])


            
            if(terms[i][0] or terms[i][-1]): #WRITING TO FILE TO CHECK TERMS MANUALLY
                f1.write(terms[i][0])
                if(terms[i][-1]!=terms[i][0]):
                    f1.write("  ")
                    f1.write(terms[i][-1])
                    f1.write('\n')
            i+=1
        

def inverted_index():
    i=0
    dict_inverted = dict()
    
    for i in range(56):  #CREATING INDEX OF ALL DOCS
        f = open("\Trump Speechs\speech_"+str(i)+".txt","r")
        arrayy = []    
        #FILING
        for line in f:
            for word in line.split():
                arrayy+=[word.split()]
                
        preprocessing_list(arrayy) #PREPROCESSING FUNCTION
        dict_inverted[i]=arrayy
        
    return dict_inverted


def query_inverted_index(query):                
    not_flag = 0
    result_set = set()
    
    if('not' in query or 'NOT' in query): #DEALING WITH NOT IN QUERY
        not_flag=1
        query=query.replace('not ','')
        query=query.replace('NOT ','')
        query=query.replace('not(','')
        query=query.replace('NOT(','')
        query=query.replace(')','')
        
    
    query_splitter=query.split()
    if(len(query_splitter)>2):
        if('(' in query_splitter):
            print('Complex Boolean Query') #COMPLEX BOOLEAN QUERIES
            separator = query_splitter.index('(')
            m=separator+1
            my_set=set()
            new_set1 = set()
            new_set1 = search_inverted(query_splitter[0])
            if(query_splitter[1]=='and' or query_splitter[1]=='AND'):
                new_set2 = search_inverted(query_splitter[m])
                while(query_splitter[m+1]!=')'):
                    if(query_splitter[m+1]=='or' or query_splitter[m+1]=='OR'):
                        new_set3 = search_inverted(query_splitter[m+2])
                        my_set=new_set2.union(new_set3)
                        new_set2=new_set3
                    if(query_splitter[m+1]=='and' or query_splitter[m+1]=='AND'):
                        new_set3 = search_inverted(query_splitter[m+2])
                        my_set=new_set2.intersection(new_set3)
                        new_set2=new_set3
                    m+=2
                result_set=my_set.intersection(new_set1)        
                    
            if(query_splitter[1]=='or' or query_splitter[1]=='OR'):
                new_set2 = search_inverted(query_splitter[m])
                while(query_splitter[m+1]!=')'):
                    if(query_splitter[m+1]=='or' or query_splitter[m+1]=='OR'):
                        new_set3 = search_inverted(query_splitter[m+2])
                        my_set=new_set2.union(new_set3)
                        new_set2=new_set3
                    if(query_splitter[m+1]=='and' or query_splitter[m+1]=='AND'):
                        new_set3 = search_inverted(query_splitter[m+2])
                        my_set=new_set2.intersection(new_set3)
                        new_set2=new_set3
                    m+=2
                result_set=my_set.union(new_set1)
                
            
        else:
            print('Not Complex Boolean Query') #OTHER BOOLEAN QUERIES
            l=0
            for l in range(len(query_splitter)):
                if(query_splitter[l]==query_splitter[-1]):
                    break

                if(query_splitter[l+1]=='or' or query_splitter[l+1]=='OR'):
                    new_set1 = set()
                    new_set2 = set()
                    new_set1 = search_inverted(query_splitter[l])
                    new_set2 = search_inverted(query_splitter[l+2])
                    if(len(result_set)==0):
                        result_set=new_set1.union(new_set2)
                    else:
                        union_set=new_set1.union(new_set2)
                        result_set.union(union_set)
                    l+=2
            
                if(query_splitter[l]==query_splitter[-1]):
                    break
            
                if(query_splitter[l+1]=='and' or query_splitter[l+1]=='AND'):
                    new_set1 = set()
                    new_set2 = set()
                    new_set1 = search_inverted(query_splitter[l])
                    new_set2 = search_inverted(query_splitter[l+2])
                    if(len(result_set)==0):
                        result_set=new_set1.intersection(new_set2)
                    else:
                        intersection_set=new_set1.intersection(new_set2)
                        result_set.intersection(intersection_set)
                    l+=2
    else:
        print('Simple Boolean Query') #SIMPLE BOOLEAN QUERIES
        result_set=search_inverted(query)
    
    if(not_flag==1): #INVERTING RESULTS FOR NOT
        all_docs=set(range(0,56))
        selected_docs=result_set
        result_set=all_docs.difference(selected_docs)                
    return result_set

    
def search_inverted(query):    #SEARCH FOR TERM IN INVERTED INDEX
    inverted_index_dict = dict()
    inverted_index_dict = inverted_index()
    stemmer = PorterStemmer() #STEM THE QUERY
    query=stemmer.stem(query)
    result_set = set()
    i=0
    for i in range(56):
        terms=inverted_index_dict[i]
        j=0
        while(j<len(terms)):
            if(terms[j][0]==query or terms[j][-1]==query):
                result_set.add(i)
                break
            j+=1       
    return result_set





















def positional_preprocessing_list(terms):
     i=0
     stemmer = PorterStemmer()
     #stop_list=[]
     #stop_list = return_stopwords()
     f1 = open("\checker.txt","w")
     while i<len(terms):
         terms[i][0]=terms[i][0].casefold() #CASEFOLDING    
         terms[i][0]=terms[i][0].replace(':','')#DATA CLEANING
         terms[i][0]=terms[i][0].replace("'",'')
         terms[i][0]=terms[i][0].replace('"','')
         
         
         if(terms[i][0].find('...')>-1): #ELIMINATING TRIPLE DOT SEPARATION
             tripdot_splitter=terms[i][0].split('...')
             terms[i][0]=tripdot_splitter[0]
             terms[i].append(tripdot_splitter[1])
             
         if(terms[i][0].find('--')>-1): #ELIMINATING DOUBLE DASH SEPARATION
             doubdash_splitter=terms[i][0].split('--')
             terms[i][0]=doubdash_splitter[0]
             terms[i].append(doubdash_splitter[1])
             
         if(terms[i][0].find(']')>-1 and terms[i][0].find('[')>-1): #ELIMINATING BRACKET SEPARATION
            terms[i][0]=terms[i][0].replace('[','')
            square_splitter=terms[i][0].split(']')
            terms[i][0]=square_splitter[0]
            terms[i].append(square_splitter[1])
            
         if(terms[i][0].find('.')>-1 and terms[i][0][-1]!='.'): #ELIMINATING DOT SEPARATION
            dot_splitter=terms[i][0].split('.')
            terms[i][0]=dot_splitter[0]
            terms[i].append(dot_splitter[1])
    
         terms[i][0]=terms[i][0].replace('.','') #DATA CLEANING
         terms[i][0]=terms[i][0].replace('?','')
         terms[i][0]=terms[i][0].replace(',','')
         terms[i][0]=terms[i][0].replace('-','')
            
#            if(terms[i][0] in stop_list):
#                terms[i][0]=''
#                if(terms[i][-1]!=terms[i][0] and terms[i][-1] in stop_list):
#                    terms[i][-1]=''
                
            
         terms[i][0]=stemmer.stem(terms[i][0]) #PORTER STEMMER
         if(terms[i][-1]!=terms[i][0]):
             terms[i][-1]=stemmer.stem(terms[i][-1])


            
         if(terms[i][0] or terms[i][-1]): #WRITING MANUALLY TO FILE TO CHECK TERMS MANUALLY
             f1.write(terms[i][0])
             if(terms[i][-1]!=terms[i][0]):
                 f1.write("  ")
                 f1.write(terms[i][-1])
                 f1.write('\n')
         i+=1
    



def positional_index(): #CREATING POSITIONAL INDEX
    i=0
    dict_positional = dict()
    
    for i in range(56):
        f = open("\Trump Speechs\speech_"+str(i)+".txt","r")
        arrayy = []    
        #FILING
        for line in f:
            for word in line.split():
                arrayy+=[word.split()]
                
        positional_preprocessing_list(arrayy)
        dict_positional[i]=arrayy
        
    return dict_positional

def search_positional(query): #SEARCHING IN POSITIONAL INDEX
    print('Proximity Query')
    positional_index_dict = dict()
    positional_index_dict = positional_index()
    separator=0 #FOR QUERIES WITH NO SEPARATION BETWEEN TERMS
    query_splitter=query.split()
    if(len(query_splitter)>2): #FOR QUERIES WITH SEPARATION BETWEEN TERMS
        query_splitter[-1]=query_splitter[-1].replace('/','')
        query_splitter[-1]=int(query_splitter[-1])
        separator=query_splitter[-1]
    separator+=1
    
    stemmer = PorterStemmer() #STEMMING THE QUERY
    query_splitter[0]=stemmer.stem(query_splitter[0])
    query_splitter[1]=stemmer.stem(query_splitter[1])    
    
    result_set = set()
    i=0
    
    for i in range(56):
        terms = []
        terms=positional_index_dict[i]
        j=0
        while(j<(len(terms)-separator)): #CHECKING PROXIMITY 
            if(terms[j][0]==query_splitter[0]):
                if(terms[j+separator][0]==query_splitter[1]):
                    result_set.add(i)
                    break
            if(terms[j][-1]==query_splitter[0]):
                if(terms[j+separator]==query_splitter[1]):
                    result_set.add(i)
            j+=1       
    return result_set
    
    
def main_execution():
    query = input("Enter query: \n")
    query_splitter = query.split()
    result_set=set()
    if(len(query_splitter)==1):
        result_set=query_inverted_index(query)
    if(len(query_splitter)>1):
        if('OR' in query_splitter or 'or' in query_splitter):
            result_set=query_inverted_index(query)
        elif('AND' in query_splitter or 'and' in query_splitter):
            result_set=query_inverted_index(query)
        elif('NOT' in query_splitter or 'not' in query_splitter):
            result_set=query_inverted_index(query)
        elif('(' in query_splitter or ')' in query_splitter):
            result_set=query_inverted_index(query)
        else:
            result_set=search_positional(query)
            
    return result_set
            
        
        

        


    

