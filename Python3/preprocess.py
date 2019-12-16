print("Importing libraries...")

# import libraries

import string
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import pickle
import pandas as pd
print("Done importing.")

# preprocessing

with open('pickle/paper.pkl', 'rb') as f:
    paper = pickle.load(f)
print("Preprocessing..")
factory = StopWordRemoverFactory()
stopword = factory.create_stop_word_remover()
stemmer = StemmerFactory().create_stemmer()
words = []
processed_paper = []
for num,x in enumerate(paper):
    text = x[2]
    text = text.lower()
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    text = text.translate(remove_punctuation_map)
    text = stopword.remove(text)
    text = text.split()
    text = [stemmer.stem(x) for x in text]
    processed_paper.append(' '.join(text))
    text = list(set(text))
    words += text
    print("Paper " +str(num+1)+ " done.")
print("Done processing.")

# save results to 'corpus/processed_paper.xlsx'

print("Saving data to corpus/processed_paper.xlsx..")
df = pd.DataFrame(processed_paper)
df.to_excel('corpus/processed_paper.xlsx', header=False, index=False)
print("Success.")

# save results to 'pickle/processed_paper.pkl'

print("Saving data to pickle/processed_paper.pkl..")
with open('pickle/processed_paper.pkl', 'wb') as f:
    pickle.dump(processed_paper, f)
print("Success.")

# save words to 'corpus/words.xlsx'

print("Saving data to corpus/words.xlsx..")
df = pd.DataFrame(words)
df.to_excel('corpus/words.xlsx', header=False, index=False)
print("Success.")

# save words to 'pickle/words.pkl'

print("Saving data to pickle/words.pkl..")
with open('pickle/words.pkl', 'wb') as f:
    pickle.dump(words, f)
print("Success.")