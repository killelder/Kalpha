# coding=UTF-8
import sys
sys.path.append("C:\Users\Myst\AppData\Local\Programs\Python\Python35-32\Lib\site-packages")
from gtts import gTTS
import mp3play
import select
import socket
import sys
import Queue
import string
import requests
from bs4 import BeautifulSoup
import json
import re, os
import time
from time import gmtime, strftime
import threading
sys.setrecursionlimit(2000)
#操練前喝水300 cc, 喝水
viewers = []
class VIEWER():
    def __init__(self, name, chattime, staytime, history, trigger):
        self.name = name        
        self.history = history
        self.chattime = chattime
        self.staytime = staytime
        self.trigger = trigger
    def today(self):
        if self.history == 1:
            sendmsg("歡迎再次來到老K的遊戲間" + self.name.encode("utf-8","ignore"))
            googletalk("tw", "歡迎再次來到老K的遊戲間" + self.name.encode("utf-8","ignore"))
        else:
            sendmsg("歡迎第一次來到老K的遊戲間" + self.name.encode("utf-8","ignore"))
            googletalk("tw", "歡迎第一次來到老K的遊戲間" + self.name.encode("utf-8","ignore"))
            self.history = 1
        self.trigger = 1

def googletalk(lan, msg):
    if lan == "tw":
        try:
            tts = gTTS(text=msg, lang="zh-tw")            
            tts.save("message.mp3")
        except:
            return 0
    if lan == "en":
        try:
            tts = gTTS(text=msg, lang="en")            
            tts.save("message.mp3")
        except:
            print "en error"
            return 0
    if lan == "jp":
        try:
            tts = gTTS(text=msg, lang="ja")            
            tts.save("message.mp3")
        except:
            print "en error"
            return 0
    filename = "message.mp3"
    clip = mp3play.load(filename)
    
    clip.play()
    time.sleep(min(15, clip.seconds()))
    clip.stop()
    
def scmp(f, s):
    for i in range(0, len(f)):
        if cmp(f[i:i+len(s)], s) == 0:
            return True
    return False

def Load_viewers():
    print "Loading viewers..."
    f = open("./views.csv", "r")
    for buf in f:
        buf2 = buf.replace("\n", "").split(",")
        viewers.append(VIEWER(buf2[0], int(buf2[1]), int(buf2[2]), 1, 0))
    f.close()

def Save_viewers():
    print "Saving viewers..."
    f = open("./views.csv", "w")
    for buf in viewers:
        f.write(buf.name)
        f.write(",")
        f.write(str(buf.chattime))
        f.write(",")
        f.write(str(buf.staytime))
        f.write(",")
        f.write("\n")
    f.close()

def Check_viewers(username, ct, st):
    check_value = 0
    print ct, st
    for item in viewers:
        if username == item.name and item.trigger == 1:
            check_value = 1
            item.chattime = item.chattime + ct
            item.staytime = item.staytime + st
        if username == item.name and item.trigger == 0:
            check_value = 1
            item.trigger = 1
            if ct != 0 or st != 0:
                item.today()
            item.chattime = item.chattime + ct
            item.staytime = item.staytime + st
    if check_value == 0:
        print "new user: " + username
        viewers.append(VIEWER(username, 0, 0, 0, 1))
        viewers[-1].chattime = viewers[-1].chattime + ct
        viewers[-1].staytime = viewers[-1].staytime + st
        if ct != 0 or st != 0:
            viewers[-1].today()

def Show_user(username):
    for item in viewers:
        if item.name == username:
           sendmsg(username.encode("utf-8","ignore") + "聊天次數: " + str(item.chattime).encode("utf-8","ignore") + " 在線時間數: " + str(item.staytime).encode("utf-8","ignore") + "mins")
           
def req_loop(url, count):
    try:
        res = requests.get(url)
        return res
    except:
        
        if count > 10:
            return None
        else:
            res = req_loop(url, count + 1)
            return res

def Scan_userlist(recordtime):
    #Check user list 
    #http://tmi.twitch.tv/group/user/xxxxx/chatters
    res = req_loop("http://tmi.twitch.tv/group/user/xxxxx/chatters", 0)
    
    if res != None:
        soup = BeautifulSoup(res.text.encode("utf-8", "ignore"))
        if scmp(soup.text, "chatters"):
            newDictionary=json.loads(str(soup))
            for buf in newDictionary["chatters"]["viewers"]:
                Check_viewers(buf, 0, recordtime)
            for buf in newDictionary["chatters"]["moderators"]:
                Check_viewers(buf, 0, recordtime)
            print "Scan Success"
def AD_SHOW(number):
    if number == 1:
        sendmsg("老k的youtube頻道: https://www.youtube.com/user/killelder")
        sendmsg("卡關?不會玩小遊戲, 老K手把手教你玩:http://ppt.cc/ZoMve , 這麼厲害的實況主還不按個追隨?訂閱?")
#---------------------------------------------------------------------
# Program parameters.

# botnick  = Default nick
# bufsize  = Input buffer size
# channel  = Default IRC channel
# port     = Default IRC port number
# server   = Default IRC server hostname
# master   = Owner of the bot
# uname    = Bot username (NOT NICK!)
# realname = Bot's real name

botnick    = "xxxxx"
bufsize    = 2048
channel    = "#xxxxx"
port       = 6667
server     = "irc.twitch.tv"
PASS = "oauth:" # your Twitch OAuth token
master     = "xxxxx"
uname      = "xxxxx"
realname   = "xxxxx"
zero = 0
#---------------------------------------------------------------------
# Set up a brief-replies dictionary.

# This is used to implement brief replies to brief commands or remarks
# such as:
#
#     VictorVortex, go away!
# or  Hello, VictorVortex

#Replies = dict()
#Replies ['die'      ] = "No, you"
#Replies ['goodbye'  ] = "I'll miss you"
#Replies ['sayonara' ] = "I'll miss you"
#Replies ['scram'    ] = "No, you"
#Replies ['shout'    ] = "NO I WON'T"
#Replies ['dance'    ] = botnick + " dances"
#Replies ['sing'     ] = "Tra la la"
#Replies ['hello'    ] = "Hi"
#Replies ['howdy'    ] = "Hi"
#Replies ['time'     ] = "It is TIME for a RHYME"
#Replies ['master'   ] = master + " is my master"
#Replies ['bacon'    ] = "Give me some, please!"
#Replies [botnick    ] = "What do you want?"
# You can add more replies, like so:
# Replies['action] = "Reply"
#---------------------------------------------------------------------
# Subroutine.

# Name:       ping
# Arguments:  None
# Purpose:    Responds to server Pings

def ping():
    global ircsock
    ircsock.send ("PONG :pingis\n")

#---------------------------------------------------------------------
# Subroutine.

# Name:       sendmsg
# Arguments:  chan = channel
#             msg  = message
# Purpose:    Responds to server Pings

# Sends a specified message to a specified channel.

def sendmsg (msg):
    global ircsock
    ircsock.send ("PRIVMSG "+ "#xxxxx" +" :"+ msg + "\n")


#---------------------------------------------------------------------
# Subroutine.

# Name:       JoinChan
# Arguments:  chan = channel
# Purpose:    Joins a channel

def JoinChan (chan):
    global ircsock
    ircsock.send ("JOIN "+ chan +"\n")



#---------------------------------------------------------------------
# Subroutine.

# Name:       recordtime
# Purpose:    remember the refresh time
# scanuser 
# saveviewers
# ad1
# ad2
recordtime = dict()
recordtime ["scanuser"] = 0
recordtime ["saveviewers"] = 0
recordtime ["ad1"] = 0
recordtime ["ad2"] = 0
gtcond = threading.Condition()
#---------------------------------------------------------------------
# Main routine.
def Main():
    global ircsock, Replies
    # Set up a couple of reply patterns
    pattern1 = '.*:(\w+)\W*%s\W*$' % (botnick)
    pattern2 = '.*:%s\W*(\w+)\W*$' % (botnick)
    #k_afk = ""

                                # Create a network socket
    ircsock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
                                # Connect to server
    ircsock.connect ((server, port))
                                # Authenticate

    ircsock.send ("PASS {}\r\n".format(PASS).encode("utf-8"))
    ircsock.send ("USER " + uname + " 2 3 " + realname + "\n")

                                # Assign nick
    ircsock.send ("NICK "+ botnick + "\n")
    # Auth to nickserv, uncomment this if needed and change password to the nickserv password
    #ircsock.send ("PRIVMSG NickServ :identify password \n")
    JoinChan (channel)          # Join channel
    Load_viewers()
    #%H:%M:%S
    Log_year = strftime("%Y", gmtime())
    Log_mon = strftime("%m", gmtime())
    Log_day = strftime("%d", gmtime())
    Log = open("./chatlog" + Log_year + "_" + Log_mon + "_" + Log_day + ".txt", "a")
    Log.write("Start time at : " + strftime("#%H:%M:%S", gmtime()) + "\n")
    
    
    Scan_userlist(0)
    
    
    recordtime ["scanuser"] = time.time()
    recordtime ["saveviewers"] = time.time()
    recordtime ["ad1"] = time.time()
    recordtime ["ad2"] = time.time()
    #recordtime ["scanuser"] = time.time()
    #recordtime ["saveviewers"] = time.time()
    #recordtime 
    
    while True:                 # Main loop
                                # Receive data from server
        
        #AutoSave per 30mins
        #time cmd
        
        if time.time() - recordtime ["saveviewers"] > 60*30:
            print "Save viewers..."
            #Save_viewers()
            thread1 = threading.Thread(target = Save_viewers)
            thread1.start()
            recordtime ["saveviewers"] = time.time()
        ircmsg = ircsock.recv (bufsize)
                                # Remove newlines
        ircmsg = ircmsg.strip ('\n\r')
        
        #Scan user > 1min
        if time.time() - recordtime ["scanuser"] > 60:
            print "Scan user..."
            #Scan_userlist(int((time.time() - recordtime ["scanuser"])/60))
            thread2 = threading.Thread(target = Scan_userlist(int((time.time() - recordtime ["scanuser"])/60)))
            thread2.start()
            recordtime ["scanuser"] = time.time()
        if time.time() - recordtime ["ad1"] > 60*27:
            print "AD SHOW"
            #AD_SHOW(1)
            thread2 = threading.Thread(target = Scan_userlist(1))
            thread2.start()
            recordtime ["ad1"] = time.time()
            
      
        #轉換大小寫  ==> 全部轉小寫
        #if (m1 != None):        # Yes
        #    word = m1.group (1) # Word found
        #    word = word.lower() # Make word lower case
        #    print word
        #                        # Print a reply
        #    if (word in Replies):
        #        sendmsg (Replies [word])
        if ircmsg.find ("PING :") != -1:
            ping()
        else:
            if scmp(ircmsg, ":xxxxx!xxxxx@xxxxx.tmi.twitch.tv JOIN #xxxxx") or scmp(ircmsg, ":xxxxx.tmi.twitch.tv 353 xxxxx = #xxxxx :xxxxx"):
                continue
            username = ircmsg.split(":")[1].split("!")[0].lower()
            if username[0:13] == "tmi.twitch.tv":
                continue
            
            message = ircmsg.split(":")[2].lower()
            Check_viewers(username, 1, 0)
            
            #print username.decode("utf-8", "ignore"), message.decode("utf-8", "ignore")
            print username + ":" + message
            Log.write(username + " : " + message)
            Log.write("\n")
            #if len(k_afk) != 0:
            #    sendmsg("老k不在哦, 老k正在" + k_afk)
            if username == "xxxxx" and message == "!exitbot":
                break
            if username == message:
                Show_user(username)
            if scmp(message, "!晚安"):
                sendmsg(username.encode("utf-8","ignore") + "晚安, 聊天室大家一起對" + username.encode("utf-8","ignore") + "說晚安哦")
            if scmp(message, "!老k"):
                sendmsg("老K: 職業:巨人族, 失智:87, 嘴砲:99, 興趣: 宣揚邪教思想, 個性: 鐵(ㄔ)漢柔(ㄙㄜˋ)情")
            if scmp(message, "!kalpha"):
                sendmsg("Kalpha: 職業:老K的mod, 年齡:0.2, 技能: 抓出所有潛水觀眾, 志向: 統治全twitch的聊天室")
            #if scmp(message, "!en"):
            #    thread3 = threading.Thread(target = googletalk("en", message.split("!en ")[1]))
            #    thread3.start()
            #    #googletalk("en", message.split("!en ")[1])
            if scmp(message, "!jp"):
                if len(message.split("!jp")) == 2:
                    thread3 = threading.Thread(target = googletalk("jp", message.split("!jp")[1]))
                    thread3.start()
                #googletalk("jp", message.split("!jp ")[1])
            if scmp(message, "!tw"):
                if len(message.split("!tw")) == 2:
                    thread3 = threading.Thread(target = googletalk("tw", message.split("!tw")[1]))
                    thread3.start()
                #googletalk("tw", message.split("!tw ")[1])
            #if scmp(message, "!番號"):
            #if username == "xxxxx" and scmp(message, "!afk"):
            #    if len(message.split("!afk")) > 1:
            #        k_afk = message.split("!afk ")[1]
    Log.close()
Main()
Save_viewers()
exit (zero)                     # Exit with success status
