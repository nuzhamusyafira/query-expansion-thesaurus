print("Importing libraries...")

# import libraries

import string
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity 
import numpy as np
import pickle
import itertools
import pandas as pd
print("Done importing.")

# import from pickle

with open('pickle/paper.pkl', 'rb') as f:
    paper = pickle.load(f)
print("Number of papers with abstract found: " +str(len(paper))+ " papers.")
with open('pickle/processed_paper.pkl', 'rb') as f:
    processed_paper = pickle.load(f)
with open('pickle/words.pkl', 'rb') as f:
    words = pickle.load(f)
with open('pickle/thesaurus.pkl', 'rb') as f:
    thesaurus = pickle.load(f)

# testing

factory = StopWordRemoverFactory()
stopword = factory.create_stop_word_remover()
stemmer = StemmerFactory().create_stemmer()

# build tf_idf

vectorizer = TfidfVectorizer(use_idf=True)

while(True):
	print("Enter query keyword:")
	init_query = input()
	query = init_query

	# without query expansion

	print("==== Without query expansion ====")
	query = query.lower()
	remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
	query = query.translate(remove_punctuation_map)
	query = stopword.remove(query)
	query = query.split()
	query = [stemmer.stem(x) for x in query]
	print("Query used: " +' '.join(query))
	
	# process the query

	print("Processing query...")
	max_result = []
	x = [' '.join(query)]
	paper_tfidf = vectorizer.fit_transform(x + processed_paper)
	q = paper_tfidf[0]
	result = cosine_similarity(paper_tfidf, q)
	idx = np.argsort(-result,axis=0).flatten()    
	final = [[num, y[0], x] for num, y in enumerate(result) if y[0] > 0.0]
	max_result += final
	max_result = sorted(max_result, key=lambda x: x[1], reverse=True)
	set_result = set()
	new_result = []
	for item in max_result:
	    if item[0] not in set_result:
	        set_result.add(item[0])
	        new_result.append(item)
	    else:
	        pass
	print("Number of documents returned: " +str(len(new_result)-1)+ ".")
	print("Top 5 [document, scores, query]:")
	for x in new_result[1:6]:
	    print(x)

	# show top 5 results

	print("==== Top 5 results ====")
	for x in new_result[1:6]: 
	    print('Result', x[0]) 
	    print('QUERY', x[2]) 
	    print(paper[x[0]-1][1]) 
	    print(paper[x[0]-1][2][:200] + '...')
	    print()

	# save results to 'result/'

	file = []
	for x in new_result[1:]:
	    temp = []
	    temp.append('Document: ' +str(x[0]))
	    temp.append('Query: ' +x[2][0])
	    temp.append('Title: ' +paper[x[0]-1][1])
	    temp.append(paper[x[0]-1][2])
	    file.append(temp)

	print("Saving result to result/" +init_query+ "_original.xlsx..")
	df = pd.DataFrame(file)
	df.to_excel('result/' +init_query+ '_original.xlsx', header=False, index=False)
	print("Success.")

	# with query expansion

	print("==== With query expansion ====")
	query = init_query
	query = query.lower()
	remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
	query = query.translate(remove_punctuation_map)
	query = stopword.remove(query)
	query = query.split()
	query = [stemmer.stem(x) for x in query]

	# generate query expansion

	print("Generating queries..")
	product_query = []
	list_synonym = []
	for x in query:
	    if x in words:
	        list_synonym.append(thesaurus[x])
	    else:
	        name = x
	        data = { "q": name }
	        encoded_data = urllib.parse.urlencode(data).encode("utf-8")
	        content = urllib.request.urlopen("http://www.sinonimkata.com/search.php", encoded_data)
	        soup = BeautifulSoup(content, 'html.parser')
	        try:
	            synonym = soup.find('td', attrs={'width': '90%'}).find_all('a')
	            synonym = [x.getText() for x in synonym]
	            thesaurus[x] = [x] + synonym
	            list_synonym.append(thesaurus[x])
	        except:
	            list_synonym.append([x])
	qs = []
	for x in itertools.product(*list_synonym):
	    x = [stemmer.stem(y) for y in x]
	    qs.append([' '.join(x)])
	print("Queries used:")
	for x in qs:
	    print(x, end=' ')
	print()

	# process the query

	print("Processing query...")
	max_result = []
	for x in qs:
	    paper_tfidf = vectorizer.fit_transform(x + processed_paper)
	    q = paper_tfidf[0]
	    result = cosine_similarity(paper_tfidf, q)
	    idx = np.argsort(-result,axis=0).flatten()    
	    final = [[num, y[0], x] for num, y in enumerate(result) if y[0] > 0.0]
	    max_result += final
	max_result = sorted(max_result, key=lambda x: x[1], reverse=True)
	set_result = set()
	new_result = []
	for item in max_result:
	    if item[0] not in set_result:
	        set_result.add(item[0])
	        new_result.append(item)
	    else:
	        pass
	print("Number of documents returned: " +str(len(new_result)-1)+ ".")
	print("Top 5 [document, scores, query]:")
	for x in new_result[1:6]:
	    print(x)

	# show top 5 results

	print("==== Top 5 results ====")
	for x in new_result[1:6]: 
	    print('Result', x[0]) 
	    print('QUERY', x[2]) 
	    print(paper[x[0]-1][1]) 
	    print(paper[x[0]-1][2][:200] + '...')
	    print()

	# save results to 'result/'

	file = []
	for x in new_result[1:]:
	    temp = []
	    temp.append('Document: ' +str(x[0]))
	    temp.append('Query: ' +x[2][0])
	    temp.append('Title: ' +paper[x[0]-1][1])
	    temp.append(paper[x[0]-1][2])
	    file.append(temp)

	print("Saving result to result/" +init_query+ "_expansion.xlsx..")
	df = pd.DataFrame(file)
	df.to_excel('result/' +init_query+ '_expansion.xlsx', header=False, index=False)
	print("Success.")
	print("Press enter to continue", end="")
	input()
	print()
	print("==== New Query====")
	print()