print("Importing libraries...")

# import libraries

from bs4 import BeautifulSoup
import urllib.request
import pickle
import pandas as pd
print("Done importing.")

# insert number of documents

print("Enter number of documents to be scrapped: ", end="")
docs_num = int(input())

# scrap documents from digilib.its.ac.id

print("Scraping..")
digilib_url = 'http://digilib.its.ac.id/publisher/51100/'
paper = []
for i in range(0,docs_num,20):
    page = urllib.request.urlopen(digilib_url+str(i))
    soup = BeautifulSoup(page, 'html.parser')
    docs = soup.find_all('span', attrs={'class': 'style5'})
    link = []
    for x in docs:
        try:
            link.append(x.find('a').get('href'))
        except:
            pass
    for x in link[:20]:
        page = urllib.request.urlopen(x)
        soup = BeautifulSoup(page, 'html.parser')
        try:
            title = soup.find('h2', attrs={'class': 'isi'}).find('i').getText()
            abstract = soup.find('span', attrs={'class': 'teks'}).find('p').getText()
            paper.append([x, title, abstract])
            print(x)
        except:
            pass
print("Scraping completed.")
print("Number of papers with abstract found: " +str(len(paper))+ " papers.")

# save results to 'corpus/paper.xlsx'

print("Saving data to corpus/paper.xlsx..")
df = pd.DataFrame(paper)
df.to_excel('corpus/paper.xlsx', header=False, index=False)
print("Success.")

# save results to 'pickle/paper.pkl'

print("Saving data to pickle/paper.pkl..")
with open('pickle/paper.pkl', 'wb') as f:
    pickle.dump(paper, f)
print("Success.")