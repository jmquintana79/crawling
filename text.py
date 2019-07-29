# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
import requests
import nltk
import string
from collections import Counter
from nltk import pos_tag
from nltk.corpus import stopwords

'''
--------------------------------ROUTINES-------------------------------------
'''

'''
Takes a url as an argument and uses the Requests library to save the webpage.
Uses an html parser to read the webpage and stores it within a "soup" object.
Requests Documentation: http://docs.python-requests.org/en/master/
Beautiful Soup Documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
'''


def parser(url):
    try:
        website = requests.get(url)
    except requests.exceptions.RequestException as error:
        print(error)
        return False
    soup = BeautifulSoup(website.text, "html.parser")
    for script in soup(["script", "style"]):
        script.decompose()
    text = soup.get_text()
    print(text)
    return text


'''
Uses a string translator to remove excess string punctuation from the text.
The text is then passed to the nltk tokenizer which stores each word into a list.
Tokenizer Documentation: http://www.nltk.org/api/nltk.tokenize.html
'''


def tokenizer(text):
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)
    tokens = nltk.word_tokenize(text)
    print(tokens)
    return tokens


'''
Uses the stopwords collection from the nltk corpus as a reference.
Firstly we create a copy of the collection of words. For each word within
the collection, if this word is equal to one of the stopwords,
remove this word from the copy of the collection. We then use the pos_tag from
the nltk library to map a pos tag to each word in the list. 
NLTK corpus documentation: http://www.nltk.org/book/ch02.html
NLTK Tagging documentation: http://www.nltk.org/book/ch05.html
'''


def remove_stop_words(tokens):
    filtered_words = tokens[:]
    for word in tokens:
        if word in stopwords.words('english'):
            filtered_words.remove(word)
    posTag = pos_tag(filtered_words)
    print(posTag)
    return posTag


'''
Uses Counter from the collections library to essentially create a map which has
the word as the value and the number of times this word occurs as the key. We take
the five most common words within the collection and return them. From these words
we can gather more context from the document as a whole.
Counter Documentation: https://docs.python.org/3/library/collections.html
'''


def select_keywords(corpus):
    word_count = Counter(corpus)
    top_five = word_count.most_common(5)
    for word in top_five:
        print(word)
    return top_five


'''
Uses a stemmer from the nltk library to remove excess letters from certain words.
For each word within the corpus, we create a new stemmed version, print a comparison
of the two words and then add the stemmed version to a new list which we then return.
Stemmer Documentation: http://www.nltk.org/_modules/nltk/stem/lancaster.html
'''


def stemmer(corpus):
    lstemmer = nltk.stem.LancasterStemmer()
    stemmedwords = []
    for word in corpus:
        wordstem = lstemmer.stem(word)
        print("Original word: " + word + " || Stemmed word: " + wordstem)
        stemmedwords.append(wordstem)
    return stemmedwords


'''
----------------------------------Main Program------------------------------------
Here we will be calling the functions that we have created above. The output will be
structured in a way that each step of the processing pipeline will be followed. Note
that the user must enter a valid URL for the entire pipeline to be followed. The program
will exit if a valid URL is not supplied. 
'''

url = input("Please enter your website URL: ")
print("Input and Output/HTML Parsing")
text = parser(url)
if(text == False):
    print("You must supply a valid URL!")
    exit()
#else:
#    print(text)
print("---------------------------------------------------------------------")
print("Pre Processing:")
tokens = tokenizer(text)
print("---------------------------------------------------------------------")
print("POS Tagging/Removing Stop Words:")
filteredPos = remove_stop_words(tokens)
print("---------------------------------------------------------------------")
print("Word Stemming:")
stem = stemmer(tokens)
print("---------------------------------------------------------------------")
print("Selecting Keywords:")
keywords = select_keywords(filteredPos)

