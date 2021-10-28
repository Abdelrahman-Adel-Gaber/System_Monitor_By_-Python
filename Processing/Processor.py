import LinuxParser 

class processor :
      
    def Utilization(self) :
        self.cached_active_ticks_ = 0
        self.cached_idle_ticks_   = 0
    
        utilization = 0
        active_ticks = LinuxParser.ActiveJiffies()
        idle_ticks = LinuxParser.IdleJiffies()
        duration_active= active_ticks - self.cached_active_ticks_
        duration_idle = idle_ticks - self.cached_idle_ticks_
        duration = duration_active + duration_idle
        utilization = float(duration_active) / duration
        self.cached_active_ticks_ = active_ticks
        self.cached_idle_ticks_ = idle_ticks
        return utilization
        
