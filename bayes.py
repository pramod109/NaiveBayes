#Naive Bayes Classifier In Python
#Mishra P Hanagandi P 
#Step 1: Preprosessing 
#     1.a. - forming the vocabulary

import os
import re
#Setting up the path for training data text files:
path_stop = "C:\\Users\\pramod\\Desktop\\Data Mining\\Home Works\\HW5\\stoplist.txt"        #path for stoplist
path_test = 'C:\\Users\\pramod\\Desktop\\Data Mining\\Home Works\\HW5\\articles\\testing'
test_list = [f for f in os.listdir(path_test)]
path_train = 'C:\\Users\\pramod\\Desktop\\Data Mining\\Home Works\\HW5\\articles\\training' 
train_list = [f for f in os.listdir(path_train)]

#Going into each text file and adding each word in the list [raw_vocabulary]
#Now, the list raw_vocabulary contains ALL the words from ALL the articles in training data!

raw_vocabulary = []
for f in range (len(train_list)):
	path_article = path_train + "\\" + train_list[f]
	texts_article = [f for f in os.listdir(path_article)]
	for f in range (len(texts_article)):
		path_text = path_article + "\\" +texts_article[f]
		with open(path_text) as h:
			words = h.read().split()
			raw_vocabulary = raw_vocabulary + words
		h.close()
		path_text = ""
	texts_article = []
	path_article = ""

#converting to lowercase
lower_vocab=[]
for f in raw_vocabulary:
        a = f.lower()
        lower_vocab.append(a)
        a=""

#removing special characters
sp_vocab=[]
for f in range(len(lower_vocab)):
        a = re.sub(r'[^a-zA-Z0-9 ]',r'',lower_vocab[f])
        sp_vocab.append(a)
        a = ""

#Deleting all the duplicate elements from the list [raw_vocabulary]
unique_vocab = list(set(sp_vocab))

#removing stop words
with open(path_stop) as i:
        stop_words = i.read().split()
i.close()
stop_words = stop_words + ["~","`","!","@","#","$","%","^","&","*","(",")","_","-","=","+","{","}","[","]",";",":","<",">",",",".","?","/"]
for f in range (len(stop_words)):
        if stop_words[f] in unique_vocab:
                unique_vocab.remove(stop_words[f])

#Removing blank spaces
unique_vocab = list(filter(None,unique_vocab))

#Finally sorting according to alphabet
unique_vocab.sort()

#removing digits
bag = [item for item in unique_vocab if not item.isdigit()]
print("Pre-processing Step A is done!\nNumber of words in the bag are : "+str(len(bag)))


#*********************************************************************************************************************************||

#Preprosessing step B - Creating Features for each article >>

uni_voc = []
sp_voc = []
f_list = []
train_feature = []
for a in range(len(train_list)):
        path_article = path_train+"\\"+train_list[a]
        texts_article = [f for f in os.listdir(path_article)]
        for b in range (len(texts_article)):
                path_text = path_article+"\\"+texts_article[b]
                with open(path_text) as c:
                        words = c.read().lower().split()
                        for d in range (len(words)):
                                i = re.sub(r'[^a-zA-Z0-9 ]',r'',words[d])
                                sp_voc.append(i)
                                i = ""
                                uni_voc = list(set(sp_voc))
                        for e in range (len(bag)):
                                if bag[e] in uni_voc:
                                        f_list.append("1")
                                else:
                                        f_list.append("0")
                        if (train_list[a] == 'arxiv'):
                                f_list.append("A")
                        if (train_list[a] == 'plos'):
                                f_list.append("P")
                        if (train_list[a] == 'jdm'):
                                f_list.append("J")
                c.close()
                train_feature.append(f_list)
                f_list = []
                uni_voc = []
                sp_voc = []
                path_text = ""
        texts_article = []
        path_article = []
print("Pre-processing Step B is done!\nSize of the feature vector is : "+str(len(train_feature[0])))
        
#***********************************************************************************************************************************||
# Classification STEP B                        

test_feature = []
for a in range(len(test_list)):
        path_article = path_test+"\\"+test_list[a]
        texts_article = [f for f in os.listdir(path_article)]
        for b in range (len(texts_article)):
                path_text = path_article+"\\"+texts_article[b]
                with open(path_text,encoding="Latin-1") as c: #************************** Used the "Latin-1" encoding
                        words = c.read().lower().split()
                        for d in range (len(words)):
                                i = re.sub(r'[^a-zA-Z0-9 ]',r'',words[d])
                                sp_voc.append(i)
                                i = ""
                                uni_voc = list(set(sp_voc))
                        for e in range (len(bag)):
                                if bag[e] in uni_voc:
                                        f_list.append("1")
                                else:
                                        f_list.append("0")
                c.close()
                        
                test_feature.append(f_list)
                f_list = []
                uni_voc = []
                sp_voc = []
                path_text = ""
        texts_article = []
        path_article = []
print("Testing data is imported into a vector...\nClassification Step begins now!")

#***************************************************************************************************************************************||

#Classification Step A
countA=0
countJ=0
countP=0
PofA=0.0
PofJ=0.0
PofP=0.0
multA=1.0
multJ=1.0
multP=1.0
probA=0.33
probJ=0.33
probP=0.33
a=0

for i in range(450):
        for j in range (17402):
                a = test_feature[i][j]
                for f in range(0,150):
                        if (train_feature[f][j] == a):
                                countA = countA + 1
                for f in range(150,300):
                        if (train_feature[f][j] == a):
                                countJ = countJ + 1
                for f in range(300,450):
                        if (train_feature[f][j] == a):
                                countP = countP + 1
                PofA = countA / 150
                PofJ = countJ / 150
                PofP = countP / 150
                multA = multA * PofA
                multJ = multJ * PofJ
                multP = multP * PofP
                countA=0
                countJ=0
                countP=0
                PofA=0.0
                PofJ=0.0
                PofP=0.0
                a=0
        val = max(multA,multJ,multP)
        if (val == multA):
                test_feature[i].append("A")
        if (val == multJ):
                test_feature[i].append("J")
        if (val == multP):
                test_feature[i].append("P")
        multA=1.0
        multJ=1.0
        multP=1.0
print("Classified data >> ")
print(test_feature[0][17402])
        
        
                
                

        
              


