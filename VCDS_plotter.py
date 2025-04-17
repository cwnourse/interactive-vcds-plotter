# -*- coding: utf-8 -*-
"""
Created on Thu Apr 17 16:02:18 2025

Begin working on a VCDS log viewer with interactive plotting.
 - import data series from a log
 - plot results simply by selecting X-axis variable, Y-axis variable(s)
 - interactive plot tool GUI for no-code analysis

@author: noursec
"""
folder = "VCDS logs"
file = "LOG-01-IDE00149_&11.CSV"

print_lines = 20

with open(f'{folder}/{file}', 'r') as f:
    i=0
    for line in f:
        if i<print_lines:
            print(line)
        i+=1