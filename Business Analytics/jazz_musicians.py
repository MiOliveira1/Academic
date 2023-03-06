from bs4 import BeautifulSoup
import requests

jazz_musicians = ['Charlie_Parker',
                  'Dizzy_Gillespie',
                  'Art_Tatum',
                  'Clark_Terry',
                  'Dave_Brubeck',
                  'Thelonious_Monk',
                  'Charles_Mingus',
                  'Benny_Goodman',
                  'Count_Basie',
                  'John_Coltrane',
                  'Miles_Davis',
                  'Sun_Ra',
                  'Nina_Simone',
                  'Fats_Waller',
                  'Duke_Ellington',
                  'Louis_Armstrong']

documents = {}
# Extract the article text for each musician and place it in a dictionary
# where the key is the name of the artist and the value is one single string
# that contains the entire contents of that artist's Wikipedia page
for musician in jazz_musicians:
  r = requests.get('https://en.wikipedia.org/wiki/' + musician)
  soup = BeautifulSoup(r.content)
  main_div = soup.find('div', attrs={'class':'mw-parser-output'})
  paragraphs = main_div.find_all('p')
  paragraphs = [p.get_text() for p in paragraphs]
  documents[musician] = ''.join(paragraphs)

# Here is an example of the value for John Coltrane
print(documents['John_Coltrane'])


# Let's take the first 200 characters of Charlie Parker's page and apply
# some preprocessing techniques to them
parker = documents['Charlie_Parker'][0:200]
print(parker)

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download(['punkt', 'stopwords'])

parker_tokenized = word_tokenize(parker)
print(parker_tokenized)

eng_stopwords = set(stopwords.words('english'))
parker_wo_stopwords = [t for t in parker_tokenized if t not in eng_stopwords]
# Equivalent method using a full for loop
# parker_wo_stopwords=[]
# for t in parker_tokenized:
#   if t not in eng_stopwords:
#     parker_wo_stopwords.append(t)
print(parker_wo_stopwords)

punctuation = set('&%$()"<>.,;:?!-[]{}–``')
parker_wo_stopwords_and_punct = [t for t in parker_wo_stopwords if t not in punctuation]
print(parker_wo_stopwords_and_punct)


from nltk.stem import SnowballStemmer

stemmer = SnowballStemmer('english')
parker_wo_stopwords_and_punct_stemmed = [stemmer.stem(t) for t in parker_wo_stopwords_and_punct]
print(parker_wo_stopwords_and_punct_stemmed)

# Applying these preprocessing techniques to the whole Corpus
processed_corpus = {}
eng_stopwords = set(stopwords.words('english'))
punctuation = set('&%$()"<>.,;:?!-[]{}–')
stemmer = SnowballStemmer('english')

def process_raw_text(d):
  result = word_tokenize(d)
  result = [t for t in result if t not in eng_stopwords]
  result = [t for t in result if t not in punctuation]
  result = [stemmer.stem(t) for t in result]
  return result

for k, v in documents.items():
  processed_corpus[k] = process_raw_text(v)

unique_words = set()
for d in processed_corpus.values():
  unique_words = unique_words.union(d)

# This is the size of our vocabulary, i.e. the number of unique tokens in our Corpus
print(len(unique_words))

# Let's calculate the TFIDF for each token in each document
import math

def tf(t, d):
  return d.count(t)

def idf(t, D):
  docs_with_t = len([1 for d in D.values() if t in d])
  return math.log(len(D) / docs_with_t)

def tfidf(t, d, D):
  return tf(t, d) * idf(t, D)

tfidf_dict = {}
D = processed_corpus
for k, d in processed_corpus.items():
  tfidf_dict[k] = {}
  for t in unique_words:
    tfidf_dict[k][t] = tfidf(t, d, D)

import pandas as pd

df = pd.DataFrame(tfidf_dict)
df_t = df.transpose()

# We end up with a data frame where each line represents one document (one Wikipedia page)
# and each column is one token in the vocabulary. The cell is the TFIDF of that token
# in that document
print(df_t)

# We can now do fun stuff like seeing what are the most import tokens in the
# Duke Ellingtion page
print(df.Duke_Ellington.sort_values(ascending=False).head(20))

# We can apply the concept of cosine similarity to compare two documents and get
# a number that represents how similar they are to each other
import numpy as np

def cosine_similarity(a, b):
  dot_product = np.linalg.multi_dot([a, b])
  norm_product = np.linalg.norm(a) * np.linalg.norm(a)
  return dot_product / norm_product


# Who is the most similar artist to Duke Ellingtion?
print(df.apply(lambda x: cosine_similarity(x, df.Duke_Ellington)).sort_values(ascending=False))

# Cosine similarity can be used to create a basic search engine. We can process
# a query like "Famous jazz saxophonist born in Kansas who played bebop" in exactly
# the same way we processed the Wikipedia pages. We also calculate the TFIDF of
# each token in this new "document" and then use Cosine Similarity to search
# for the most similar document.

query = 'Famous jazz saxophonist born in Kansas who played bebop'
query_after_preproc = process_raw_text(query)
query_vector = pd.Series({t:tfidf(t, query_after_preproc, D) for t in unique_words})

print(df.apply(lambda x: cosine_similarity(x, query_vector)).sort_values(ascending=False))
