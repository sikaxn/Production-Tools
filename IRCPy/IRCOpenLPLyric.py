# coding: utf-8
import time
import urllib.request,json

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
    global defNone
    defNone = cfglst[4]
    print(cfglst)
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
    
  

def cfgdecode():
    ##print("Reading config files \n")
    ##cfgFile = open('ECSDisplay.cfg','r')
    with open("ECSDisplay.cfg") as fp:
        Lines = fp.readlines()
        count = -1
        lstread = ["","","","",""]
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


def lyricSend(textIn):
    length = len(textIn)
    ####print(length)
	writeNewLines(textIn)




while True:
    try:
        init()
        while True:
            lyricSend(lyricFormatting(lyricGet()))
            time.sleep(0.3)
    except:
       print("Something went wrong")
       exit()