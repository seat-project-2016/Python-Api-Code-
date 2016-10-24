#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
import datetime
import urllib
import urllib2
import re
import sys
import web
import random
import base64
import StringIO
import requests
import hashlib
from httplib import HTTPResponse
import sys
import os
import jwt


urls = (
    '/', 'index',
    '/register', 'register',
    '/getmystatus','GetMyStatus',
    '/login','Login'
)


#Staging Server
db = web.database(host='0.0.0.0', port=3306 , dbn='mysql' , user='root', pw='seat@123', db='seatdb')
root = "http://ec2-52-27-151-189.us-west-2.compute.amazonaws.com"

class index:
    def GET(self):
        status = {"status": "Info", "message": "This page is intentionally left blank.","statusCode":121}
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', '*')
        web.header('Content-Type', 'application/json')
        return  json.dumps(status)
    
class register:
    def OPTIONS(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Methods','*')
        web.header('Access-Control-Allow-Headers','authcode')
        return
    def GET(self):
        status = {"status": "Info", "message": "This page is intentionally left blank.","statusCode":121,"success":True}
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', '*')
        web.header('Content-Type', 'application/json')
        return  json.dumps(status)

    def POST(self):
        data = json.loads(web.data())
        print (data)
        JArray = {}
        try:
            checkNum = db.query("SELECT * from `driver` WHERE phone_number ="+str(data['phone_number']))
            if len(checkNum) <= 0:
                registered_date = datetime.datetime.now()
                payload = {
                   "phone_number":data['phone_number']
                }
                encoded = jwt.encode(payload, 'secret', algorithm='HS256')                
                driverObj = db.insert('driver',name=data['name'],phone_number=data['phone_number'],registered_date=registered_date,status=0,device_id=data['device_id'],os_type=data['os_type'],auth_code=encoded)
                foldername1 = data['name'] + "_" + data['phone_number']                
                foldername = "/var/www/html/DriverImages/"+str(foldername1)
                os.makedirs(foldername)
                for images in data['documents']:
                    images['content'] += '=' * (-len(images['content']) % 4)
                    data2 =  base64.b64decode(images['content'])
                    filename = images['name']                    
                    out = open(foldername+"/"+filename, "w+")
                    out.write(data2)
                    out.close()
                    url = "http://ec2-52-27-151-189.us-west-2.compute.amazonaws.com/DriverImages/"+foldername1+"/"+filename
                    driverdetails = db.insert('driverdetails',proofname=images['proofname'],image=url,driver_id=driverObj)                
                JArray['errorCode'] = 200
                JArray['errorMessage'] = "Thank you :) Your documents are successfully uploaded. You will receive your login details shortly upon approval."
                JArray['phone_number'] = data['phone_number']
                JArray['token'] = encoded
                web.header('Access-Control-Allow-Origin', '*')
                web.header('Access-Control-Allow-Methods','GET,PUT,POST')
                web.header('Access-Control-Allow-Headers', '*')
                web.header('Content-Type', 'application/json') 
                web.header('Cache-Control', 'no-cache') 
                web.header('Pragma', 'no-cache')  
                web.header('Cache-Control', 'no-cache')                
                return json.dumps(JArray) 
            else:
                JArray['errorCode'] = 201
                JArray['errorMessage'] = "Sorry You have already registered"
                JArray['token'] = ''
                JArray['phone_number'] = ''
                web.header('Access-Control-Allow-Origin', '*')
                web.header('Access-Control-Allow-Methods','GET,PUT,POST')
                web.header('Access-Control-Allow-Headers', '*')
                web.header('Content-Type', 'application/json') 
                web.header('Cache-Control', 'no-cache') 
                web.header('Pragma', 'no-cache')  
                web.header('Cache-Control', 'no-cache')                
                return json.dumps(JArray)               

        except Exception as e:
            print(e)
            JArray['errorCode'] = 500
            JArray['errorMessage'] = "Something Went wrong"+str(e)
            JArray['token'] = ''
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Methods','GET,PUT,POST')
            web.header('Access-Control-Allow-Headers', '*')
            web.header('Content-Type', 'application/json') 
            web.header('Cache-Control', 'no-cache') 
            web.header('Pragma', 'no-cache')  
            web.header('Cache-Control', 'no-cache')                
            return json.dumps(JArray) 

class GetMyStatus:
    def OPTIONS(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Methods','*')
        web.header('Access-Control-Allow-Headers','authcode')
        return
    def GET(self):
        status = {"status": "Info", "message": "This page is intentionally left blank.","statusCode":121,"success":True}
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', '*')
        web.header('Content-Type', 'application/json')
        return  json.dumps(status)

    def POST(self):
        data = json.loads(web.data())
        print (data)
        JArray = {}
        try:
            checkNum = db.query("SELECT * from `driver` WHERE phone_number ="+str(data['phone_number'])+" and auth_code='"+str(data['authtoken'])+"'")
            if len(checkNum) <= 0:
                JArray['errorCode'] = 201
                JArray['errorMessage'] = "Wrong AuthCode and Number!"                
                web.header('Access-Control-Allow-Origin', '*')
                web.header('Access-Control-Allow-Methods','GET,PUT,POST')
                web.header('Access-Control-Allow-Headers', '*')
                web.header('Content-Type', 'application/json') 
                web.header('Cache-Control', 'no-cache') 
                web.header('Pragma', 'no-cache')  
                web.header('Cache-Control', 'no-cache')                
                return json.dumps(JArray) 
            else:
                for cust in checkNum:
                    approvedStatus = cust.status
                    reason = cust.reason
                    statuschangeddate =cust.status_changed_date
                if int(approvedStatus) == 1:
                    JArray['errorCode'] = 200
                    JArray['status'] = 1
                    JArray['errorMessage'] = "Congrats! your documents got approved by Seat contact them for more details."
                    web.header('Access-Control-Allow-Origin', '*')
                    web.header('Access-Control-Allow-Methods','GET,PUT,POST')
                    web.header('Access-Control-Allow-Headers', '*')
                    web.header('Content-Type', 'application/json') 
                    web.header('Cache-Control', 'no-cache') 
                    web.header('Pragma', 'no-cache')  
                    web.header('Cache-Control', 'no-cache') 
                    return json.dumps(JArray)               
                elif int(approvedStatus) == 2:                    
                    JArray['errorCode'] = 200
                    JArray['status'] = 2
                    JArray['errorMessage'] = "Sorry :( your documents rejected. Please register again or contact Seat for more deatils"
                    web.header('Access-Control-Allow-Origin', '*')
                    web.header('Access-Control-Allow-Methods','GET,PUT,POST')
                    web.header('Access-Control-Allow-Headers', '*')
                    web.header('Content-Type', 'application/json') 
                    web.header('Cache-Control', 'no-cache') 
                    web.header('Pragma', 'no-cache')  
                    web.header('Cache-Control', 'no-cache')                
                    return json.dumps(JArray)  
  
                else:
                    JArray['errorCode'] = 200
                    JArray['status'] = 0
                    JArray['errorMessage'] = "Not yet approved contact Seat for more deatils"
                    web.header('Access-Control-Allow-Origin', '*')
                    web.header('Access-Control-Allow-Methods','GET,PUT,POST')
                    web.header('Access-Control-Allow-Headers', '*')
                    web.header('Content-Type', 'application/json') 
                    web.header('Cache-Control', 'no-cache') 
                    web.header('Pragma', 'no-cache')  
                    web.header('Cache-Control', 'no-cache')                
                    return json.dumps(JArray)  


        except Exception as e:
            print(e)
            JArray['errorCode'] = 500
            JArray['errorMessage'] = "Something Went wrong"+str(e)
            JArray['token'] = ''
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Methods','GET,PUT,POST')
            web.header('Access-Control-Allow-Headers', '*')
            web.header('Content-Type', 'application/json') 
            web.header('Cache-Control', 'no-cache') 
            web.header('Pragma', 'no-cache')  
            web.header('Cache-Control', 'no-cache')                
            return json.dumps(JArray) 

class Login:
    def OPTIONS(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Methods','*')
        web.header('Access-Control-Allow-Headers','authcode')
        return
    def GET(self):
        status = {"status": "Info", "message": "This page is intentionally left blank.","statusCode":121,"success":True}
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', '*')
        web.header('Content-Type', 'application/json')
        return  json.dumps(status)

    def POST(self):
        data = json.loads(web.data())
        print (data)
        JArray = {}
        try:
            checkNum = db.query("SELECT * from `driver` WHERE phone_number ="+str(data['phone_number'])+" and password='"+str(data['password'])+"'")
            if len(checkNum) <= 0:
                JArray['errorCode'] = 201
                JArray['errorMessage'] = "Wrong AuthCode and Number!"                
                web.header('Access-Control-Allow-Origin', '*')
                web.header('Access-Control-Allow-Methods','GET,PUT,POST')
                web.header('Access-Control-Allow-Headers', '*')
                web.header('Content-Type', 'application/json') 
                web.header('Cache-Control', 'no-cache') 
                web.header('Pragma', 'no-cache')  
                web.header('Cache-Control', 'no-cache')                
                return json.dumps(JArray) 
            else:
                JArray['errorCode'] = 200
                JArray['errorMessage'] = "Logged in successfully"
                web.header('Access-Control-Allow-Origin', '*')
                web.header('Access-Control-Allow-Methods','GET,PUT,POST')
                web.header('Access-Control-Allow-Headers', '*')
                web.header('Content-Type', 'application/json') 
                web.header('Cache-Control', 'no-cache') 
                web.header('Pragma', 'no-cache')  
                web.header('Cache-Control', 'no-cache') 
                return json.dumps(JArray)                               
        except Exception as e:
            print(e)
            JArray['errorCode'] = 500
            JArray['errorMessage'] = "Something Went wrong"+str(e)
            JArray['token'] = ''
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Methods','GET,PUT,POST')
            web.header('Access-Control-Allow-Headers', '*')
            web.header('Content-Type', 'application/json') 
            web.header('Cache-Control', 'no-cache') 
            web.header('Pragma', 'no-cache')  
            web.header('Cache-Control', 'no-cache')                
            return json.dumps(JArray) 



if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()                          
                    
