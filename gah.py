import time
import sys
import os

def gahwrite(txt):
	GAH = open("tobmalf.chatlog","a")
	GAH.write("["+str(int(time.time()))+"]"+txt+"\n")
	GAH.close()

for i in open(sys.argv[1], "r").readlines():
	gahwrite("<<< receive << "+i[0:i.find(' ')]+" < "+i[i.find(' '):-1]+"\n")


