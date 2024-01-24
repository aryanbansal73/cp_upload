from dotenv import load_dotenv
import os

import pymongo
import time

class Util:
    def __init__(self, db_name) -> None:
        # self.connection_url = "mongodb://localhost:27017/"
        self.db_pass = os.getenv('db_pass')
        self.connection_url = f"mongodb+srv://whathwaye:{self.db_pass}@cluster0.gsuq52o.mongodb.net/?retryWrites=true&w=majority"
        self.db_name = db_name
        self.client = pymongo.MongoClient(self.connection_url)
        self.db = self.client[self.db_name]
    def give_db(self ):
        client = pymongo.MongoClient(self.connection_url)
        return  client
    def close_db(self,client):
        client.close()
    def insert_doc(self, col_name, data):
        client = pymongo.MongoClient(self.connection_url)
        collection = self.db[col_name]
        collection.insert_one(data)
        client.close()
  
    def search_doc(self, col_name, dic):
        client = pymongo.MongoClient(self.connection_url)
        collection = self.db[col_name]
        data = collection.find_one(dic)
        client.close()
           # returns None if not found
        return data
    
    def search_doc_with_projection(self, col_name, dic, projection):

        collection = self.db[col_name]
        data = collection.find(dic, projection)   # returns None if not found

        return data
        
    def update_doc(self, col_name, data):
        collection = self.db[col_name]
        filter_criteria = {'_id': data['_id']}  # Assuming '_id' is the unique identifier for your document

        # Directly use the update data without nesting it under $set
        update_data = data

        collection.update_one(filter_criteria, {'$set':data} ,  upsert= False)
        
    def get_collection_names(self):
        names = self.db.list_collection_names()
        return names
        
    def get_all_data(self, col_name):
        collection = self.db[col_name]
        data = collection.find()
        list_of_docs = []
        for d in data:
            list_of_docs.append(d)
        return list_of_docs
    
    def get_projected_data(self, col_name, projection):
        collection = self.db[col_name]
        data = collection.find({}, projection)
        list_of_docs = []
        for d in data:
            list_of_docs.append(d)
        return list_of_docs
    
        
        
# obj = Util('options_data')
# t1 = time.time()
# obj.search_doc(col_name='BANKNIFTY', dic={'expiry': '2023-09-06'})
# print(time.time() - t1)
# t1 = time.time()
# obj.search_doc_with_projection(col_name='BANKNIFTY', dic={'expiry': '2023-09-06'}, projection={
#     'data.44400': 1
# })
# print(time.time() - t1)
        
