import nltk
import json
from bs4 import BeautifulSoup
from pymongo import MongoClient

ps = nltk.PorterStemmer()
client = MongoClient('mongodb://localhost:27017/')
db = client.IR_search_engine
with open('WEBPAGES_RAW/bookkeeping.json') as f:
    loaded_json = json.loads(f.read())

def process_single_word(search_query):
    query = ps.stem(search_query.lower())
    output_list = []
    result_set = db.inverted_index.find({query: {"$exists": True}})[0]
    #print(result_set)
    for key, value in result_set[query].items():
        tup = (key, value[0])
        output_list.append(tup)
    sorted_list = sorted(output_list, key=lambda tup: -tup[1])
    for i in range(10):
        print(loaded_json[sorted_list[i][0]],sorted_list[i])
        html_page = open("WEBPAGES_RAW/" + sorted_list[i][0], encoding="utf8")
        soup = BeautifulSoup(html_page, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()
        print(soup.find('title').get_text())
        snippet = soup.find('body').get_text().strip()[0:100]
        print(snippet.replace("\n"," "),"\n")

def process_multiple_word(search_query):
    tokens = [ps.stem(tk.lower()) for tk in search_query]
    tfidf_dict = {}    
    for tk in tokens:
        idf = db.idf_index.find({tk: {"$exists": True}})[0][tk]
        result_set = db.inverted_index.find({tk: {"$exists": True}})[0]
        for key, value in result_set[tk].items():
            if key not in tfidf_dict:
                tfidf_dict[key] = (value[0] * idf)
            else:
                tfidf_dict[key] += (value[0] * idf)
    i=0    
    for k, v in sorted(tfidf_dict.items(), key=lambda kv: kv[1], reverse=True):
        print(loaded_json[k],"\n")
        i+=1
        if i>=10:
            break
    #print(tfidf_dict)


while(True):
    search_query = input("Enter the query to be searched: ")
    tokens = search_query.split(" ")
    if(len(tokens)==1):
        process_single_word(tokens[0])
    else:
        process_multiple_word(tokens)