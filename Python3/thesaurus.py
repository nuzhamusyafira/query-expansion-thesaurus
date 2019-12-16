print("Importing libraries...")

# import libraries

from bs4 import BeautifulSoup
import urllib.request
import pickle
import pandas as pd
print("Done importing.")

# scrap from sinonimkata.com
with open('pickle/words.pkl', 'rb') as f:
    words = pickle.load(f)
print("Generating thesaurus..")
thesaurus = {}
words = list(set(words))
for x in words:
    name = x
    data = { "q": name }
    encoded_data = urllib.parse.urlencode(data).encode("utf-8")
    content = urllib.request.urlopen("http://www.sinonimkata.com/search.php", encoded_data)
    soup = BeautifulSoup(content, 'html.parser')
    try:
        synonym = soup.find('td', attrs={'width': '90%'}).find_all('a')
        synonym = [x.getText() for x in synonym]
        thesaurus[x] = [x] + synonym
    except:
        thesaurus[x] = [name]
    print("Thesaurus for '" +x+ "' done.")
print("Done generating.")

# save results to 'corpus/thesaurus.xlsx'

thesaurus_list = [[x, thesaurus[x]] for x in thesaurus]
print("Saving data to corpus/thesaurus.xlsx..")
df = pd.DataFrame(thesaurus_list)
df.to_excel('corpus/thesaurus.xlsx', header=False, index=False)
print("Success.")

# save results to 'pickle/thesaurus.pkl'

print("Saving data to pickle/thesaurus.pkl..")
with open('pickle/thesaurus.pkl', 'wb') as f:
    pickle.dump(thesaurus, f)
print("Success.")