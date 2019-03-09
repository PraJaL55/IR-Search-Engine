from flask import request
from flask import Flask
from collections import OrderedDict
import nltk
import json
from bs4 import BeautifulSoup
from pymongo import MongoClient

app = Flask(__name__)
ps = nltk.PorterStemmer()
client = MongoClient('mongodb://localhost:27017/')
db = client.IR_search_engine
with open('../WEBPAGES_RAW/bookkeeping.json') as f:
    loaded_json = json.loads(f.read())

def convert_to_json(output_list):
    output_json=OrderedDict()
    for url in output_list:
        html_page = open("../WEBPAGES_RAW/" + url, encoding="utf8")
        soup = BeautifulSoup(html_page, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()
        title = soup.find('title').get_text()
        snippet = soup.find('body').get_text().strip()[0:100]
        snippet = snippet.replace("\n"," ")
        snippet = snippet.replace("\t"," ")
        output_json[loaded_json[url]] = [title, snippet]
    return output_json


def process_single_word(search_query):
    query = ps.stem(search_query.lower())
    output_list = []
    output_json={}
    result_set = db.inverted_index.find({query: {"$exists": True}})[0]
    for key, value in result_set[query].items():
        tup = (key, value[0])
        output_list.append(tup)
    sorted_list = sorted(output_list, key=lambda tup: -tup[1])
    output_list=[]
    for i in range(10):
        output_list.append(sorted_list[i][0])
    return convert_to_json(output_list)        

def check_proximity(pos1,pos2):
    l,r=0,0
    while(l<len(pos1) and r<len(pos2)):
        if pos1[l]+2<=pos2[r] or pos2[r]+2<=pos1[l]:
            return True
        if pos1[l]<pos2[r]:
            l+=1
        else:
            r+=1
    return False


def process_multiple_word(search_query):
    tokens = [ps.stem(tk.lower()) for tk in search_query]
    tfidf_dict = {}  
    output_json={} 
    for tk in tokens:
        idf = db.idf_index.find({tk: {"$exists": True}})[0][tk]
        result_set = db.inverted_index.find({tk: {"$exists": True}})[0]
        for key, value in result_set[tk].items():
            if key not in tfidf_dict:
                tfidf_dict[key] = (value[0] * idf)
            else:
                tfidf_dict[key] += (value[0] * idf)
    result_set1 = db.inverted_index.find({tokens[0]: {"$exists": True}})[0][tokens[0]]
    result_set2 = db.inverted_index.find({tokens[1]: {"$exists": True}})[0][tokens[1]]
    for rs in result_set1:
        if rs in result_set2:
            pos1 = result_set1[rs][1::]
            pos2 = result_set2[rs][1::]
            prox = check_proximity(pos1, pos2)
            if prox:
                tfidf_dict[rs]*=1.5
    i=0  
    output_list=[]  
    for k, v in sorted(tfidf_dict.items(), key=lambda kv: kv[1], reverse=True):
        output_json[k] = loaded_json[k]
        output_list.append(k)
        i+=1
        if i>=10:
            break   
    return convert_to_json(output_list)

@app.route("/get_search_results", methods=['POST'])
def hello():
    search_query = request.data.decode("utf-8")
    tokens = search_query.split(" ")
    if(len(tokens)==1):
        res=process_single_word(tokens[0])
        return json.dumps(res)
    else:
        res=process_multiple_word(tokens)
        return json.dumps(res)