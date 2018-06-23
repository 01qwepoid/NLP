import requests
import bs4
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords 
from textblob import TextBlob
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import string
#for performaning concordance 
from nltk.text import Text

#get the required website
url = "https://techcrunch.com/2018/05/06/technical-ignorance-is-not-leadership/"
res = requests.get(url)
soup = bs4.BeautifulSoup(res.text)

#extract text
text = ''
#get each sentence into text variable
for s in range(0,13):
	text = text +soup.select('p')[s].getText().lower()
print(text)
#use nlp
words = word_tokenize(text)
print(words)

#set of punctuations
others = {'’','”','“','—','also','one','it','got','get','but'}
useful_words = [word for word in words if word not in stopwords.words('english')]
useful_words = [word for word in useful_words if word not in others]
useful_words = [word for word in useful_words if word not in string.punctuation]

#print(string.punctuation)
unique_words = set(useful_words)
freq_dist = nltk.FreqDist(useful_words)
print(freq_dist.most_common(10))
freq_dist.plot(20)

#words used only once
hap = freq_dist.hapaxes()
print(hap)

#print long words
longwords = [w for w in useful_words if len(w)>15]
print(longwords)


#usage of a word in the given text - Concordance
textforc = Text(words)
print("Concordance :")
print(textforc.concordance('policy'))

#words which have been used in a similar context
print("Similar : ")
print(textforc.similar('policy'))

#plot the place of usage of a word in the text
textforc.dispersion_plot(["policy","implement"])

#collocations - 2 words used together often
print(textforc.collocations())



print("Total useful words : ",len(useful_words))
print("Total unique words : ",len(unique_words))

#wnl = WordNetLemmatizer()

#lem = " ".join([wnl.lemmatize(i) for i in useful_words])
#lem1 = []
#lem1.append(wnl.lemmatize(i) for i in useful_words)
#type(lem1)

#print(lem1)
	
#fqwords = [word]

#write to fil

f= open("output2.txt","w+",encoding="utf-8")
f.write("Sentences with the highest subjectivity \n")

print('Sentences with the highest subjectivity')

# # loop for each sentence
sentences = sent_tokenize(text)
for sentence in sentences:

#     # get sentiment score for sentence
     sentence_sentiment = TextBlob(sentence).sentiment
     print(sentence_sentiment)
#     # if the subjectivity(opinionated) score is greater than 0.5 then 
#     # print out the sentence with the score    
     if  sentence_sentiment.subjectivity > 0.5:

#         #print(sentence, sentence_sentiment.subjectivity)
#         #print(sentence)

        f.write(str(sentence))
        f.write(str(sentence_sentiment))

        f.write("{}\t,{}\n".format(sentence, sentence_sentiment.subjectivity))

f.close()