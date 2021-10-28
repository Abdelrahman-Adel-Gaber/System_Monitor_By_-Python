#!/usr/bin/env python3

import os
import sys
main_path = os.path.abspath(__file__[:-7])
print(main_path)
sys.path.insert(0, main_path + "/Display/")
sys.path.insert(0, main_path + "/Processing/")

import Ncurses_Display
import System

def main() :
  S = System.system
  Ncurses_Display.Display(S , 10)  

main()  
