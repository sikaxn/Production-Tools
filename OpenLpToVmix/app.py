from flask import Flask, request, render_template
from os import listdir
import os
from datetime import date
import re
app = Flask(__name__)



import urllib.request,json

def nwkConnectionInit():
    

   # #print("Init network")
    url = "http://127.0.0.1:4316/api/controller/live/text"  ##Edit this to yoru OpenLP Machine IP 
    ##print(url)
    global req
    
    req = urllib.request.Request(url)
    try:
        ##print("Connecting...\n")
        read = urllib.request.urlopen(req).read()
        ##print("Connected...\n")
        return read
    except:
        ##print("Network Connection issue! \n")
        return ""
    return ""


def find_true(json_obj):
    try:
        j_obj = json.loads(json_obj)
        slides = j_obj['results']['slides']
        for i in slides:
            if i['selected']:
                return i['text']
        return ""
    except:
        return ""


def strip_ignore(textIn):
    textOut = "".join(re.split("\(|\)|\[|\]", textIn)[::2])
    return textOut

        

@app.route('/')
def mainpagesr():
   return render_template('index.html')
   
@app.route('/view')
def viewpager():
    return render_template('view.html')


@app.route('/raw')
def returnRawData():
    read = nwkConnectionInit()
    
    return read
    
    
@app.route('/sel')
def returnCurrentSelected():
    read = nwkConnectionInit()
    read = find_true(read)
    read = strip_ignore(read) ##everything in [ ] or ( ) will be ignored. comment this line if you don't want this to happen
    return read




if __name__ == '__main__':
    nwkConnectionInit()
    #app.debug = True
    app.run()