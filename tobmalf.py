#!/usr/bin/env python

# here's how maybe to make it reflective and tend to use its own words
# more often without adding a lot

# when it goes to respond to any phrase it preferentially saliency-checks
# phrases that it responded to. it does not choose a response of its own
# (even if it is not made up by the markov chainer, thus sensible) in the
# case that the next few speeches collected after he said it consitute
# negative reinforcement (emotionally negative, non-sequiturs, kicks/bans
# etc). positive phrases he'll preferentially choose and neutral ones
# (or ones that have been scored < confidencethreshold times) he'll
# also choose if the only other alternative is saliency-ranking the
# entire database of things other people were replying to.

# needed changes
# - tobmalf needs to break up 'lastspch' and put what he says in
#   the channel histories and uniquephrases if it's made up (this means
#   tobmalf's existing database needs to be massaged with something
#   like the new code, to consult his chatlog and insert his own speech
#   where it belongs, then do the assessment, which will be necessarily
#   fuzzy given the timer resolution in the chatlog. but future entries
#   will be non-fuzzy)
# - tobmalf must not treat lines ending with a question mark, starting
#   with a full colon or msg'd to him specially. these must all go to
#   the same handler
# for any of this to happen
# in so doing tobmalf fakes self-awareness and reflectiveness by
# heavily analyzing responses to things he says and preferring to
# quote himself before quoting another person or using the markov chainer
# (which tobmalf does now only when stumped). since tobmalf will be
# registering upon his sensorium and memory in all the same ways, but
# also much more deeply, as every other participant of his environment,
# and since those participants constitute that environment, at this
# point tobmalf will be fundamentally embodied and self-aware
# also, since people ought to respond well to stuff the markov chainer
# makes up which is sensible, likeable, funny or topical, he'll gradually
# gain a repertoire of well-scored things to say that he made up. however,
# the list of things he said he said will initially mostly consist of
# pointers to quotes of other people. phrases will contain names of 
# people not in the channel etc will be naturally pruned by this process
# and i'm hoping quoting people directly at all will be so disturbing
# on its own that invented phrases will come to outpopulate reused ones
# in the list of unique things tobmalf has said 
# alright

# when i am done tobmalf will be fully aware of his nature as an element of
# and primary actor of interest on his environment
#
# Joel Rosdahl <joel@rosdahl.net>
# Edited by Flamoot
# Edited by John Ohno <john.ohno@gmail.com>

from dotext import dotext

#import twitter
import os
import sys

from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr

dotext("`%tobmalf is starting. aaaa")

import time
def gahwrite(txt):
  GAH = open("tobmalf.chatlog","a")
  GAH.write("["+str(int(time.time()))+"]"+txt+"\n")
  GAH.close()

gahwrite("---restart---")

import tempfile
import cPickle
import urllib
import random
import glob
import time
import sys
import os
import re

# gzipin(fn) -- gunzips a cPickle
def gzipin(fn): 
  dotext("`%[`8gunzippin a cPickle...",sameline=1)
  sys.stdout.flush()
  p = os.popen("gunzip -c '"+fn+"'")
  sys.stdout.flush()
  l = "".join(p.readlines())
  p.close()
  dotext(" `7gherkinated`%]")
  sys.stdout.flush()
  return cPickle.loads(l)


global chansums
global chansumtimes
global quotes
chansums = {} # chansums is a dictionary of lists of extractions ordered by channel
chansumtimes = {}
quotes = []
global color
color = ''


def swapcolor(x, y):
  global color
  if color==x:
    color=y
  color=x

# loadsummaries() -- loads anemic predicates
def loadsummaries():
  global chansums
  global chansumtimes
  for fn in glob.glob('tobmalf.*.summary.anemic'):
    chan = fn.split('.summary')[0]
    chan = chan.split('tobmalf.')[1]
    mysumries = gzipin(fn)
    chansums.update({chan:mysumries[0]})
    chansumtimes.update({chan:mysumries[1]})
    dotext("`![`8loaded `3"+str(len(mysumries[0]))+"`8 extractions for`! `3"+(chan.replace('#',"`!#`3").replace(".","`8.`3"))+"`!]")

# fancy new main() does the inits and such.
# TODO: try and break this up
def main():
  loadsummaries() # anemic now!
  mysumries = []
  dotext("`3[`%loading quotes`3]")
  try:
    quotes = gzipin("tobmalf.quotes")
  except:
    quotes = []
  dotext("`3[",sameline=1)
  color = '`7'
  samples = 30
  for x in range(samples):
    if quotes == []: break
    t = random.choice(quotes)
    dotext(color+t+" ",sameline=1)
    swapcolor('`%', '`7')
  dotext("`3]")
  dotext("`3[`%"+str(len(quotes))+" `7unique `%quotes `7loaded`8.`3]")
  gahwrite("["+str(len(quotes))+" unique quotes loaded.]")
  
  dotext("`![`8extraction stats`3:`!]")
  
  samples = 15
  dotext("\n`![`8loading unique entities`3.`!]")
  global allents
  try:
    allents = gzipin("tobmalf.entities.unique")
  except:
    allents = {}
  dotext("`![",sameline=1)
  color = '`8'
  for x in range(samples):
    if allents == {}: break
    t = random.choice(allents.keys())
    dotext(color+t+"`3:`!"+str(allents[t]),sameline=1)
    swapcolor('`1', '`8')
  dotext("`!]")
  dotext("`![`%"+str(len(allents))+" `8unique `3entities `8loaded`3.`!]")
  gahwrite("["+str(len(allents))+" unique entities loaded.]")
  
  dotext("\n`![`8loading unique adjectives`3.`!]")
  global alladjs
  try:
    alladjs = gzipin("tobmalf.adjectives.unique")
  except:
    alladjs = {}
  dotext("`![",sameline=1)
  color = '`8'
  for x in range(samples):
    if alladjs == {}: break
    t = random.choice(alladjs.keys())
    dotext(color+t+"`3:`!"+str(alladjs[t]),sameline=1)
    swapcolor('`1', '`8')
  dotext("`![`%"+str(len(alladjs))+" `8unique `3adjectives `8loaded`3.`!]") #use adjectives somehow
  gahwrite("["+str(len(alladjs))+" unique adjectives loaded.]")
  
  dotext("\n`![`8loading unique pxs`3.`!]")
  global allpxs
  try:
    allpxs = gzipin("tobmalf.pxs.unique")
  except:
    allpxs = {}
  dotext("`![",sameline=1)
  color = '`8'
  for x in range(samples):
    if allpxs == {}: break
    t = random.choice(allpxs.keys())
    dotext(color+t+"`3:`!"+str(allpxs[t]),sameline=1)
    swapcolor('`1', '`8')
  dotext("`!]")
  dotext("`![`%"+str(len(allpxs))+" `8unique `3pxs `8loaded`3.`!]") #use these somehow
  gahwrite("["+str(len(allpxs))+" unique pxs loaded.]")
  
  dotext("\n`![`8loading unique s-events`3.`!]")
  global allsubjes
  try:
    allsubjes = gzipin("tobmalf.subjes.unique")
  except:
    allsubjes = {}
  dotext("`![",sameline=1)
  color = '`8'
  for x in range(samples):
    if allsubjes == {}: break
    t = random.choice(allsubjes.keys())
    dotext(color,sameline=1)
    print t,
    dotext ("`3:`!"+str(allsubjes[t]),sameline=1)
    swapcolor('`1', '`8')
  dotext("`!]")
  dotext("`![`%"+str(len(allsubjes))+" `8unique `3subj_events `8loaded`3.`!]") #use these somehow
  gahwrite("["+str(len(allsubjes))+" unique subj_events loaded.]")
  
  dotext("\n`![`8loading unique vsoo's`3.`!]")
  global allvsoos
  try:
    allvsoos = gzipin("tobmalf.vsoos.unique")
  except:
    allvsoos = {}
  dotext("`![",sameline=1)
  color = '`8'
  for x in range(samples):
    if allvsoos == {}: break
    t = random.choice(allvsoos.keys())
    dotext(color,sameline=1)
    print t,
    dotext ("`3:`!"+str(allvsoos[t]),sameline=1)
    swapcolor('`1', '`8')
  dotext("`!]")
  dotext("`![`%"+str(len(allvsoos))+" `8unique `3VSOOs `8loaded`3.`!]") #use these somehow
  gahwrite("["+str(len(allvsoos))+" unique VSOOs loaded.]")
  
  dotext("\n`0[`8loading unique phrases`2.`0]")
  global uniquesays
  try:
    uniquesays = gzipin("tobmalf.patterns-unique")
  except:
    uniquesays = []
  dotext("`0[",sameline=1)
  color = '`8'
  for x in range(samples):
    if uniquesays == []: break
    t = random.choice(uniquesays)
    dotext(color+t.replace("\n",". ").strip(),sameline=1)
    swapcolor('`2', '`8')
  dotext("`0]")
  dotext("`0[`%"+str(len(uniquesays))+" `8unique `2phrases `8loaded`2.`0]")
  gahwrite("["+str(len(uniquesays))+" unique phrases loaded.]")
  
  global table
  dotext("\n`#[`8loading compressed markov table`5.`#]")
  notf = 0
  try:
    TF = open("tobmalf.markov.new","r")
  except:
    notf = 1
  if notf == 0:
    TF.close()
    table = gzipin("tobmalf.markov.new")
  else:
    dotext("`#[`8tobmalf.markov.new not found`5.`#]")
    table = {}
  
  if table != {}:
    dotext("`#[",sameline=1)
    color = '`5'
    for x in range(samples):
      t = random.choice(table.keys())
      dotext(color,sameline=1)
      print t,
      dotext ("`2/`1", sameline=1)
      print table[t],
      swapcolor('`5', '`8')
    dotext("`#]")
  dotext("`#[`%"+str(len(table))+" `8total `5markov nodes `8loaded`5.`#]") #use these somehow
  gahwrite("["+str(len(table))+" total MARKOV nodes loaded.]")
  
  global personality
  dotext("\n`9[`8loading compressed personality table`1.`9]")
  notf = 0
  try:
    TF = open("tobmalf.personality","r")
  except:
    notf = 1
  if notf == 0:
    TF.close()
    personality = gzipin("tobmalf.personality")
  else:
    dotext("`9[`8tobmalf.personality not found`1.`9]")
    personality = {}
  
  if personality != {}:
    dotext("`9[",sameline=1)
    color = '`1'
    for x in range(samples):
      t = random.choice(personality.keys())
      dotext(color,sameline=1)
      print t,
      dotext ("`9/`1", sameline=1)
      print personality[t],
      swapcolor('`1', '`8')
    dotext("`9]")
  dotext("`9[`%"+str(len(personality))+" `8total `1personality entries `8loaded`1.`9]") #use these somehow
  gahwrite("["+str(len(personality))+" total personality entries loaded.]")
  
  dotext("`![`8starting conceptnet`3.`!]")
  dotext("`![`8initializing conceptnet`3.`!]")
  
  # Configurable inits
  global botbanner 
  botbanner = "hi"
  global saydelay 
  saydelay = 300 # for flood protection -- in 1/100's of a second
  global logsize 
  logsize = 2500
  global intrusionprob 
  intrusionprob = 93
  global twitterprob
  twitterprob = 23
  global threshold 
  threshhold = 1
  
  # Don't-touch inits
  global loglines 
  loglines = []
  global logtimes
  logtimes = []
  global recentsays 
  recentsays = ["","","","","","","","","","","","","","","","","",""]
  global logidx 
  logidx = 0
  global logcycles 
  logcycles = 0
  global nick 
  nick = "" # Not the bot's nick ('nickname') -- the nick/channel being written to, for global modification (foolishly)
  global rtfaurl 
  rtfaurl = ""
  global rtfafile
  rtfafile = ""
  global rtfaflag 
  rtfaflag = ""
  global lastspkr 
  lastspkr = {"#wtf-other-wtf":""}
  global lastspch 
  lastspch = {"#wtf-other-wtf":""}
  
  global_c_wtf = ""
  
  for t in range(0,logsize):
      loglines.append(0)
      logtimes.append(0)
  
  global lastsay 
  lastsay = 0
  global rot13 
  rot13 = 0
  global links 
  links = []
  
  global lastThingBotSaid 
  lastThingBotSaid = {}
  global pssbt 
  pssbt = {}
  global whobotsaw 
  whobotsaw = {}
  global whatbotsaw 
  whatbotsaw = {}
  
  global bot 
  bot = TestBot(channelz, nickname, server, port)
  bot.start()

# main() ends here

def on_links(connection, event):
    global links

    links.append((event.arguments()[0],
                  event.arguments()[1],
                  event.arguments()[2]))

def on_endoflinks(connection, event):
    global links

    print "\n"

    m = {}
    for (to_node, from_node, desc) in links:
        if from_node != to_node:
            m[from_node] = m.get(from_node, []) + [to_node]

    if connection.get_server_name() in m:
        if len(m[connection.get_server_name()]) == 1:
            hubs = len(m) - 1
        else:
            hubs = len(m)
    else:
        hubs = 0

    bot.say(nick, "%d servers (%d leaves and %d hubs)\n" % (len(links), len(links)-hubs, hubs))

    print_tree(0, [], connection.get_server_name(), m)
    
def indent_string(level, active_levels, last):
    if level == 0:
        return ""
    s = ""
    for i in range(level-1):
        if i in active_levels:
            s = s + "| "
        else:
            s = s + "  "
    if last:
        s = s + "`-"
    else:
        s = s + "|-"
    return s

def print_tree(level, active_levels, root, map, last=0):
    bot.say (nick, indent_string(level, active_levels, last)
                     + root + "\n")
    if root in map:
        list = map[root]
        for r in list[:-1]:
            print_tree(level+1, active_levels[:]+[level], r, map)
        print_tree(level+1, active_levels[:], list[-1], map, 1)

# TODO: figure out what this actually DOES
def addtochansums(key, txt):
  global uniquesays
  global chansums
  global chansumtimes
  key = key.lower().replace('#','')
  try:
    idx = uniquesays.index(txt)
  except:
    idx = -1
  if idx == -1:
    idx = len(uniquesays)
    uniquesays.append(txt)
    dotext("`0[`8added phrase `0#`2"+str(idx)+", '"+(txt.replace("`",""))+"'`0]")
  else:
    dotext("`0[`8found phrase `0#`2"+str(idx)+", '"+(txt.replace("`",""))+"'`0]")

  if idx == 0: # hmm
    print "idx 0 (got a blank), nothin to do."
    if not chansums.has_key(key):
      chansums.update({key:[idx]})
      chansumtimes.update({key:[int(time.time())]}) # so things that expect us to always make a key don't break
    return
    
  if not chansums.has_key(key):
    chansums.update({key:[idx]})
    chansumtimes.update({key:[int(time.time())]})
  else:
    chansums[key].append(idx)
    chansumtimes[key].append(int(time.time()))

  dotext("`![`8chansums updated`!]")

class TestBot(SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channelz = channelz
        c = self.connection
        dotext("`%go go tobmalf.")
        c.add_global_handler("links", on_links)
        c.add_global_handler("endoflinks", on_endoflinks)


    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")


    def on_welcome(self, c, e):
        global global_c_wtf
        markov("the mouse is in the floral print. there is no more firmament. film at eleven, ninety three.")
        global_c_wtf = c
        for channel in self.channelz:
          c.join(channel)
          time.sleep(1)

    def rejoin(self):
        global global_c_wtf
        for channel in self.channelz:
          global_c_wtf.join(channel)
          time.sleep(1)
    
    def log(self, txt, slog=0):
        global logidx
        global loglines
        global logtimes
        global logcycles
        dotext ("`2Log `%"+str(logidx)+"`8/`7"+str(logsize)+" `8[`%"+str(time.localtime()[3]).zfill(2)+"`8:`%"+str(time.localtime()[4]).zfill(2)+"`8.`%"+str(time.localtime()[5]).zfill(2)+"`8]`7: `2"+txt)
        if slog == 1:
          return txt
        loglines[logidx] = txt
        logtimes[logidx] = int(time.time())
        logidx += 1
        if logidx >= logsize:
            logcycles += 1
            logidx = 0


    def on_privmsg(self, c, e):
        self.log("< msg "+e.source()+" "+e.arguments()[0])
        print e.arguments()
        if e.source().__contains__("ENKI"): # have flazmot in your name to
          self.do_command(e, e.arguments()[0]) # issue commands in msg O_O
        else:
          self.getmessage('',e.source(),e.arguments()[0])


    def on_pubmsg(self, c, e):
        if int(random.random() * 23523) == 5:
          dotext("`@[`8RANDOM DATAFILE DUMP`4. `8GET READY`4.`@]")
          self.writeout()
          dotext("`@[`8ALL DONE`4.`@]")
        global lastspkr
        global lastspch
        global chansums
        global chansumtimes
        global server
        self.log("< "+e.target()+" "+e.source()+" "+e.arguments()[0])
        a = e.arguments()[0].replace("\x02","").split(":", 1)
        if len(a) > 1:
          if a[0].count(" ") == 0 and (a[0].lower().count(nickname.lower()) == 0 and a[0].lower().count(nickname.lower().zfill(10)) == 0):
            aone = a[1] # strip nicknames lines are addressed to unless it's the bot's name
          else:
            aone = a[0]+":"+a[1] # ._.
        else:
          aone = a[0] #stupid
          
        if e.target().startswith('#'):
          tochan = e.target()
        else:
          tochan = server+"."+"#wtf-other-wtf" # pubmsg after all

        if len(a) > 1 and (aone.startswith("!") or irc_lower(a[0]) == irc_lower(self.connection.get_nickname().zfill(10))): #zfill(10) is the password for public commands ,_,
          self.do_command(e, aone.strip())
        else:
          self.getmessage(tochan, e.source(), aone)
        return          
          
    # TODO: break this up
    def getmessage(self, tochan, source, msg):

        global lastspkr
        global lastspch
        global chansums
        global chansumtimes
        global server
        global personality
        global recentsays
        global uniquesays
        global allents
        global alladjs
        global allpxs
        global allsubjes
        global allvsoos
        global lastThingBotSaid
        global pssbt
        global whobotsaw
        global whatbotsaw
	global color


        aone = msg # ignore this, but know aone is the msg
        invoker = nm_to_n(source)
        if tochan == "":
          # oh let's try this
          tochan = "__"+invoker
	  if invoker.find("bittwist") != -1:
	  	return 0

        if tochan != "":
          if not lastspkr.has_key((server+"."+tochan).lower().replace('#',"")):
            lastspkr.update({(server+"."+tochan).lower().replace('#',""):""})
            mylastspkr = ""
          else:
            mylastspkr = lastspkr[(server+"."+tochan).lower().replace('#',"")]
          if not lastspch.has_key((server+"."+tochan).lower().replace('#',"")):
            lastspch.update({(server+"."+tochan).lower().replace('#',""):""})
            mylastspch = ""
          else:
            mylastspch = lastspch[(server+"."+tochan).lower().replace('#',"")]
        else:
          mylastspkr = invoker
          mylastspch = aone
          
        if mylastspkr != invoker or tochan =="" or invoker.startswith("beet") or mylastspkr.startswith("beet"):
          dotext("`!new speaker on `3"+server+"`8.`3"+tochan+"`8. `!processing `3lastspch`8['`3"+(server+"."+tochan).lower().replace('#',"")+"`8']:")

          # emotional ranking of responses near the bot's last speech in channel history
          premoodadjustmentmls = mylastspch
          if pssbt.has_key((server+"."+tochan).lower().replace('#',"")):
            phrasesScoredSinceBotTalked = pssbt[(server+"."+tochan).lower().replace('#',"")]
            if phrasesScoredSinceBotTalked < 4 and phrasesScoredSinceBotTalked > -1:
              phrasesScoredSinceBotTalked += 1
              if mylastspkr == whobotsaw[(server+"."+tochan).lower().replace('#',"")] and phrasesScoredSinceBotTalked == 1:
                mylastspch = mylastspch.lstrip(whatbotsaw[(server+"."+tochan).lower().replace('#',"")])
                
              if mylastspch != "":
                mylastspchmood = 0.0
                gahwrite('(( mood score '+str(mylastspchmood)+' for "'+mylastspch+'"))')
              pssbt[(server+"."+tochan).lower().replace('#',"")] = phrasesScoredSinceBotTalked
          mylastspch = premoodadjustmentmls

          if tochan != "":
            addtochansums(server+"."+tochan,mylastspch)
            dotext ("`7"+str(len(chansums[(server+"."+tochan).lower().replace('#',"")]))+" extractions accumulated for `!"+server+"`8.`!"+tochan)
          dotext ("`5adding lines to markov table...", sameline=1)
          sys.stdout.flush()
          newmarkovlines = ""
          for hehhh in mylastspch.split("\n"):
              hehhh = hehhh.strip()
              hehhh = re.compile(r"(\.\s*){2,}", re.I).sub(". ", hehhh)
              # anything else we wanna cook irc text with
              if hehhh == "":
                continue
              newmarkovlines += "> msg me "+hehhh+"\n"
          if newmarkovlines != "":
            markov(newmarkovlines.strip())
          sys.stdout.flush()
          dotext ("`#done")
          # markov() reads lines in log() format...
          #markovlines = "> msg me "+aone.strip()
          mylastspkr = invoker
          mylastspch = aone.strip()
        else:
          if mylastspch != "" and (not mylastspch.endswith("?")) and (not mylastspch.endswith("!")) and (not mylastspch.endswith(".")) and (not mylastspch.endswith(",")) and (not mylastspch.endswith(":")) and (not mylastspch.endswith(";")):
            mylastspch += "."
          mylastspch += "\n"+aone.strip()
        if tochan != "":
          lastspkr[(server+"."+tochan).lower().replace('#',"")] = mylastspkr
          lastspch[(server+"."+tochan).lower().replace('#',"")] = mylastspch
        intrusiontries = 0
        maxintrusiontries = 5
        minintrusionsgenerated = 1 # this includes im a smart bot
        # this is a bad way to do this now, i should just find all the replies
        # to one highest-scored saliently related phrase at once instead of
        # repeatedly scoring all the phrases and finding a reply in a shuffled
        # list of channel summaries
        # tobmalf may try to respond to someone who speaks more than one line (intrusion):
        global nickname
        global intrusionprob


        # IF LOGS GET TOO BIG
        # comment here:
        gahwrite("<<< receive << "+source+" < "+(" ".join(mylastspch.split("\n")))+"\n")


        if tochan == "" or tochan == "__"+invoker or aone.count("everyone") > 0 or aone.count("everybody") > 0 or random.choice(range(intrusionprob)) == 0 or aone.count(" thanks ")>0 or aone.lower().startswith("any") or aone.lower().count(nickname.lower().replace("_","")) > 0 or (aone.lower().replace("_","").replace(nickname.lower(),"").strip() == "hi") or (aone.lower().count("hello") > 0):
          mylist = []      # important
          for achan in chansums:
            if achan != server+"."+tochan:
              mylist.append(achan)
            else:
              dotext("`3[`8skipping this channel`3]",sameline=1)
              pass

        # heh
        # if 1 == 1:
        # hrm
        #if random.choice(range(11)) == 1:


          # IF LOGS GET TOO BIG
          # uncomment here:
          # gahwrite("<<< receive << "+source+" < "+(" ".join(mylastspch.split("\n")))+"\n")


          #intrusions = []
          intrusions=[("im a smart bot",-1)]
          dotext("`![`8mylastspkr`3: `9"+mylastspkr+"`!]",sameline=1)
          if tochan != "":
            dotext("`![`8tochan`3: `9"+tochan+"`!]", sameline=1)
          else:
            dotext("`![`8msg to`3: `9"+invoker+"`!]", sameline=1)
          while len(intrusions) < minintrusionsgenerated:
            intrusiontries += 1
            if intrusiontries >= maxintrusiontries:
              dotext("\n`![`8giving up on response`!]")
              break
              # indent from here
            dotext("`![`8tryna respond to "+mylastspkr+"`!]")
            likesToSay = random.choice(xrange(7))
            if likesToSay == 1 and len(personality) > 0:
              intrusions.append((random.choice(personality.keys()),-1))
              dotext("`9[`1just likes to say `7"+intrusions[-1][0]+", mood score `%"+str(personality[intrusions[-1][0]])+"`9]") # major time saver
	      #if(random.choice(xrange(twitterprob)) == 1):
	      #  twitter.Api(username="zalgos", password="toobparts23").PostUpdate(markov(intrusions[-1][0]))
	      continue

           
            if mylastspch != "":
              random.shuffle(mylist)
              deadent = 0

              dotext("`9>`3"+mylastspch.replace("\n", " "))
              dotext("`0[`8uhh... searchin "+str(len(mylist))+" channel logs for somethin smart to say.`2.`0.]")
              correspondencecounter = 0

              dotext("`0[`%"+str(correspondencecounter)+"`8 total non-unique linguistic entities isolated`0]")
                
              dotext("`0[`8scoring`0]")
              wtfctr = 0
              scores = {}
              wtfctr = 0
              dotext ("\n`2[`8ok... scores`2]")
              woahwtfctr = 1
              highest = [-1,"",0]
              while woahwtfctr < 6:
                dotext ("`2[`8wtfctr`2:`0"+str(wtfctr)+"`2]`1",sameline=1)
                for key in scores:
                  if key[0] == wtfctr:
                    if scores[(wtfctr,key[1],key[2])] > highest[0]:
                      highest = [scores[(wtfctr,key[1],key[2])],key[1],key[2]]
                woahwtfctr = 7 # woah
              global threshold

              print "responding to '"+mylastspch+"'"

              if threshold > correspondencecounter:
                threshold == correspondencecounter - 1 # hmm
              if threshold < 1:
                threshold = 1
              if highest[0] > threshold: # threshold
                dotext ("\n`0[`8ok. going with highest-scored phrase '`1"+(highest[1].replace("\n"," "))+"`8', scored `2"+str(highest)+"`0]")
                # less intrusive full colon massaging before putting text in the phrases db ok
                # now we gotta find a reply to this
                dotext ("\n`![`9finding a reply`!]")
                random.shuffle(mylist)
                foundphrase = ""
                foundidx = -1
                for somechan in mylist:
                  somechannel = chansums[somechan]
                  idx = 0
                  while idx < len(somechannel):
                    if somechannel[idx] == highest[2]:
                      try:
                        replyseekincrement = random.choice([1,1,1,1,1,1,1,1,2,2,3])
                        foundphrase = uniquesays[somechannel[idx+replyseekincrement]]
                        foundidx = somechannel[idx+replyseekincrement]
                      except:
                        foundphrase = ""
                      break
                    idx += 1
                  if foundphrase != "":
                    break
                if foundphrase != "":
                  dotext("`![`9reply found in `3"+somechan+"`!]")
                  tttt = foundphrase.replace("\n",". ").replace(". )", ". :)").replace(". p."," . :p.").replace(". P.", ". :P.").replace(". D.",". :D.").replace(". (.",". :(.").replace(". .",". ").replace(" .", ".")
                  myintrusion = (tttt,foundidx)
                else:
                  dotext("`![`3no reply found in any channel summary, saying sought text instead`!]")
                  tttt = highest[1].replace("\n",". ").replace(". )", ". :)").replace(". p."," . :p.").replace(". P.", ". :P.").replace(". D.",". :D.").replace(". (.",". :(.").replace(". .",". ").replace(" .", ".")
                  myintrusion = (tttt, highest[2])
                intrusions.append(myintrusion)
                intrusions = list(set(intrusions)) # if use sets not lists ok
              else:
                dotext ("\n`2[`8highest phrase score `2"+str(highest[0])+" `8not high enough, bailing`2]")
                #intrusions = [] # i dunno he can say im a smart bot i guess
          if 1 == 1:
            if 1 == 1: # ha ha open up idle and get rid of these soon    
              if intrusions != []: #hm
                print intrusions
                againn = 1
                intrusions.remove(("im a smart bot", -1))
                while againn == 1:
                  if intrusions != []:
                    intrusiontuple = random.choice(intrusions)
                    intrusion = intrusiontuple[0]
                    intrusionidx = intrusiontuple[1]                    
                    againn = 0
                    if recentsays.count(intrusion) > 0:
                      dotext ("`3[`8skippin `9'`1"+intrusion.replace("\n"," ")+"`9' as i said it already`8]")
                      intrusions.remove(intrusiontuple)
                      againn = 1
                    else:
                      dotext("`8[`!ok `3ok `9ok `7intrusion `3#`%"+str(intrusionidx)+" picked `8]")
                  if intrusions == [("im a smart bot", -1)] or intrusions == []:
                    intrusion = "im a smart bot"
                    break                      
                if intrusion == "im a smart bot":
                  dotext('`#[`8new tack, markov`#]')
                  if random.choice([1,2,3]) != 3:
                    subseed = random.choice(mylastspch.replace("\n"," ").split(" "))
                    senseed = ""
                    if mylastspch.lower().count(" you") > 0 or mylastspch.lower().count(nickname.lower().replace("_","")) > 0:
                      senseed = "I"
                    elif mylastspch.lower().startswith("i "):
                      senseed = "you"
                    intrusion = ""
                    while len(intrusion) < 1:
                      intrusion += markov("",outputs=1,w1="",w2="",subjectseed=subseed,sentenceseed=senseed) # for privmsgs
                    dotext("`5[`8saying `9'`1"+intrusion+"`9'`5]")

                    recentsays.append(intrusion)
                    recentsays.pop(0) # right
                    lastThingBotSaid.update({(server+"."+tochan).lower().replace('#',""):intrusion})
                    whobotsaw.update({(server+"."+tochan).lower().replace('#',""):mylastspkr})
                    whatbotsaw.update({(server+"."+tochan).lower().replace('#',""):mylastspch})
                    pssbt.update({(server+"."+tochan).lower().replace('#',""):0})
                    if personality.has_key(intrusion):
                      pass
                    else:
                      personality.update({intrusion:0.0}) # ok that is enough on the markov side o_o
                    
                    n = random.choice(['2','1','5','2','1'])
                    os.system("sleep "+n+"s")
                    if tochan == "": # private message
                      tochan = invoker # i think i will send tochan to invoker at the start and store histories for chats
                    if intrusion.strip().startswith("//"):
                      intrusion = "http:"+intrusion.strip() # oops .-.
                      
                    if random.choice(range(1)) == 0:
                      print "SENDING TO CHANNEL "+tochan
                      if not tochan.startswith("#"):
                        pass
                        
                    self.say(re.compile(r"^\#?__").sub('',tochan), (". ".join(intrusion.split("\n"))).replace("  "," ").replace(" . ",". "))
                  else:
                    print "new tack, bailing"
                else:
                  recentsays.append(intrusion)
                  recentsays.pop(0) # right
                  lastThingBotSaid.update({(server+"."+tochan).lower().replace('#',""):intrusion})
                  whobotsaw.update({(server+"."+tochan).lower().replace('#',""):mylastspkr})
                  whatbotsaw.update({(server+"."+tochan).lower().replace('#',""):mylastspch})
                  pssbt.update({(server+"."+tochan).lower().replace('#',""):0})
                  if personality.has_key(intrusion):
                    pass
                  else:
                    personality.update({intrusion:0.0}) # ok that is enough on the markov side o_o

                  if intrusion.count(",") > 0:
                    if intrusion.split(",")[0].count(" ") == 0:
                      intrusion = intrusion.split(",",1)[1]
                  if intrusion.startswith("//"):
                    intrusion = "http:" + intrusion
                  intrusion = intrusion.replace(" //", " http://")
                  dotext("\n`![`8i am gonna say `!'`3"+intrusion+"`!', `3#`%"+str(intrusionidx)+" `8ok `!]")
                  n = random.choice(['1','1','1','5'])
                  os.system("sleep "+n+"s")

                  oldtc = ""
                  if tochan.startswith("__"): # in case of private msgs ,_,
                    oldtc = tochan
                    tochan = invoker
                    
                    
                  if random.choice(range(1)) == 0:
                    print "SENDING TO RANDOM CHANNEL "+tochan
                    if not tochan.startswith("#"):
                      pass
                        
                  self.say(re.compile(r"^\#?__").sub('',tochan), (". ".join(intrusion.split("\n"))).replace("  "," "))
                  if oldtc.startswith("__"): # to be clean ,_,
                    tochan = oldtc
                    
        pass
	# end of getmsg


    def say(self, nick, msg, type="msg"):
        global lastsay

        self.log("> msg "+nick+" "+msg)
        
        gahwrite(">>> told >> "+nick+" > "+(msg.replace("\n"," "))+"\n")

        if rot13 == 1:
            pout, pin = os.popen2("/usr/games/rot13")
            pout.write(msg)
            pout.close()
            msg = "".join(pin.readlines())
            pin.close()

        for line in msg.split("\n"):
            while int(time.time()*100) - lastsay < saydelay:
                time.sleep(.01)
            
            lastsay = int(time.time()*100)
        
            if type == "msg":
                try:
                  self.connection.privmsg(nick, line)
                except:
                  print "Error -- couldn't privmsg "+nick
            elif type == "notice":
                try:
                  self.connection.notice(nick, line)
                except:
                  print "Error -- couldn't notice "+nick


    def on_dccmsg(self, c, e):
        c.privmsg("You said: " + e.arguments()[0][:10]+" ...")


    def on_dccchat(self, c, e):
        if len(e.arguments()) != 2:
            return
        args = e.arguments()[1].split()
        if len(args) == 4:
            try:
                address = ip_numstr_to_quad(args[2])
                port = int(args[3])
            except ValueError:
                return
            self.dcc_connect(address, port)
    # TODO: break this up
    def writeout(self):
      global chansums
      global chansumtimes
      global allents
      global alladjs
      global allpxs
      global allsubjes
      global allvsoos
      global table
      global server
      global uniquesays
      global personality
      global color
      dotext("`3[`8Writing out anemic channel summaries`3]")
      for k in chansums.keys():
        myk = k
        myfn = "tobmalf."+myk+".summary.anemic"
        gzipout(myfn, [chansums[k],chansumtimes[k]])
        dotext("`![`7tobmalf."+myk+".summary.anemic written`!]")

      samples = 30
      dotext("`3[",sameline=1)
      color = '`7'
      for x in range(samples):
        if quotes == []: break
        t = random.choice(quotes)
        dotext(color+t+" ",sameline=1)
        swapcolor('`%', '`7')
      dotext("`3]")
      dotext("`3[`%"+str(len(quotes))+" `7unique `%quotes `7saved`8.`3]")
      gahwrite("["+str(len(quotes))+" unique quotes saved.]")
      gzipout("tobmalf.quotes",quotes)

      samples = 30
      dotext("`![",sameline=1)
      color = '`8'
      for x in range(samples):
        t = random.choice(allents.keys())
        dotext(color+t+"`3:`!"+str(allents[t]),sameline=1)
        swapcolor('`1', '`8')
      dotext("`!]")
      dotext("`![`%"+str(len(allents))+" `8unique `3entities `8saved`3.`!]")
      gahwrite("["+str(len(allents))+" unique entities saved.]")
      gzipout("tobmalf.entities.unique",allents)

      dotext("`![",sameline=1)
      color = '`8'
      for x in range(samples):
        t = random.choice(alladjs.keys())
        dotext(color+t+"`3:`!"+str(alladjs[t]),sameline=1)
        swapcolor('`1', '`8')
      dotext("`!]")
      dotext("`![`%"+str(len(alladjs))+" `8unique `3adjectives `8saved`3.`!]") #use adjectives somehow
      gahwrite("["+str(len(alladjs))+" unique adjectives saved.]")
      gzipout("tobmalf.adjectives.unique",alladjs)

      dotext("`![",sameline=1)
      color = '`8'
      for x in range(samples):
        t = random.choice(allpxs.keys())
        dotext(color+t+"`3:`!"+str(allpxs[t]),sameline=1)
        swapcolor('`1', '`8')
      dotext("`!]")
      dotext("`![`%"+str(len(allpxs))+" `8unique `3pxs `8saved`3.`!]") #use these somehow
      gahwrite("["+str(len(allpxs))+" unique pxs saved.]")
      gzipout("tobmalf.pxs.unique",allpxs)

      dotext("`![",sameline=1)
      color = '`8'
      for x in range(samples):
        t = random.choice(allsubjes.keys())
        dotext(color,sameline=1)
        print t,
        dotext ("`3:`!"+str(allsubjes[t]),sameline=1)
        swapcolor('`1', '`8')
      dotext("`!]")
      dotext("`![`%"+str(len(allsubjes))+" `8unique `3subj_events `8saved`3.`!]") #use these somehow
      gahwrite("["+str(len(allsubjes))+" unique subj_events saved.]")
      print "HEY HERE'S ALLSUBJES -------> "+str(type(allsubjes))
      gzipout("tobmalf.subjes.unique", allsubjes)
            
      dotext("`![",sameline=1)
      color = '`8'
      for x in range(samples):
        t = random.choice(allvsoos.keys())
        dotext(color,sameline=1)
        print t,
        dotext ("`3:`!"+str(allvsoos[t]),sameline=1)
        swapcolor('`1', '`8')
      dotext("`!]")
      dotext("`![`%"+str(len(allvsoos))+" `8unique `3VSOOs `8saved`3.`!]") #use these somehow
      gahwrite("["+str(len(allvsoos))+" unique VSOOs saved.]")
      gzipout("tobmalf.vsoos.unique",allvsoos)

      dotext("`0[",sameline=1)
      color = '`8'
      for x in range(samples):
        t = random.choice(uniquesays)
        dotext(color,sameline=1)
        print t.replace("\n",". ").strip(),
        swapcolor('`2', '`8')
      dotext("`0]")
      dotext("`0[`%"+str(len(uniquesays))+" `8unique `2phrases `8saved`2.`0]") #use these somehow
      gahwrite("["+str(len(uniquesays))+" unique phrases saved.]")
      gzipout("tobmalf.patterns-unique",uniquesays)

      dotext("`5[`8writing markov table`5]")
      gzipout("tobmalf.markov.new",table)
      dotext("`#[`7tobmalf.markov written`#]")

      dotext("`1[`8writing personality matrix`1]")
      gzipout("tobmalf.personality",personality)
      dotext("`9[`7tobmalf.personality written`9]")

    # TODO: break this up
    def do_command(self, e, cmd):
        global color
	global nick
        global rot13
        global rtfaurl
        global rtfafile
        global rtfaflag
        global lastspch
        global lastspkr
        global chansums
        global chansumtimes
        global global_c_wtf
        
        cmd = re.compile(r"^.+?: ").sub("", cmd) # get out the name if the command starts with it
                                  # NOTE THIS MAKES THE BOT NOT RESPOND WITH A NAME IF ADDRESSED WITH ITS
                                  # NAME BUT IT ALLOWS THE COMMANDS TO WORK. MAYBE SET A FLAG OR ONLY
                                  # TAKE OUT THE BOT'S NAME.ZFILL(10) INSTEAD OF .+?
        
        gahwrite("<<< addressed by << "+e.source()+" < "+cmd+"\n")
        
        dotext("`$Command received from `6"+e.source()+"`%: `6"+cmd+"")
                           
        invoker = nm_to_n(e.source())
        
        if e.target().startswith("#"):
            nick = e.target()
        else:
            nick = nm_to_n(e.source())
            
        c = self.connection

        if cmd == "XXXXXXXXXXXXX!!!!!!!!disconnect":
            self.disconnect()

        if cmd == "rejoin!":
            self.say(nick, "rejoining channels")
            self.rejoin()

        elif cmd == "XXXXXXXXXXXXXX!!!!list":
            srvchans = c.list()
            print c.list
            dir(c.list)
            print c.list.__doc__
            print srvchans

        elif cmd == "XXXXXXXXXXXXXX!!!!!showlog":
            self.say(nick, "outputting log to console.")

            print loglines
            print logidx

            idx = logidx # logidx always points to the oldest entry
            
            print loglines[idx]

            if idx >= logsize or type(loglines[idx]) == type(1):
              idx = 0 # do i really need this here and there? it seems like a minor quibble but algorithms are very important

            while 1:
              if type(loglines[idx]) == type(1): break
              dotext ("`3"+str(logtimes[idx])+"`!::`3"+loglines[idx])
              idx += 1
              if idx >= logsize:
                idx = 0
              if idx == logidx:
                break
                
        elif cmd == "givemeanexperimentalmultilineresponseinoneprivmsgbotty":
            self.say(nick, "ok\nflamoot\nhere\nya\ngo")

        elif cmd == "diediedie   !!!":
            self.writeout()
            self.die()

        elif cmd == "XXXXXXXXXXXXXXXXXXXX!!!!!!!!!!!tree":
            self.say(nick, 'Producing server linkage tree.')
            c.links()

        elif cmd.startswith("tell"):
            args = cmd.split(" ")
            if len(args) < 3:
                self.say(nick, "Usage: tell [#]foo baz baz baz ...")
            else:
                self.say(args[1], " ".join(args[2:]))
                
        elif cmd.startswith("!intrusionprob"):
            args = cmd.split(" ")
            global intrusionprob
            if len(args) < 2:
                self.say(nick, "Usage: !intrusionprob n (where prob is 1/n)...\nn ="+str(intrusionprob))
            else:
              try:
                intrusionprob = int(args[1])
              except:
                self.say(nick, "exception")

        elif cmd.startswith("!threshold"):
            args = cmd.split(" ")
            global threshold
            if len(args) < 2:
                self.say(nick, "Usage: !threshold n (where min object match is > n)\nn = "+str(threshold))
            else:
              try:
                threshold = int(args[1])
              except:
                self.say(nick, "exception")


        elif cmd.startswith("XXXXXXXXXXX!!!!!!!!!!rtfa"):
            args = cmd.split(" ")
            if len(args) < 2:
              self.say(nick, "Usage: rtfa http://foo.baz")
            else:
              if rtfafile == "":
                arg = args[1].strip("\n").strip(" ")
                if not arg[:7].lower() == ("http://"):
                  arg = "http://" + arg
                self.say(nick, "rtfa'ing: "+arg)
                arg = arg.replace("'","")
                arg = arg.replace('"',"")
                arg = arg.replace("\\","")
                arg = arg.replace("\n","")
                arg = arg.replace("\r","")
                arg = arg.replace("\b","")
                rtfaurl = arg
                rtfafile = tempfile.mkstemp()[1]
                rtfafile2 = tempfile.mkstemp()[1]
                rtfaflag = tempfile.mkstemp()[1]
                os.system("rm "+rtfaflag)
                os.system("killall -9 summarize.py; (lynx --dump '"+arg+"' > "+rtfafile+" ; cat "+rtfafile+" | python summarize.py) | tee "+rtfafile2+" ; mv "+rtfafile2+" "+rtfaflag+") &")
                self.say(nick, "summarizing your document in the background. rtfa again to check on it")
              else:
                myfail = 0
                try:
                  TTTF = open(rtfaflag,"r")
                except:
                  myfail = 1
                if myfail == 1:
                  self.say(nick, "i can't rtfa anything now, i'm already grokking "+rtfaurl+" which is still processing or hung. check again though!")
                else:
                  self.say(nick, "hi, i'm sitting on a summary of "+rtfaurl+", previously requested. please make your request again after i finish blatting this thing")
                  TTTF.close()
                  search = "".join(os.popen("cat "+rtfaflag+" | grep SUMMARYDONEEEE --after-context=10000000 | grep -v SUMMARYDONEEEE | nl").readlines())
                  mytl = ""
                  for myl in search.split("."):
                    if mytl.count(".") < 4:
                      mytl = mytl + myl
                    else:
                      myl = mytl
                      mytl = ""                  
                      self.say(nick, (myl+".").replace("\n"," "))
                      xtxt = 0
                      while xtxt < 333000:
                        xtxt += 1 # delay ?!
                  rtfafile = ""
                  rtfaurl = ""
                  rtfaflag = ""
        elif cmd == "XXXXXXXX!!!!!!!rot13":
            if rot13 == 0:
                rot13 = 1
                self.say(nick,"rot13 on")
            else:
                rot13 = 0
                self.say(nick,"rot13 off")

        elif cmd.startswith("XXXXXXX!!!!!!read"):
            args = cmd.split(" ")
            if len(args) < 2:
              self.say(nick, "Usage: read http://foo.baz")
            else:
              arg = args[1].strip("\n").strip(" ")
              if not arg[:7].lower() == ("http://"):
                arg = "http://" + arg
              arg = arg.replace("'","")
              arg = arg.replace('"',"")
              arg = arg.replace("\\","")
              arg = arg.replace("\n","")
              arg = arg.replace("\r","")
              arg = arg.replace("\b","")

              rtfaurl = arg
              pslines = os.popen("lynx --dump '"+arg+"'").readlines()
              self.say(nick, "reading "+arg+" ...")
              hehhh = ""
              for psl in pslines:
                psl = psl.strip("\n").strip(" ")
                if psl == "":
                  continue
                hehhh += psl+" "
              hehhh = re.compile(r"http://.+?(?:[\"' \n]|$)", re.I).sub("", hehhh)
              hehhh = re.compile(r"\[.+?\]", re.I).sub("", hehhh)
              hehhh = re.compile(r"\b\d+\b", re.I).sub("", hehhh)
              hehhh = re.compile(r"(\.\s*){2,}", re.I).sub(". ", hehhh)
              markov("> msg me "+hehhh, donotaddperiods=1)
              self.say(nick, str(len(pslines))+" lines markoved")
        
        elif cmd.startswith("fortune"):
            args = cmd.split("_")
            cmdargs = "-a "
            if len(args) > 1:
                for arg in args:
                    if arg == "short":
                            cmdargs += "-s "
                    elif arg == "long":
                            cmdargs += "-l "
                    elif arg == "inoccuous":
                            cmdargs = cmdargs.replace("-a ", "")
                    elif arg == "offensive":
                            cmdargs = cmdargs.replace("-a ", "-o ")
            self.say(nick, "debug: /usr/games/fortune "+cmdargs)
            self.say(nick, "\n".join(os.popen("/usr/games/fortune "+cmdargs).readlines()))

        elif cmd == "XXXXXXXXXXXXXXX!!!!!!!!!!!!!!!floodoff":
            while 1:
                self.say(nick, "goodbye, cruel world!")

        elif re.compile(r"^XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXwhat\s*['i]?s").search(cmd) != None:
          cmd = cmd.strip("?")
          prepend = e.source().split("!")[0]+"\x02:\x02 "
          result = re.compile(r"^what\s*['i]?s\s+(.+?)\s*(stand for|)$").search(cmd)
          if result == None:
            self.say(nick,prepend+"What's what?")
          else:
            arg = result.group(1)
            if result.group(2) == "stand for":
              arg += " stands for"
            else:
              arg += " is"
            print "Googling '"+arg+"'"
            matched = 0
            linegrabbing = 0
            donegrabbing = 0
            resultresultregex = re.compile(r"("+arg+r"\s+(?:[^. ]+\s*){1,9})", re.I)
            search = os.popen("lynx --dump 'http://google.ca/search?"+urllib.urlencode({"q":arg})+"'").readlines()
            lines = []
            for line in search:
              print line
              resultsresult = re.compile(r"Results 1 - [0-9]+ of about ([0-9,]+) for").search(line)
              resultresult = resultresultregex.search(line)
              if re.compile(r"No standard web pages").search(line) != None and matched == 0:
                print "No matches found for "+arg+"."
                self.say(nick,prepend+"No matches on Google for "+arg+".")
                break
              elif resultsresult != None and matched == 0:
                matched = 1
                self.say(nick,prepend+resultsresult.group(1)+" matches on Google for "+arg+".")
                lines = []
              elif resultresult != None or linegrabbing == 1:
                donegrabbing = 0
                linegrabbing = 1   # start grabbing lines
                if re.compile(r" - \[[0-9]+\]Similar pages").search(line) != None:
                  linegrabbing = 0
                  donegrabbing = 1
                  matched = 0
                else:
                  lines.append(line)
                
              if donegrabbing == 1:
                donegrabbing = 0
                lines = re.compile(r"\s{2,}").sub(" ", " ".join(lines).replace("\n", " "))
                resultresult = resultresultregex.search(lines).group(1)
                self.say(nick,prepend+"A result: "+resultresult)
                lines = []

        elif cmd.startswith("cutup"):
            words = []
            ctr = 0
            
            if cmd.split(" ",1)[0] != cmd: # there was an argument after cutup 
              cmd, speaker = cmd.split(" ", 1)
              print ("Selecting words spoken by "+speaker)
            else:
              speaker = ""
              print ("Making a cutup of all spoken lines")
                            
            for l in loglines:
              print "Processing line "+str(ctr)+" : "+str(l)
              if type(l) == type(1):
                print "Aborting -- end of log hit"
                break # if there's an integer in a loglines[] record then it has not been written to yet, so abort

              ctr += 1
              
              if speaker != "":
                rcv, chan, name = l.split(" ",2)
                
                try:
                  linesayer = name.split("!")[0]
                except:
                  linesayer = nickname # if we can't unpack a speaker name then we must have said the line
                  
                if rcv == "<" and name.split("!")[0] == speaker:
                  print ("Line #"+str(ctr)+" was spoken by "+linesayer+" and was added to the cutup pile")
                elif rcv == "<" and name.split("!")[0] != speaker:
                  print ("Line #"+str(ctr)+" was spoken by "+linesayer+" and is worthless to me now")
                  continue
                elif rcv == ">":
                  print ("Line #"+str(ctr)+" was spoken by me, the malf bot")
                  if speaker != nickname:
                    continue

              words.extend(re.compile(r"\s+").sub(" ", l).split(" ",3)[3].split(" ")) # so we shouldn't get any blanks and uh, bad line to read

            random.shuffle(words) # jesus christ
            cutup = []
            minwords = 10 + int(random.random()*10)
            maxwords = 15 + int(random.random()*25)
            dotext("`0Producing cut-up from `%"+str(ctr)+" `0lines, `%"+str(minwords)+"`0-`%"+str(maxwords)+" `0words long, from `%"+str(len(words))+" `0total words`2.")
            ctr = 0
            for i in range(0,maxwords):
              ctr = ctr + 1
              try:
                word = words[ctr]
              except:
                break
              if word.startswith("http://"):
                continue
              if word.endswith(":") or word.endswith("\x02:\x02"):
                continue
              cutup.append(word)
              if (word.endswith(".") or word.endswith("?") or word.endswith("!")) and ctr > minwords and ctr < maxwords:
                break
            
            dotext ("`0Produced `%"+str(ctr)+"`2-`0word cutup `2'`0"+" ".join(cutup)+"`2'")
            self.say (nick, " ".join(cutup))


        elif cmd == "XXXXXXXXXX!!!!!stats":
            for chname, chobj in self.channels.items():
                self.say(nick, "--- Channel statistics ---")
                self.say(nick, "Channel: " + chname)
                users = chobj.users()
                users.sort()
                self.say(nick, "Users: " + ", ".join(users))
                opers = chobj.opers()
                opers.sort()
                self.say(nick, "Opers: " + ", ".join(opers))
                voiced = chobj.voiced()
                voiced.sort()
                self.say(nick, "Voiced: " + ", ".join(voiced))

        elif cmd == "wb":
            prepend = e.source().split("!")[0]+"\x02:\x02 "
            self.say(nick, prepend+"ty")
            
        elif cmd == "ty":
            prepend = e.source().split("!")[0]+"\x02:\x02 "
            self.say(nick, prepend+"np")

        elif cmd == "XXXXXXXXXXXXXXXXXXX!!!!!!!!dcc":
            dcc = self.dcc_listen()
            c.ctcp("DCC", nick, "CHAT chat %s %d" % (
                ip_quad_to_numstr(dcc.localaddress),
                dcc.localport))

        elif (cmd.startswith("!addquote") or cmd.startswith("!newquote")):
            prepend = e.source().split("!")[0]+"\x02:\x02 "
            quote = re.compile(r"^!(new|add)quote\s*").sub("",cmd)
            if quote.strip() == "":
                self.say(nick, prepend+"error, no quote")
            else:
                quotes.append(e.source().split("!")[0]+"- "+quote)
                self.say(nick, prepend+"quote #"+str(len(quotes))+" added")

        elif (cmd.startswith("!quote")):
            prepend = e.source().split("!")[0]+"\x02:\x02 "
            spkr = re.compile(r"^!quote[^ ]*\s*").sub("",cmd)
            if spkr.strip() == "":
                if quotes != []:
                  self.say(nick, random.choice(quotes))
                else:
                  self.say(nick, prepend+"error, no quotes stored")
            else:
                t = []
                for tt in quotes:
                  if tt.startswith(spkr):
                    t.append(tt)
                if t == []:
                  self.say(nick, prepend+"error, no quotes stored by "+spkr)
                else:
                  self.say(nick, random.choice(t))
                
        elif cmd.startswith("writeout!"):
            self.say(nick, "writing")
            dotext("`@[`8REQUESTED DATAFILE DUMP`4. `8GET READY`4.`@]")
            self.writeout()
            dotext("`@[`8ALL DONE`4.`@]")
            self.say(nick, "written")

        elif cmd.startswith("XXXXXXXXXXXXXXXXXXXXXXXXX!!!!!!!showsummaries"):
            global server
            prepend = e.source().split("!")[0]+"\x02:\x02 "
            args = cmd.split(" ")
            if len(args) < 2:
              self.say(nick, prepend+"Usage: showsummaries #channel")
            else:
              if not chansums.has_key((server+"."+args[1]).lower().replace("#","")):
                self.say(nick, prepend+"No summaries logged for #channel")
              else:
                # does this break now or
                for l in chansums[(server+"."+args[1]).lower().replace("#","")]: # get a list of extractions
                  for ll in l: # get an extraction
                    for lll in cPickle.dumps(ll).split("\n"): # get a meaningless line from pickled extraction forthwith
                      lll = lll.strip()
                      if lll == "":
                        continue
                      self.say(nick, lll)
                
        elif cmd.startswith("markov"):
          cmd = cmd.strip()
          prepend = ""
          self.say(nick, "interrogating markov table")
          myctr = 0
          minsentences = 3 # this may have an off-by-one
          myprint = ""
          markout = ""
          w1 = ""
          w2 = ""
          if cmd.count(" ") == 1 and cmd.split(" ")[0].count("_") == 0 or cmd.split(" ")[0].count("_seedsubject") > 0:
            subjectseed = cmd.split(" ")[1]
            sentenceseed = ""
            self.say(nick, "using subject seed "+subjectseed)
          elif cmd.count(" ") == 1 and cmd.split(" ")[0].count("_seedsentence") > 0:
            sentenceseed = cmd.split(" ")[1]
            subjectseed = ""
            self.say(nick, "using sentence seed "+sentenceseed)
          elif cmd.count(" ") == 2:
            subjectseed = cmd.split(" ")[1]
            sentenceseed = cmd.split(" ")[2]
          else:
            sentenceseed = ""
            subjectseed = ""
          blanks = 0
          maxblanks = 50
          while markout.count("\n") < minsentences and markout.count(".") < minsentences and blanks < maxblanks:
            result = markov("",outputs=1,w1="",w2="",sentenceseed=sentenceseed,subjectseed=subjectseed)
            if result.strip() == "":
              blanks += 1
            else:
              markout += result
          if blanks < maxblanks:
            for l in markout.split("\n"):
              myprint += " "+l
              myctr += 1
              if myctr > 1:
                self.say(nick, myprint)
                myprint = ""
                myctr = 0
            if myctr > 0:
              self.say(nick, myprint)
          else:
            # markov function wouldn't produce minsentences sentences
            # with given parameters, markov fails
            self.say(nick, "- markov function wouldn't produce "+str(minsentences)+" sentences before producing "+str(maxblanks)+" aborted attempts.")
            self.say(nick, "- (sentenceseed='"+sentenceseed+"', subjectseed='"+subjectseed+"')")
        else:
            prepend = e.source().split("!")[0]+"\x02:\x02 "
            if cmd.strip(" ").endswith("?") and random.choice([1,2,3]) != 2:
                answers = ["yes", "you betcha", "that's exactly right", "rarely more than a half-dozen", "it's hard to be sure", "well, you really have to know what you're doing", "i asked my question first?","who are you?","who is this","what","yup"]
                n = random.choice(['1','2','7','6','4'])
                os.system("sleep "+n+"s")
                self.say(nick, prepend+answers[int(random.random()*len(answers))])
            else:
                cmd = cmd.strip()
                if cmd != "" and random.choice(range(34)) != 1: #sometimes be silent tobmalf
                  method = 0

                  blanks = 0
                  minsentences=2
                  myctr = 0
                  myprint = ""
                  markout = ""
                  maxblanks = 50
                  print "markoving"
                  if random.choice([1,2,3]) != 3:
                    subseed = random.choice(cmd.split(" "))
                  else:
                    subseed = ""
                  senseed = ""
                  if cmd.lower().count(" you") > 0 or cmd.lower().count(nickname.lower().replace("_","")) > 0:
                    senseed = "I"
                  elif cmd.lower().startswith("i "):
                    senseed = "you"
                  markov("> msg me "+cmd.strip()+"\n",outputs=0,w1="",w2="",subjectseed=subseed,sentenceseed=senseed) # for privmsgs
                  while markout.count("\n") < minsentences and markout.count(".") < minsentences and blanks < maxblanks:
                    cmd = cmd.strip()
                    if cmd.count(" ")==0:
                      seedone = cmd
                      seedtwo = ""
                      method = 3 # parrot single word openings
                    elif len(cmd.split(" ")) >= 2:
                      myt = cmd.split(" ")
                      print myt
                      seedone = random.choice(myt)
                      myt.remove(seedone)
                      try:
                        seedtwo = random.choice(myt)
                      except:
                        print "SEEDTWO ERROR?!"
                        seedtwo = ""
                    else:
                      seedone = ""
                      seedtwo = ""
                    if method == 0: method = random.choice([1,2,3,4,5,6])
                    seedone = random.choice(seedone.split(" "))
                    seedtwo = random.choice(seedtwo.split(" "))
                    if method == 1:
                      subjectseed = seedone
                      sentenceseed = seedtwo
                    elif method == 2:
                      sentenceseed = seedone
                      subjectseed = seedtwo
                    elif method == 3:
                      sentenceseed = seedone
                      subjectseed = ""
                    elif method == 4:
                      sentenceseed = seedtwo
                      subjectseed = ""
                    elif method == 5:
                      subjectseed = seedone
                      sentenceseed = ""
                    elif method == 6:
                      subjectseed = seedtwo
                      sentenceseed = ""
                    result = markov("",outputs=1,w1="",w2="",sentenceseed=sentenceseed,subjectseed=subjectseed)
                    result = result.strip("\n").strip(" ").strip("\t").strip()
                    if result == "":
                      blanks += 1
                    else:
                      markout += result
                      dotext ("`#>> markov returned `8'`5"+result+"`8'`#]")
                  if blanks < maxblanks:
                    mostsentences = 3 # note this is not the same as maxsentences
                    markout = ". ".join(markout.split(".",mostsentences)[0:-1])# for tersity, max 3 sentences ?
                    mydone = 0
                    while mydone == 0:
                      reresult = re.compile(r"\?([^ ])").search(markout)
                      if reresult != None:
                        markout = re.compile(r"\?([^ ])").sub("? "+reresult.group(1),markout)
                      else:
                        mydone = 1
                    mydone = 0
                    while mydone == 0:
                      reresult = re.compile(r"\!([^ ])").search(markout)
                      if reresult != None:
                        markout = re.compile(r"\!([^ ])").sub("! "+reresult.group(1),markout)
                      else:
                        mydone = 1
                    if markout.startswith("//"):
                      markout = "http:" + markout
                    markout = markout.replace(" //", " http://")
                    for l in markout.split("\n"):
                      myprint += " "+l
                      myctr += 1
                      if myctr > 1:
                        myprint += "\n"
                        myctr = 0
                    myprint = myprint.replace("\n ", "\n").strip()
                    n = random.choice(['1','3','5','2','1','1','2','1'])
                    os.system("sleep "+n+"s")
                    if myprint.startswith("."):
                      myprint = myprint.lstrip(".").strip()
                    self.say(nick, (prepend+myprint).replace("\x02  ","\x02 "))
                  else:
                    # markov function wouldn't produce minsentences sentences
                    # with given parameters, markov fails
                    myprint = prepend+random.choice(["uh",'arg','er','orly','wtf','neg','sure','great',"that's a bald-faced lie"])
                    self.say(nick, myprint)
                    dotext("`%[`8markov function wouldn't produce `5"+str(minsentences)+" `8sentences before producing `5"+str(maxblanks)+" `8aborted attempts.")
                    dotext("`5[`8(sentenceseed='"+sentenceseed+"', subjectseed='"+subjectseed+"')")
# end of do_command

# TODO: break this up
def markov(newlines,outputs=0,donotaddperiods=0,w1="",w2="",sentenceseed="",subjectseed=""):
  global color
  stopword = "\n" # Since we split on whitespace, this can never be a word
  stopsentence = (".", "!", "?", "\n") # Cause a "new sentence" if found at the end of a word
  sentencesep  = "\n" #String used to seperate sentences


  # GENERATE TABLE
  if w1=="": w1 = stopword
  if w2=="": w2 = stopword
  global table
  oldlen = len(table) 
  totalwords = 0        
  for line in newlines.split("\n"):
      if line.strip() == "": continue
      line = line.strip()
      line = line.replace("\n", "")
      if donotaddperiods == 1:
        period = ""
      else:
        period = "."
      line = re.compile(r"\s+").sub(" ", line).split(" ",3)[3]+period
      while line.count("..") > 0:
        line = line.replace("..",".")
      while line.count("!!") > 0:
        line = line.replace("!!","!")
      while line.count("??") > 0:
        line = line.replace("??","?")
      while line.count("?!") > 0:
        line = line.replace("?!","?")
      while line.count("!?") > 0:
        line = line.replace("!?","!")
      print "cooked line: "+line

      firstword = 1
      for word in line.split():
          if (word.endswith(":") or word.endswith("\x02:\x02")) and firstword == 1:
                firstword = 0
                continue
          firstword = 0
          totalwords += 1
          if word[-1] in stopsentence:
              if table.setdefault( (w1, w2), {} ).has_key(word[0:-1]):
                if table.setdefault( (w1, w2), {} )[word[0:-1]] >= 1000 and word[0:-1] == stopword:
                  print "markovdebug> extra stopwords trimmed [1]"
                  table.setdefault( (w1, w2), {} )[word[0:-1]] = 1000
                  pass
                else:
                  table.setdefault( (w1, w2), {} )[word[0:-1]] += 1
              else:
                table.setdefault( (w1, w2), {} ).update({word[0:-1]:1})
              w1, w2 = w2, word[0:-1]
              word = word[-1]
          if table.setdefault( (w1, w2), {} ).has_key(word):
            if table.setdefault( (w1, w2), {} )[word] >= 1000 and word == stopword:
              print "markovdebug>extra stopwords trimmed to 1000 [2]"
              table.setdefault( (w1, w2), {} )[word] = 1000
              pass
            else:
              table.setdefault( (w1, w2), {} )[word] += 1
          else:
            table.setdefault( (w1, w2), {} ).update({word:1})
          w1, w2 = w2, word
  # Mark the end of the file # should i do this at all <<< ???
  if table.setdefault( (w1, w2), {} ).has_key(stopword):
    if table.setdefault( (w1, w2), {} )[stopword] >= 1000: # we're trimmin these now just to be careful like
      print "markovdebug>extra stopwords trimmed to 1000 [3]"
      table.setdefault( (w1, w2), {} )[stopword] = 1000
      pass
    else:
      table.setdefault( (w1, w2), {} )[stopword] += 1
  else:
    table.setdefault( (w1, w2), {} ).update({stopword:1})

  dotext("`5[`8markov'd `#"+str(totalwords)+" `8words.`5]",sameline=1)
  dotext("`#[`8markov cloud grows from `%"+str(oldlen)+"`8 to `%"+str(len(table))+" `8nodes`5.`#]",sameline=1)
  print
  
  if outputs == 0: return ""
  # GENERATE SENTENCE OUTPUT
  maxsentences = 14

  if sentenceseed != "":
    dotext("`#[`8seeking 1.seed `5"+sentenceseed+"`#]",sameline=1)
  if subjectseed != "":
    dotext("`#[`8seeking 2.seed `5"+subjectseed+"`#]",sameline=1)
  sys.stdout.flush()

# new tack  
  w1 = stopword
  w2 = stopword
  sentencecount = 0
  sentence = []

  output = ""

  seedtries = 2500 # not a good way to do this
  seedctr = 0

  if subjectseed != "" and sentenceseed != "" and table.has_key((sentenceseed,subjectseed)):
    w1 = sentenceseed
    w2 = subjectseed
  elif subjectseed != "" and sentenceseed != "" and table.has_key((subjectseed,sentenceseed)):
    w2 = sentenceseed
    w1 = subjectseed
  elif sentenceseed != "" and table.has_key((stopword,sentenceseed)):
    w2 = sentenceseed
    w1 = stopword
  elif sentenceseed != "" and table.has_key((sentenceseed,stopword)):
    w1 = sentenceseed
    w2 = stopword
  elif subjectseed != "" and table.has_key((subjectseed,stopword)):
    w1 = subjectseed
    w2 = stopword
  elif subjectseed != "" and table.has_key((stopword,subjectseed)):
    w2 = subjectseed
    w1 = stopword
  
  sentenceseed = ""
  subjectseed = ""
  
  oldsentenceseed = ""
  while sentencecount < maxsentences:
      if output.count(" ") > 30: # beetris protection
        break
      expansion = []
      for mykey in table[(w1, w2)]:
        for mytemp in range(table[(w1, w2)][mykey]):
          if mykey=="\n" and mytemp > 10:
            pass
          else:
            expansion.append(mykey)
      print "?",
      print str(len(expansion))
      sys.stdout.flush()
      newword = random.choice(expansion) # i should exhaustively search this table instead
      if sentenceseed != "" and newword.lower() != sentenceseed.lower() and sentence == [] and seedctr < seedtries:
        seedctr += 1
        continue
      if seedctr >= seedtries and sentenceseed != "":
        sentenceseed = ""
        dotext("`#[`8seed not found in `5"+str(seedtries)+" `8tries, last candidate word `1'`5"+(newword.replace("\n"," "))+"`1'`#]",sameline=1)
        dotext("`#[`8giving up on sentence seed`#]",sameline=1)
        sentenceseed = ""
      sys.stdout.flush()
      if newword.lower() == sentenceseed.lower() and sentence == [] and sentenceseed != "":
        dotext("`#[`8matched sentence seed `5"+sentenceseed+" `8to word `5"+newword+"`8!`#]")
        oldsentenceseed = sentenceseed
        sentenceseed = ""
      if newword == stopword: return output # some kind of pathological end condition
      if (newword in stopsentence):
          add = 0
          if subjectseed == "":
            add = 1
          else:
            # do this next line with a regex instead ok
            if (" "+(" ".join(sentence).lower())+" ").count(" "+(subjectseed.lower())+" ") > 0:
              dotext("`#[`8matched subject seed `5"+subjectseed+" `8to sentence `5"+(" ".join(sentence))+"`8!`#]")
              add = 1
            else:
              seedctr += 1
              add = 0
              if seedctr >= seedtries:
                dotext("`#[`8seed not found in `5"+str(seedtries)+" `8tries, last candidate sentence `1'`5"+(" ".join(sentence))+"`1'`#]",sameline=1)
                seedctr = 0
                sentencecount += 1 # bad subject seeds will get you an empty list
          if add == 1:
            output += "%s%s%s" % (" ".join(sentence), newword, sentencesep)
            sentencecount += 1
          sentence = []
          seedctr = 0
          if oldsentenceseed != "":
            sentenceseed = oldsentenceseed
      else:
          sentence.append(newword)
      w1, w2 = w2, newword

  return output


def gzipout(fn, gherkin):
  dotext("`%[`8gzippin a gherkin...",sameline=1)
  sys.stdout.flush()
  gzt = ""
  gzt = cPickle.dumps(gherkin)
  gherkin = ""
  print str(len(gzt))+"B",
  sys.stdout.flush()
  (po, pi) = os.popen2("gzip -9 -c > '"+fn+"'")
  po.write(gzt)
  po.close()
  pi.close()
  sys.stdout.flush()
  dotext(" `7done`%]")
  n = len(gzt)
  return n




port = 6667

channelz = ['##grandlan', '#dastoob', '#grlug']
nickname = 'shorttoob'
server = 'irc.freenode.net' 

main()

