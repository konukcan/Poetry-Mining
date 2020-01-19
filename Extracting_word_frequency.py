import requests
from bs4 import BeautifulSoup
import nltk
nltk.download('stopwords')

url = 'http://www.gutenberg.org/files/6099/6099-h/6099-h.htm'

r = requests.get(url)
r.encoding = 'utf-8'
html = r.text

soup = BeautifulSoup(html, features="lxml")
text = soup.get_text()
#Enlever la préface
text_sans_préface = text[338:]
#Enlever les copyrights de fin sur la page gutenberg
text_clean = text_sans_préface[0:-370]

tokenizer = nltk.tokenize.RegexpTokenizer('\w+')
tokens = tokenizer.tokenize(text_clean)

words = [token.lower() for token in tokens]
sw = nltk.corpus.stopwords.words('french')
artifacts = ["a", "i", "où", "o","rimbaud","_", "or","h", "ni", "chants","the","of", "project","là", "1", "with", "this","work","works","any", "gutenberg","and","l", "-" "of", "to", "you", "in", "tm"]
uninteresting = ['comme', 'cette', 'si', 'plus', 'car', 'tout', 'tous', 'sans', 'leurs', 'dont', 'sous', 'puis','quand', 'très']
words_ns = []
for word in words:
    if word not in sw+artifacts+uninteresting:
                    words_ns.append(word)


freqdist = nltk.FreqDist(words_ns)
freqdist.plot(25)
