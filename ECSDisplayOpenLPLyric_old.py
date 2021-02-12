# coding: utf-8
def find_true(json_obj):
    slides = json_obj['results']['slides']
    for i in slides:
        if i['selected']:
            return i['text']
    return None

import time
import serial
import urllib.request,json

print("hi")

##Getting data from LP server
url="http://10.0.0.159:4316/api/controller/live/text" # OpenLP ip and req api url goes here
req = urllib.request.Request(url)
##parsing response
try:
    read = urllib.request.urlopen(req).read()
    cont = json.loads(read.decode('utf-8'))
    print("Connectiong...\n")
except:
    print("Connection issue! \n")
    cont = "{}"



ser = serial.Serial()
ser.baudrate = 9600
ser.port = '/dev/ttyUSB0'
ser.open()
ser.write(b'\x0c')##clear screen
ser.write(str("Welcome! OpenLP Lyric tool").encode("latin_1"))


for i in range (2):
    ser.write(str(i).encode("latin_1"))
    time.sleep(1)
while True:
    ser.write(b'\x0c')##clear screen
    try:
        read = urllib.request.urlopen(req).read()
        cont = json.loads(read.decode('utf-8'))
        ##print("Connectiong...\n")
        out = "Connected."
        ser.write(str(out).encode("latin_1"))
        time.sleep(1)
        lastwords = "nothinghere66666655555\n"
        while True:
            try:
                read = urllib.request.urlopen(req).read()
                cont = json.loads(read.decode('utf-8'))
               ## print("Connectiong...\n")
                js_string = urllib.request.urlopen(req).read()
                j_obj = json.loads(js_string)
                ##print(j_obj)
                out = find_true(j_obj)
               ## print("\n out\n ----------------------\n")
                ##print(out)
                out = str(out)
                out = out.replace('\n'," ")
                out = out.replace("’","'")
                ##out = out.replace("'","")

                out = out[0:40]
               ## print("\n out20\n ----------------------\n")
               ## print(out)
                ##print(lastwords)
                if out!= lastwords:
                   ## print("if in--------!!!!")
                    ser.write(b'\x0c')
                    try:
                        ser.write(str(out).encode("latin_1"))
                    except:
                        print("unknown character,check input")
                        ser.write(str("Unknown Character").encode("latin_1"))
                    lastwords = out
                time.sleep(0.1)
            except:
                print("while try failed\n")
                break
                ##out = "Connection issue"
                ##ser.write(str(out).encode("latin_1"))
    except:
        out = "Connection issue"
        ser.write(str(out).encode("latin_1"))
       
    time.sleep(1)
