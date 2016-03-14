__author__ = 'Abhijit'



from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from urllib.request import urlopen
from nltk.stem.snowball import EnglishStemmer

import nltk
import re
import csv
import random

stemmer = EnglishStemmer()
percentage_of_accuracy=0
Positive_words=[]
Negative_words=[]
Positive_symbols=[]
Negative_symbols=[]

All_tweets=[]
Training_Tweets=[]
Testing_Tweets=[]
Positive_tweets=[]
Negative_tweets=[]
Neutral_tweets=[]
i=0;

# reading from the csv file to dsitribute the total number of tweets amonng positive, neutral and negative tweets
with open('dataset.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        All_tweets.append(row[5].lower())
        print(row)
        print(type(row))
        if(row[0]=='4'):
            Positive_tweets.append(row[5].lower())
        elif(row[0]=='2'):
            Neutral_tweets.append(row[5].lower())
        elif(row[0]=='0'):
            Negative_tweets.append(row[5].lower())
        i+=1
print("total number of tweets present are:")
print(i)
print("Number of positive Tweets:")
print(len(Positive_tweets))
print("Number of negative Tweets:")
print(len(Negative_tweets))
print("Number of neutral Tweets:")
print(len(Neutral_tweets))

# randomize the tweet dataset
'''
random.shuffle(All_tweets)
training_data_length=0.80*float(len(All_tweets))
for i in range(int(training_data_length)):
    Training_Tweets.append(All_tweets[i])
print("lenth of the training set is :")
print(len(Training_Tweets))

for i in range(int(training_data_length)+1,len(All_tweets)):
    Testing_Tweets.append(All_tweets[i])
print("lenth of the testing set is :")
print(len(Testing_Tweets))
'''
# List of positive words
Pos_words = open('positive-words.txt', 'r+')
Pos_words=''.join(Pos_words)
#print('Numberf of positive words')
Positive_words.extend(Pos_words.split('\n',4800))
#print(len(Positive_words))

# list of negative words:
Neg_words = open('negative-words.txt', 'r+')
Neg_words=''.join(Neg_words)
#print("Number of negative words:")
Negative_words.extend(Neg_words.split('\n',4800))
#print(len(Negative_words))

# Adding positive symbols into the Positive_symbols list
Positive_symbols.extend(':)')
Positive_symbols.extend(':-)')
Positive_symbols.extend(': )')
Positive_symbols.extend(':D')
Positive_symbols.extend('=)')
Positive_symbols.extend(';-)')
Positive_symbols.extend(';)')

# Adding negative symbols into the Negative_symbols list
Negative_symbols.extend(':(')
Negative_symbols.extend(':-(')
Negative_symbols.extend(': (')
Negative_symbols.extend(':|')
Negative_symbols.extend('=(')

# first approach using the list of sentiment words, both positive and negative and emoticons
# random shuffling the dataset to get each time different 5 tweets
random.shuffle(All_tweets)
# removing the stop words from the tweet we are testing
# testing the word against the actual sense of it:
categories=[]
raw_documents=[]
documents=[]
percentage_of_accuracy+=5
categories.append("positive")
categories.append("neutral")
categories.append("negative")
all_words = []
for category in categories:
    if category=="positive":
        for i in range(len(Positive_tweets)):
            raw_documents.append((Positive_tweets[i],category))
            documents.append((word_tokenize(Positive_tweets[i]),category))
            all_words.extend(word_tokenize(Positive_tweets[i]))
    if category=="negative":
        for i in range(len(Negative_tweets)):
            raw_documents.append((Negative_tweets[i],category))
            documents.append((word_tokenize(Negative_tweets[i]),category))
            all_words.extend(word_tokenize(Negative_tweets[i]))
    if category=="neutral":
        for i in range(len(Neutral_tweets)):
            raw_documents.append((Neutral_tweets[i],category))
            documents.append((word_tokenize(Neutral_tweets[i]),category))
            all_words.extend(word_tokenize(Neutral_tweets[i]))

#random.shuffle(documents)
stop_words = set(stopwords.words('english'))
Correct_predition=0
Incorrect_prediction=0
for i in range(len(documents)):
    positive_count=0
    negative_count=0
    neutral_count=0
    All_tweets[i]
    pss=re.compile(r':\)|:-\)|: \)|:\)|:D|=\)|;-\)|;\)')
    nss=re.compile(r':\(|:-\(|:\(|:\||=\(')
    os=re.compile(r'!!!')
    if (pss.findall(raw_documents[i][0])):
        positive_count+=len(pss.findall(raw_documents[i][0]))
    if (nss.findall(raw_documents[i][0])):
        negative_count+=len(pss.findall(raw_documents[i][0]))
    #print(pss.search(All_tweets[i]))
    filtered_sentence = []
 #   print(positive_count)
  #  print(raw_documents[i][0])
   # print(negative_count)
    lemmatized_filtered_sentence=[]
    # Lemmatizing each word in the filtered list after removing the stop words
    lemmatizer= WordNetLemmatizer()
    for j in range(len(documents[i][0])):
        lemmatized_filtered_sentence.append(stemmer.stem(documents[i][0][j]))
    print(lemmatized_filtered_sentence)
    for i in range(len(lemmatized_filtered_sentence)):
        if lemmatized_filtered_sentence[i] in Positive_words:
            positive_count+=1
        if lemmatized_filtered_sentence[i] in Negative_words:
            negative_count+=1
        if lemmatized_filtered_sentence[i] =='?':
            Correct_predition+=1
        if lemmatized_filtered_sentence[i] =='...':
            Correct_predition+=1

    if os.findall(raw_documents[i][0]):
        Correct_predition+=1

    if(positive_count>negative_count and documents[i][1]=="positive"):
        Correct_predition+=1

    elif(positive_count<negative_count and documents[i][1]=="negative"):
        Correct_predition+=1

        #or (positive_count>negative_count and documents[i][1]=="negative") or (positive_count<negative_count and documents[i][1]=="positive")

    elif(positive_count==negative_count and documents[i][1]=="neutral" ):
        Correct_predition+=1
    #m2=re.compile(r'[><\'\'^@$%*_+=?;!&.*\-,/()":]|')

print("percentage of correct prediction using emoticons and set of training words is:")
percentage_of_accuracy+=(Correct_predition/len(documents))*100
print(percentage_of_accuracy)

