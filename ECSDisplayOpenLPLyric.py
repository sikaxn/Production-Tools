# coding: utf-8
import time
import serial
import urllib.request,json
import pinyin
import subprocess

def find_true(json_obj):
    slides = json_obj['results']['slides']
    for i in slides:
        if i['selected']:
            return i['text']
    return ""

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)


def init():
    cfglst = cfgdecode()
    global pyEnabled
    pyEnabled = cfglst[3]
    ##print(cfglst)
    welcomeRun = 0
    nwstat = 1
    srstat = 1
    retryCounter = 0
    while True:
        retryCounter = retryCounter + 1
        msg = "This is " + str(retryCounter) + " try."
        ##print(msg)
        if retryCounter > 50:
            ##print("too many retry, exit now.")
            writeNewLines("Too many retry, Wait 30sec.")
            retryCounter = 0
            time.sleep(30)
        if nwstat == 1:
            nwstat = nwkConnectionInit(cfglst)
        if srstat == 1:    
            srstat = serConnectionInit(cfglst)
        if srstat == 0 and nwstat == 0:
            break
        elif srstat == 1 and nwstat == 0:
            time.sleep(1)
            ##print("serial retry\n")
        elif srstat == 0 and nwstat == 1:
            if welcomeRun == 0:
                welcomeRun = 1
                welcomeMSG()
            ##print("serial good network bad")
            out = str(retryCounter) + " Connection issue, now retry"
            writeNewLines(out)
            time.sleep(1)
            out = "IP: " + str(getIPAddr())
            writeNewLines(out)
            time.sleep(1)
            cfglst = cfgdecode()
            out = "Server IP: " + str(cfglst[0]) + " Port: " + str(cfglst[1])
            writeNewLines(out)
            ##print("network retry\n")
            time.sleep(1)
        else:
                time.sleep(1)
                ##print("all retry\n")
    time.sleep(1)
    writeNewLines("ready")
    ##print("ready\n")
    return
    
def serConnectionInit(connCfg):
    ## Read connCfg 
    global prevLine
    prevLine = ""
    ipaddr = connCfg[0]
    port = connCfg[1]
    serialRes = connCfg[2]
    ##print("Init serial")
    try:
        global ser
        ser = serial.Serial()
        ser.baudrate = 9600
        ser.port = serialRes
        ser.open()
        ser.write(b'\x0c')##clear screen
        ser.write(str("Welcome! OpenLP Lyric tool").encode("latin_1"))
        time.sleep(1)
        out = "IP: " + str(getIPAddr())
        writeNewLines(out)
        time.sleep(3)
    except:
        ##print("Serial connection issue! \n")
        cont = "{}"
        return 1
    return 0

def nwkConnectionInit(connCfg):
    ## Read connCfg 
    ipaddr = connCfg[0]
    port = connCfg[1]
    serialRes = connCfg[2]
    ##print("Init network")
    url = "http://" + ipaddr + ":" + port + "/api/controller/live/text" ## generate URL
    global req
    req = urllib.request.Request(url)
    try:
        ##print("Connecting...\n")
        read = urllib.request.urlopen(req).read()
        cont = json.loads(read.decode('utf-8'))
        ##print("Connected...\n")
    except:
        ##print("Network Connection issue! \n")
        cont = "{}"
        return 1
    return 0
    
def welcomeMSG():
    ##print("Starting Up display \n")
    time.sleep(1)
    for i in range (2):
        ser.write(b'\x0c')##clear screen
        ser.write(str(i).encode("latin_1"))
        time.sleep(1)
  
def writeNewLines(text):
    global prevLine
    ####print("previous")
    ####print(prevLine)
    if text != prevLine:
       prevLine = text 
       try:
           ##print("write to ECS\n")
           ser.write(b'\x0c')##clear screen
           ser.write(str(text).encode("latin_1"))
       except:
           ##print("Serial issue...")
           init()
    ##else:
        ##print("Same text no need to update.\n")
  
def writeScrollLines(text):
    global prevLine
    if True:
       prevLine = text 
       if prevLine == text:
           ser.write(b'\x0c')##clear screen
           ser.write(b'\x1b\x12')##Enable vert scrolling mode
       try:
           ##print("write to ECS\n")
           textList = text.split()
           ####print(textList)
           length = len(textList)
           ####print(length)
           for i in range(length):
               ser.write(str(textList[i]).encode("latin_1"))
               ser.write(str(" ").encode("latin_1"))
               time.sleep(0.05)
               currenttext = lyricFormatting(lyricGet())
               if currenttext != text:
                    break
       except:
           ##print("Serial issue...")
           init()
    ##else:
        ##print("Same text no need to update.\n")


def cfgdecode():
    ##print("Reading config files \n")
    ##cfgFile = open('ECSDisplay.cfg','r')
    with open("ECSDisplay.cfg") as fp:
        Lines = fp.readlines()
        count = -1
        lstread = ["","","",""]
        for line in Lines:
            count += 1
            lstread[count] = line.strip()
            ##print("Line{}: {}".format(count, line.strip()))
        fp.close()
        return lstread
    ##return "cgflist"

def lyricGet():
    try:
        read = urllib.request.urlopen(req).read()
        cont = json.loads(read.decode('utf-8'))
        js_string = urllib.request.urlopen(req).read()
        j_obj = json.loads(js_string)
        currentLyric = find_true(j_obj)
        ####print(currentLyric)
        return currentLyric
    except:
        init()

def lyricFormatting(inputLyric):
    try:
        needConv = inputLyric.isascii()
    except:
        needConv = False
        return "ready"
    if needConv == True:
        formattedLyric = inputLyric.replace('\n'," ") ## replace newline to space to avoic massive scrolling.
        formattedLyric = inputLyric
    if needConv == False:   
        ##print("Convert needed")
        out = str(inputLyric)
        out = out.replace('\n'," ")## replace newline to space to avoic massive scrolling.
        ##Reformatting Chinese characters
        out = out.replace("’","'")
        out = out.replace("，",",")
        out = out.replace("。",".")
        out = out.replace("（","(")
        out = out.replace("）",")")
        out = out.replace("？","?")
        out = out.replace("！","!")
        out = out.replace("¥","$")
        out = out.replace("：",":")
        out = out.replace("–","-")
        out = out.replace("”","’")
        out = out.replace("“","’")
        ##COnvert to pinyin
        global pyEnabled
        if pyEnabled == 1:
            out = pyTranslate(out)
            ##print(out)
        #remove non ascii
        out = strip_non_ascii(out)
        #finially check if ok to output/
        okToOutput = out.isascii()
        
        if okToOutput == True:
            formattedLyric = out
        else:
            formattedLyric = "Unsupported Characters."
    return formattedLyric

def lyricSend(textIn):
    length = len(textIn)
    ####print(length)
    if length < 41:
        writeNewLines(textIn)
    else:
        writeScrollLines(textIn)

def pyTranslate(textIn):
    outLL = pinyin.get(textIn , format="strip")
    ##print("get py")
    ##print(outLL)
    outStr = outLL
    return outStr

def getIPAddr():
    myIPAddr = subprocess.getoutput('hostname -I')
    return myIPAddr

while True:
    try:
        init
        while True:
            lyricSend(lyricFormatting(lyricGet()))
            time.sleep(0.3)
    except:
        print("Something went wrong")