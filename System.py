import LinuxParser
import Process
import Processor

class system :
      
    # Return the system's CPU
    def Cpu(self) :
        self.cpu_ = Processor.processor
        return self.cpu_

    # Return a container composed of the system's processes 
    def Processes(self) :
        pids = LinuxParser.Pids()
        self.processes_ = []

        extant_pids = []
        for  p in  self.processes_: 
         extant_pids.append( p.Pid() )
        
        extant_pids = set(extant_pids)
        
        #Emplace All new Processes
        for  pid in pids :
         if not extant_pids.__contains__(pid)  :
            self.processes_.append(Process.process(pid))
        
        for  p in self.processes_  :
         p.CpuUtilization(LinuxParser.ActiveJiffies_(int(p.Pid())), LinuxParser.Jiffies())
        
        self.processes_.sort()
        
        return self.processes_


    #  Return the system's kernel identifier (string)
    def Kernel() : 
        return LinuxParser.Kernel()


    # Return the system's memory utilization
    def  MemoryUtilization() :
        return LinuxParser.MemoryUtilization()


    # Return the operating system name
    def OperatingSystem() : 
        return LinuxParser.OperatingSystem() 


    # Return the number of processes actively running on the system
    def RunningProcesses() :
        return LinuxParser.RunningProcesses()


    # Return the total number of processes on the system
    def TotalProcesses() : 
        return LinuxParser.TotalProcesses()


    # Return the number of seconds since the system started running
    def UpTime() : 
        return LinuxParser.UpTime_()


'''
S = system
print(S.Processes(S)[88].CpuUtilization_())
'''    
    
        

         