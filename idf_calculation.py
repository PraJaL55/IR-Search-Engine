from pymongo import MongoClient
import time
import math

# connect to mongoDB database
client = MongoClient('mongodb://localhost:27017/')
db = client.IR_search_engine

# Parse through all tokens and calculate idf
number_of_documents = db.inverted_index.count_documents({})

start_time = time.time()

for token in db.inverted_index.find():
    key, value = token.items()
    document_frequency = len(value[1])
    token_name = value[0]

    # calculate idf and insert
    idf = math.log10(number_of_documents/document_frequency)
    db.idf_index.insert_one({token_name: idf})

time_elapsed = time.time() - start_time
print("Idf calculation took: " + str(time_elapsed))
