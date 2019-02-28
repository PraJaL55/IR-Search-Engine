from pymongo import MongoClient
import nltk
import json
import time
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

# use this the first time
# nltk.download("stopwords")

# connect to mongoDB database
client = MongoClient('mongodb://localhost:27017/')
db = client.IR_search_engine

# Use nltk porter stemmer
ps = nltk.PorterStemmer()
tokenizer = RegexpTokenizer('[a-zA-Z0-9]+')

# Give weights to important tags in term frequency
heading_tags = {'h1': 6, 'h2': 5, 'h3': 4, 'h4': 3, 'h5': 2, 'h6': 1, 'b': 6, 'em': 4, 'i': 3}

# Root corpus directory
corpus = "WEBPAGES_RAW"


# Expected dictionary
# tokens = {
#     "informatics": {
#         "3/78": [5, 6, 96, 43, 122],
#         "5/8": [8, 5, 88, 145]
#     },
#     "computer": {
#         "6/2": [5, 6, 96, 43, 122],
#         "89/7": [8, 5, 88, 145]
#     },
#     "toy": {
#         "6/2": [5, 6, 96, 43, 122],
#         "89/7": [8, 5, 88, 145]
#     }
# }


# Parse all files in bookkeeping.json and build inverted index
def create_index():
    with open(corpus + '/bookkeeping.json') as f:
        loaded_json = json.loads(f.read())
    num_of_docs_parsed = 1
    tokens_holder = {}
    stop_words = set(stopwords.words('english'))
    for x in loaded_json:
        print("Indexing file: " + x)
        html_page = open(corpus + "/" + x, encoding="utf8")
        soup = BeautifulSoup(html_page, 'html.parser')
        if soup.find('html') is None and soup.find('body') is None and soup.find('title') is None:
            continue
        for script in soup(["script", "style"]):
            script.extract()
        tokens = tokenizer.tokenize(soup.get_text(separator=' ').lower())

        # Remove stop words
        for j in range(len(tokens)):
            if tokens[j] in stop_words or tokens[j].isdigit():
                continue
            if tokens[j] not in tokens_holder:
                tokens_holder[tokens[j]] = {}
                tokens_holder[tokens[j]][x] = [1, j]
            else:
                if x in tokens_holder[tokens[j]]:
                    tokens_holder[tokens[j]][x][0] += 1
                    tokens_holder[tokens[j]][x].append(j)
                else:
                    tokens_holder[tokens[j]][x] = [1, j]

        # Give extra weight to important tags
        for k, v in heading_tags.items():
            tag = soup.find_all(k)
            for content in tag:
                important_tokens = tokenizer.tokenize(content.get_text(separator=' ').lower())
                for it in important_tokens:
                    if it in tokens_holder:
                        tokens_holder[it][x][0] += v

        # Batch write to mongoDB every 15 files
        if num_of_docs_parsed % 15 == 0:
            batch_write(tokens_holder)
            tokens_holder = {}
        num_of_docs_parsed += 1


# Batch write dictionary to MongoDB database
def batch_write(tokens_holder):
    for key, value in tokens_holder.items():
        result = db.inverted_index.find_one({key: {"$exists": True}})
        if result:
            updated_value = {**result[key], **value}
            db.inverted_index.update_one({"_id": result["_id"]}, {"$set": {key: updated_value}})
        else:
            db.inverted_index.insert_one({key: value})


start_time = time.time()

# Build the inverted index
create_index()

time_elapsed = time.time() - start_time
print("Index creation took: " + str(time_elapsed))
