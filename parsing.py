import re
import nltk,json
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

ps = nltk.PorterStemmer()
tokenizer = RegexpTokenizer('[a-zA-Z0-9]+')
heading_tags = {'h1':6,'h2':5,'h3':4,'h4':3,'h5':2,'h6':1,'b':6,'em':4,'i':3}
def create_index():
    with open('WEBPAGES_RAW/bookkeeping.json') as f:
        loaded_json = json.loads(f.read())
    i=1
    dict={}
    stop_words=set(stopwords.words('english'))
    for x in loaded_json:
        html_page = open("WEBPAGES_RAW/"+x)
        soup = BeautifulSoup(html_page, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()    
        tokens = tokenizer.tokenize(soup.get_text(separator=' ').lower())
        for j in range(len(tokens)):
            if tokens[j] in stop_words:
                continue
            if tokens[j] not in dict:
                dict[tokens[j]]={}
                dict[tokens[j]][x]=[1,j]
            else:
                if x in dict[tokens[j]]:
                    dict[tokens[j]][x][0]+=1
                    dict[tokens[j]][x].append(j)
                else:
                    dict[tokens[j]][x]=[1,j]
        print(dict)
        print('\n')
        for k,v in heading_tags.items():
            tag=soup.find_all(k)
            for content in tag:
                important_tokens = tokenizer.tokenize(content.get_text(separator=' ').lower())
                for it in important_tokens:
                    if it in dict:
                        dict[it][x][0]+=v
        print(dict)
        print('\n')
            
        if i%5==0:
            #call prajal's fn
            dict={}
            break
        i+=1
create_index()

