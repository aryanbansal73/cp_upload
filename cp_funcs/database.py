from flask import Flask, redirect, url_for, session, render_template, request,flash
import pymongo
from dotenv import load_dotenv
import os
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
def connect_db():
    db_pass =  os.getenv("db_pass")
    connection_url = f"mongodb+srv://whathwaye:{db_pass}@cluster0.gsuq52o.mongodb.net/?retryWrites=true&w=majority"
    db_name  = os.getenv("db_name1")
    client = pymongo.MongoClient(connection_url)
    # print(db_name)
    db = client[db_name]
    collection_name =  os.getenv("collection_name1")
    records = db[collection_name]
    return records

