import curses
import time
import System
import Process
import Format

# 50 bars uniformly displayed from 0 - 100 %
# 2% is one bar(|)

def ProgressBar(percent) :
  result = "0%"
  size   = 50
  bars   = percent * size 

  for  i in range(size) :  
    if i <= bars :
        result = result + '|' 
    else :
        result = result + ' '
  

  display = str(percent * 100)
  display = display[0:4]

  if percent < 0.1 or percent == 1.0 :
    display = " " + str(percent * 100)[0:3]
  return result + " " + display + "/100%"

#########################################################

def DisplaySystem( system_, window_) :
  row = 0
  
  window_.addstr( 1 +row, 2, ("OS: " + system_.OperatingSystem()))
  window_.addstr( 2 +row, 2, ("Kernel: " + system_.Kernel()))
  window_.addstr( 3 +row, 2, "CPU: ")
  window_.attron(curses.color_pair(1))
  window_.addstr( 3+row, 10, "")
  window_.addstr( ProgressBar(system_.Cpu(system_).Utilization(system_.Cpu(system_))))
  window_.attroff(curses.color_pair(1))
  window_.addstr( 4 +row, 2, "Memory: ")
  window_.attron( curses.color_pair(1) )
  window_.addstr( 4+row, 10, "")
  window_.addstr( ProgressBar(system_.MemoryUtilization()))
  window_.attroff(curses.color_pair(1))
  window_.addstr( 5+row, 2,
            ("Total Processes: " + str(system_.TotalProcesses())))
  window_.addstr(6+row, 2, ("Running Processes: " + str(system_.RunningProcesses())))
  window_.addstr(7+row, 2, ("Up Time: " + Format.ElapsedTime(system_.UpTime())))
  window_.refresh()
  return [system_ , window_]

#########################################################

def DisplayProcesses( processes_, window_,  n) :
  row =0
  pid_column =2
  user_column =9
  cpu_column = 25
  ram_column =35
  time_column =50
  command_column = 60
  window_.attron(curses.color_pair(2))
  window_.addstr(1+row, pid_column, "PID")
  window_.addstr(1+row, user_column, "USER")
  
  try:
    window_.addstr(1+row, cpu_column, "CPU[%%]")
    window_.addstr(1+row, ram_column, "RAM[MB]")
    window_.addstr(1+row, time_column, "TIME+")
    window_.addstr(1+row, command_column, "COMMAND")
    window_.attroff(curses.color_pair(2))
  except curses.error:
    pass
  
  num_processes = processes_.__len__()
  if num_processes > n :
    num_processes = n
  row +=1  
  for  i in range(10) :
    row = row + 1
    window_.addstr(row, pid_column, str(processes_[i].Pid()))
    window_.addstr(row, user_column, processes_[i].User())
    cpu = processes_[i].CpuUtilization_() * 100
    window_.addstr(row, cpu_column, str(cpu)[0:4])
    window_.addstr(row, ram_column, processes_[i].Ram())
    window_.addstr(row, time_column,Format.ElapsedTime(processes_[i].UpTime()))
    x_max=window_.getmaxyx()
    x_max = x_max[1]
    window_.addstr(row, command_column,str(processes_[i].Command())[0 : 15])
  
  return window_
#########################################################

def Display(system_ ,  n) :
  stdstr=curses.initscr()      # start ncurses
  curses.noecho()       # do not print input values
  curses.cbreak()       # terminate ncurses on ctrl + c
  curses.start_color()  # enable color

  yx_max = stdstr.getmaxyx()
  x_max  = yx_max[1]
  y_max = yx_max[0]
  system_window =  curses.newwin(9, x_max-1 ,0 ,0)
  process_window = curses.newwin(n+3, x_max -1,9,0)
  while (1) :
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    system_window.box( 0, 0)
    process_window.box(0 , 0)

    
    
    
    Ret=DisplaySystem(system_, system_window)
    system_=Ret[0]
    system_window = Ret[1]
    
    process_window = DisplayProcesses(system_.Processes(system_), process_window, n)
    

    system_window.refresh()
    process_window.refresh()
    stdstr.refresh()
    time.sleep(0.2)
  
  curses.echo()  
  curses.nocbreak()
  curses.endwin()
####################################################
