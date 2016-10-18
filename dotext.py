#!/usr/bin/python

def dotext(txt, sameline=0):
  burytoken = "\xfe\xfd"
  esc = "`"

  if txt.__contains__(esc):
    # bury ``
    txt = txt.replace(esc+esc,burytoken)
  
    txt = txt.replace(esc+"1", "\x1b[0;34m") # lo blue 
    txt = txt.replace(esc+"2", "\x1b[0;32m") # lo green
    txt = txt.replace(esc+"3", "\x1b[0;36m") # lo cyan
    txt = txt.replace(esc+"4", "\x1b[0;31m") # lo red
    txt = txt.replace(esc+"5", "\x1b[0;35m") # lo magenta
    txt = txt.replace(esc+"6", "\x1b[0;33m") # lo yellow
    txt = txt.replace(esc+"7", "\x1b[0;37m") # lo white
    txt = txt.replace(esc+"8", "\x1b[1;30m") # hi black
    txt = txt.replace(esc+"9", "\x1b[1;34m") # hi blue
    txt = txt.replace(esc+"0", "\x1b[1;32m") # hi green
    txt = txt.replace(esc+"!", "\x1b[1;36m") # hi cyan
    txt = txt.replace(esc+"@", "\x1b[1;31m") # hi red
    txt = txt.replace(esc+"#", "\x1b[1;35m") # hi magenta
    txt = txt.replace(esc+"$", "\x1b[1;33m") # hi yellow
    txt = txt.replace(esc+"%", "\x1b[1;37m") # hi white
  
    # disinter and decode ``
    txt = txt.replace(burytoken,esc)

  #return txt
  if sameline == 0:
    print txt
  else:
    print txt,

def wee():
  #print dotext("``bobjoe``")

  dotext("`8``1`9# `1lo blue\t", sameline = 1)
  dotext("`8``2`0# `2lo green\t", sameline=1)
  dotext("`8``3`!# `3lo cyan\t", sameline=1)
  dotext("`8``4`@# `4lo red ", sameline=0)
  dotext("`8``5`## `5lo magenta\t", sameline=1)
  dotext("`8``6`$# `6lo yellow\t", sameline=1)
  dotext("`8``7`%# lo white\t", sameline=1)
  dotext("`8``8# `8hi black", sameline=0)
  dotext("`8``9`1# `9hi blue\t", sameline=1)
  dotext("`8``0`2# `0hi green\t", sameline=1)
  dotext("`8``!`3# `!hi cyan\t", sameline=1)
  dotext("`8``@`4# `@hi red ", sameline=0)
  dotext("`8``#`5# `#hi magenta\t", sameline=1)
  dotext("`8``$`6# `$hi yellow\t", sameline=1)
  dotext("`8``%`7# `%hi white", sameline=1)
