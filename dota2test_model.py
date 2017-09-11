#!flask/bin/python
from pymongo import MongoClient # Database connector
from bson.objectid import ObjectId # For ObjectId to work

client = MongoClient('localhost', 27017)    #Configure the connection to the database
db_name = 'dota2test'    #Select the database
db_mongo = client[db_name]

def insert_data_mongo(col_name, insert_data):
	try:
		db_mongo[col_name].insert(insert_data)
		return True
	except:
		return False

def find_data_mongo(col_name, search_param):
	try:
		return db_mongo[col_name].find(search_param,{'_id':0})
	except:
		return False

def count_data_mongo(col_name, search_param):
	try:
		return db_mongo[col_name].find(search_param,{'_id':0}).count()
	except:
		return 0