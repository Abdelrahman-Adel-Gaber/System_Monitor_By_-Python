def Pad (s) :
    if  s.__len__() == 1 :
      s = '0' + s 
    elif s.__len__() == 0 :
        s = "00"
    return s         

def ElapsedTime(time) :
  hours = int(time / (60 * 60))
  minutes = int ((time / 60) % 60)
  seconds = int (time % 60)
  return Pad(str(hours)) + ":" + Pad(str(minutes)) + ":" + Pad(str(seconds))
