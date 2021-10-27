import LinuxParser 

class process :
  def __init__(self, pid) :
      self.pid_ = pid
      self.cpu_ = 0.0
      self.cached_active_ticks_ = 0
      self.cached_idle_ticks_ = 0
      self.cached_system_ticks_ =0

  def Pid(self) :
      return self.pid_                               
  
  def User(self) :      
      return LinuxParser.User(self.pid_)
                     
  def Command(self) :
      return LinuxParser.Command(self.pid_)

  def CpuUtilization_(self) :
      return self.cpu_

  def CpuUtilization(self, active_ticks, system_ticks) :
      duration_active = active_ticks - self.cached_active_ticks_
      duration=system_ticks - self.cached_system_ticks_
      self.cpu_ = duration_active / duration
      self.cached_active_ticks_ = active_ticks
      self.cached_system_ticks_ = system_ticks


  def Ram(self) :  
      return LinuxParser.Ram(self.pid_)                     
  
  
  def UpTime(self) :     
      return LinuxParser.UpTime(self.pid_)                  
  
  def __lt__(self, other) :
   return self.cpu_ > other.cpu_
  
  def __gt__(self, other) :
   return self.cpu_ < other.cpu_
  