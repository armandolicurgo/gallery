# Requires pymongo 3.6.0+
from pymongo import MongoClient
from datetime import datetime 
from bson.objectid import ObjectId

def connectionString():
	return "mongodb://localhost:27017/"

def connectionDatabase():
	return "test"

def connectionCollection():
	return "gallery"

def userName():
        return "Armando"

def isOwner(thisuser):
        ownersfile = open("owners.txt","r")
        owners = ownersfile.read()
        ownersfile.close()
        # users 
        return owners.find(thisuser+"\n") != -1

def dropPhotos():
	client = MongoClient(connectionString())
	database = client[connectionDatabase()]
	collection = database[connectionCollection()]
	query = {}
	cursor = collection.remove(query)
	"""try:
		for doc in cursor:
			print(doc)
	finally:
		client.close()
	"""
	client.close()


def likePhoto(objectid):
	client = MongoClient(connectionString())
	database = client[connectionDatabase()]
	collection = database[connectionCollection()]
	query = {}
	cursor = collection.update({"_id": ObjectId(objectid)}, {"$set": {"likes": 1}})
	"""try:
		for doc in cursor:
			print(doc)
	finally:
		client.close()
	"""
	client.close()

def approvePhoto(objectid):
	client = MongoClient(connectionString())
	database = client[connectionDatabase()]
	collection = database[connectionCollection()]
	query = {}
	cursor = collection.update({"_id": ObjectId(objectid)}, {"$set": {"approved": 1}})
	"""try:
		for doc in cursor:
			print(doc)
	finally:
		client.close()
	"""
	client.close()

def disapprovePhoto(objectId):
	#db.Doc.update({"_id": objectId}, {"$set": {"approved": 1}})
	client = MongoClient(connectionString())
	database = client[connectionDatabase()]
	collection = database[connectionCollection()]
	query = {}
	cursor = collection.update({"_id": objectId}, {"$set": {"approved": 0}})
	"""try:
		for doc in cursor:
			print(doc)
	finally:
		client.close()
	"""
	client.close()


def getAllPhotos():
	client = MongoClient(connectionString())
	database = client[connectionDatabase()]
	collection = database[connectionCollection()]
	query = {}
	cursor = collection.find(query)
	try:
		for doc in cursor:
			print(doc)
	finally:
		client.close()

def getAllPhotosHTML():
	client = MongoClient(connectionString())
	database = client[connectionDatabase()]
	collection = database[connectionCollection()]
	query = {}
	cursor = collection.find(query)
	try:
		for doc in cursor:
			print(doc)
			print(doc['filename'])
			print(doc['user'])
			print(doc['likes'])
			print(doc['approved'])
			print(doc['date'])			
	finally:
		client.close()


def getAllApprovedPhotos():
	client = MongoClient(connectionString())
	database = client[connectionDatabase()]
	collection = database[connectionCollection()]
	query = {"approved": 1}
	cursor = collection.find(query)
	try:
		for doc in cursor:
			print(doc)
	finally:
		client.close()


def insertPhoto(query):
	client = MongoClient(connectionString())
	database = client[connectionDatabase()]
	collection = database[connectionCollection()]
	oid = collection.insert_one(query).inserted_id
	#print(dir(oid))
	"""
	try:
		for doc in cursor:
			print(doc)
	finally:
		client.close()
	"""
	client.close()
	return oid 



"""
dropPhotos()
getAllPhotos()
objid=insertPhoto({"user":"Armando","approved": 0,"likes": 0,"filename":"teste3.jpg","date": datetime.now()})
getAllPhotos()
likePhoto(objid)
approvePhoto(objid)
getAllPhotos()
disapprovePhoto(objid)
getAllPhotos()
print("approved")
getAllApprovedPhotos()
getAllPhotos()

likePhoto("5b51f27370d9be1574b5ed46")
approvePhoto("5b51f27370d9be1574b5ed46")
print(userName(),isOwner(userName()))
print("Elza",isOwner("Elza"))

getAllPhotos()


"""

dropPhotos()

