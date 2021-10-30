import enum 
import os

kProcDirectory="/proc/"
kCmdlineFilename = "/cmdline" 
kCpuinfoFilename = "/cpuinfo" 
kStatusFilename = "/status" 
kStatFilename = "/stat" 
kUptimeFilename = "/uptime" 
kMeminfoFilename = "/meminfo" 
kVersionFilename = "/version" 
kOSPath = "/etc/os-release" 
kPasswordPath = "/etc/passwd" 


class CPUStates(enum.Enum) :
  kUser_      = 0
  kNice_      = 1
  kSystem_    = 2
  kIdle_      = 3
  kIOwait_    = 4
  kIRQ_       = 5
  kSoftIRQ_   = 6
  kSteal_     = 7
  kGuest_     = 8
  kGuestNice_ = 9


##########################################################

def Pids() :
  pids_values = []
  strl=os.listdir("/proc")
  for dirs in strl:
      if os.path.isdir("/proc/"+dirs) and dirs.isnumeric():
        pids_values.append(int(dirs))
  return pids_values 

##########################################################

def MemoryUtilization() :
   mem_total = 1.0 
   mem_free  = 0.0 
   buffers   = 0.0

   f = open(kProcDirectory + kMeminfoFilename ,"r")
   stream = f.readlines()
   for line in stream :
       Str = line.split()
       if Str[0] == "MemTotal:" :
           mem_total = float(Str[1])
       elif Str[0] == "MemFree:" :
           mem_free = float(Str[1])
       elif Str[0] == "Buffers:" :
           buffers = float(Str[1])
           
   return 1 - mem_free / (mem_total - buffers)

##########################################################
def UpTime_() :
  line  = ""
  
  f = open(kProcDirectory + kUptimeFilename)
  stream =f.readline()
  line = stream.split()

  return float(line[0])


##########################################################
def Jiffies() : 
  return UpTime_() * os.sysconf(int(os.sysconf_names['SC_CLK_TCK']))

##########################################################
def ActiveJiffies_(pid) :
  line = ""
  token = ""
  try :
    f = open (kProcDirectory + str(pid) + kStatFilename)
    f = f.readline()
    stream = f.split()
    jiffies = 0     
    if(stream.__len__() > 21) :
      user = int(stream[13])
      kernel = int(stream[14])
      children_user = int(stream[15])
      children_kernel = int(stream[16])
      jiffies = user + kernel + children_user + children_kernel
    
    return jiffies
  except:
    return 0
  
##########################################################

def CpuUtilization() :
  line = ""
  token = ""
  f = open(kProcDirectory + kStatFilename)
  f = f.readlines()
  for stream in f :
     line = stream.split()    
     if (line[0] == "cpu") :
       line.remove(line[0])  
       return line
   
  return []

##########################################################

def ActiveJiffies() :
  time = CpuUtilization()
  return (int(time[CPUStates.kUser_.value]) + int(time[CPUStates.kNice_.value]) +
          int(time[CPUStates.kSystem_.value]) + int(time[CPUStates.kIRQ_.value]) +
          int(time[CPUStates.kSoftIRQ_.value]) + int(time[CPUStates.kSteal_.value]) +
          int(time[CPUStates.kGuest_.value]) + int(time[CPUStates.kGuestNice_.value]))

##########################################################

def IdleJiffies() :
  time = CpuUtilization()
  return (int(time[CPUStates.kIdle_.value]) + int(time[CPUStates.kIOwait_.value]))

##########################################################

def TotalProcesses() :
  f = open(kProcDirectory + kStatFilename)
  stream = f.readlines()
  for l in stream :
    l = l.split()   
    if l[0] == "processes" : 
     return int(l[1])
  
  return 0

##########################################################

def RunningProcesses() :
  line = ""
  f = open(kProcDirectory + kStatFilename)
  stream = f.readlines()
  for l in stream :
    l = l.split()   
    if l[0] == "procs_running" :
      return int(l[1])
  
  return 0


##########################################################


def OperatingSystem() :
  value = ""
  f = open(kOSPath)
  lines = f.readlines()  
  for l in lines :
    l = l.replace(' ', '_')
    l = l.replace('=', ' ')
    l = l.replace('"', ' ')
    l = l.split()
    if l[0] == "PRETTY_NAME" :
      value = l[1].replace('_', ' ')
      return value
  
  return value

##########################################################

def Kernel() : 
  f = open(kProcDirectory + kVersionFilename)
  stream = f.readline()
  stream = stream.split()
  return stream[2]

##########################################################

def Command( pid ) :
  try :  
    f = open (kProcDirectory + str(pid) + kCmdlineFilename)
    line = f.readline()
    return line
  except :
    return ""  
##########################################################

def Ram( pid ) :
  f = open(kProcDirectory + str(pid) + kStatusFilename)
  stream = f.readlines()
  for l in stream :
    l = l.split() 
    if  l[0] == "VmSize:" : 
      return str(int(l[1]) / 1024)
  
  return "0"


##########################################################


def Uid( pid) :
  try :  
    f= open( kProcDirectory + str(pid) + kStatusFilename)
    stream = f.readlines()
    for l in stream :
      l = l.split()
      if (l[0]== "Uid:")  :
        return l[1]
    return ""
    
  except :  
   return ""

  
##########################################################

def User( pid) : 
  f = open(kPasswordPath)
  token = "x:" + Uid(pid)
  stream = f.readlines()
  for l in stream :
    marker = l.find(token)
    if marker != -1 :
      return l[0:marker-1] 
  
  return "0"

##########################################################


def UpTime(pid) : 
  time = 0
  try :
    f = open(kProcDirectory + str(pid) + kStatFilename)
    lines = f.readline()
    time = lines.split()[13]
    time =float(time) /os.sysconf(int(os.sysconf_names['SC_CLK_TCK']))
    return time
  except :
   return time


##########################################################
