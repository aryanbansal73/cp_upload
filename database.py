from flask import Flask, redirect, url_for, session, render_template, request,flash
import pymongo
from dotenv import load_dotenv
import os
def connect_db():
    db_pass = os.getenv('db_pass')
    connection_url = f"mongodb+srv://whathwaye:{db_pass}@cluster0.gsuq52o.mongodb.net/?retryWrites=true&w=majority"
    db_pass =  os.getenv("db_pass")
    db_name  = os.getenv("db_name")

    client = pymongo.MongoClient(connection_url)
    db = client[db_name]
    collection_name = 'test1'
    records = db[collection_name]
    return records

