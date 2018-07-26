# -*- coding: utf-8 -*-
# Armando Licurgo - 7/19/2018
# create gallery
# 
from flask import Flask, request, render_template, send_file, make_response, redirect, session, url_for
import os
from werkzeug import secure_filename
from bson.objectid import ObjectId
from pymongo import MongoClient
from datetime import datetime 
import boto3
import botocore


# local py files
import gistfile1
import useboto


# version = 1.0  HERE



#
def connectionString():
	return "mongodb://localhost:27017/"      #   <- EDIT HERE
#def connectionString():                            
#	return "mongodb://localhost:27017/"     # ORIGINAL CODE

def connectionDatabase():
	return "test"

def connectionCollection():
	return "gallery"

def userName():
	return theusername

def cookName():
	return "fidumaegua"

def cookpack(p1,p2):
	pack = p1+":"+p2
	pack = pack.replace("@"," a ")
	return pack
def nameInCook(cc):
	try:
		c = cc.replace(" a ","@")
		aux = c.split(":")
		prnt(aux)
		return aux[0]
	except:
		return "NotLogged."

def sortorderInCook(cc):
	c = cc.replace(" a ","@")
	aux = c.split(":")
	return aux[2]
def fbidInCook(cc):
	c = cc.replace(" a ","@")
	aux = c.split(":")
	return aux[1]

#
def prnt(pp):
	thisdebug = True    #   HERE
	if thisdebug == True:
		print(pp)



def safecook(request,thecookie,defavalue):
	st = ""
	ret = request.cookies.get(thecookie)
	prnt(dir(ret))
	return ret
	#prnt("coOkie",ret)
	if type(ret) == type(st):
		return "xxxxx" + ret
	out = ""
	for one in defavalue:
		out += one
	return "yyyyy"+out

def isOwner(thisuser):
	prnt(thisuser)
	o = open("owners.txt","r")
	owners = o.read()
	o.close()
	return owners.find(thisuser+"\n") != -1

def up(pp):
	r = pp.replace("&lt;","<")
	r = r.replace("&gt;",">") 
	r = r.replace("&#34;",'"') 
	return r

def getAllPhotosHTML(istheowner,approved,  sort):
	client = MongoClient(connectionString())
	database = client[connectionDatabase()]
	collection = database[connectionCollection()]
	if sort == "date":
		query = {"approved": approved}
		cursor = collection.find(query)
	else:
		query = {"approved": approved}                
		sortthis = [ (u"likes", -1) ]
		cursor = collection.find(query, sort= sortthis)
	allphotos = ""
	try:
		for doc in cursor:
			prnt(doc)
			objectid = ObjectId(doc['_id']).__str__()
			filename=(doc['filename'])
			user=(doc['user'])
			likes=(doc['likes'])
			approved=(doc['approved'])
			date=(str(doc['date'])).split(".")[0]
			allphotos += render_template("eachphoto.html",filename=filename,user=user,likes=likes,approved=approved,date=date,objectid=objectid,istheowner=istheowner)		
	finally:
		client.close()
	return allphotos

def getAllApprovedPhotosHTML(istheowner,   sort=""):
	return getAllPhotosHTML(istheowner,1 , sort)

def approvePhoto(objectid,query = {"$set": {"approved": 1}} ):
	client = MongoClient(connectionString())
	database = client[connectionDatabase()]
	collection = database[connectionCollection()]
	cursor = collection.update({"_id": ObjectId(objectid)},query )
	client.close()

def disapprovePhoto(objectid):
	approvePhoto(objectid, {"$set": {"approved": -1}})

def dropPhotos():
	client = MongoClient(connectionString())
	database = client[connectionDatabase()]
	collection = database[connectionCollection()]
	query = {}
	cursor = collection.remove(query)
	client.close()

def serviceindex(user):
	if user=="":
		cook = safecook(request,cookName(),"NotLogged")
		theusername = nameInCook(cook)
	else:
		theusername = user
	prnt(theusername) 	
	appowner = isOwner(theusername)
	if (appowner):
		# then approve photos
		htmltext = getAllPhotosHTML(appowner,0,"date")
		return up(render_template("index.html",htmltext = htmltext, appowner=appowner, username=theusername))
	else:
		htmltext = getAllApprovedPhotosHTML(appowner,"date")
		return up(render_template("index.html",htmltext = htmltext, appowner=appowner, username=theusername))

	
def likePhoto(pobjectid):
	xlikes = 0
	client = MongoClient(connectionString())
	database = client[connectionDatabase()]
	collection = database[connectionCollection()]
	query = {"_id": ObjectId(pobjectid)}
	projection = {}
	projection["likes"] = u"$likes"
	cursor = collection.find(query,projection = projection)
	try:
		for doc in cursor:
			likesst = doc['likes']
			#prnt(likesst,"likes st")
			xlikes = int(likesst) + 1   # add this like
			break
	finally:
		pass
	cursor = collection.update({"_id": ObjectId(pobjectid)}, {"$set": {"likes": xlikes}})
	client.close()
	return "<!DOCTYPE html>"+str(xlikes)+" likes</html>"


def insertPhoto(query):
	client = MongoClient(connectionString())
	database = client[connectionDatabase()]
	collection = database[connectionCollection()]
	oid = collection.insert_one(query).inserted_id
	client.close()
	return oid 


def serviceindex2(user):
	if user=="":
		cook = safecook(request,cookName(),"NotLogged")
		theusername = nameInCook(cook)
	else:
		theusername = user
	prnt(theusername) 	
	appowner = False
	htmltext = getAllPhotosHTML(False,1,"likes")
	return up(render_template("index.html",htmltext = htmltext, appowner=appowner, username=theusername))


application = Flask(__name__)


@application.route('/')
def index():
	x = serviceindex("")
	return x

@application.route('/top')
def indextop():
	x = serviceindex2( "" )
	return x


@application.route('/approved')
def indexapproved():
	cook = safecook(request,cookName(),"NotLoged;0;")
	theusername = nameInCook(cook) 
	#prnt(theusername, cook)
	appowner = False
	htmltext = getAllApprovedPhotosHTML(appowner)
	return up(render_template("index.html",htmltext = htmltext, appowner=appowner, username=theusername))



@application.route('/upload', methods=['GET', 'POST'])
def upload_file():
	cook = safecook(request,cookName(),"NotLoged:0:")
	theusername = nameInCook(cook) 
	if request.method == 'POST':
		try:
			file = request.files['file']
			secure_name = secure_filename(file.filename)
		except:
			secure_name = ""
		if secure_name.find(".jpg")  != -1 or secure_name.find(".jpeg")  != -1:
			file.save(os.path.join('static', secure_name ))
			file.save( secure_name )
			useboto.botoupload( os.path.join('static', secure_name ), file )
			objid = insertPhoto({"user": theusername ,"approved": 0,"likes": 0,"filename": secure_name, "date": datetime.now()})
		return redirect(url_for('index'))
	return render_template("upload.html")


@application.route('/login', methods=['POST'])
def logininto():
	if request.method == 'POST':
		requesta = request.data
		prnt(requesta)
		loginn = request.form.get('uname')
		pw = request.form.get('psw')
		#prnt(loginn,pw)
		theuserdata = ( gistfile1.main(loginn,pw) )
		#prnt(theuserdata)
		if len(theuserdata) == 3:
			theuserfbid = theuserdata[1]
			theusername = loginn
		else:
			theuserfbid = "0"
			theusername = "NotLoged1"
			#theusername = loginn			
		x = serviceindex(theusername)
		resp = make_response(    x     )
		resp.set_cookie(cookName(),cookpack(theusername,theuserfbid))
		return resp


@application.route('/img/<photoid>')
def getimage(photoid):
	filename =  photoid
	#prnt(filename)
	#return send_file(filename, mimetype='image/jpg')
	useboto.botodownload("/static/" + filename)
	return application.send_static_file(photoid)

@application.route('/approve/<photoid>')
def approve(photoid):
	approvePhoto(photoid)
	return "200"

@application.route('/like/<photoid>')
def likeit(photoid):
	r = likePhoto(photoid)
	return r

@application.route('/dropphotos')
def dropphotos():
	dropPhotos()   # for debug only


@application.route('/disapprove/<photoid>')
def disapprove(photoid):
	disapprovePhoto(photoid)
	return "200"


@application.route("/set")
def setcookie(thecookie,thevalue):
	resp = make_response(    serviceindex("")     )
	resp.set_cookie(thecookie,thevalue)
	return resp


@application.route("/get/<thecookie>")
def getcookie(thecookie):
	f = safecook(request,thecookie,"indefinido")
	return ""+ f      # + "<br>Name is:" + nameInCook(f) + "<br>FBid: " + fbidInCook(f)

if __name__ == "__main__":
	#application.run(debug=True)
	application.run(host='0.0.0.0', port=80, debug=True)   # HERE

