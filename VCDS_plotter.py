# -*- coding: utf-8 -*-
"""
Created on Thu Apr 17 16:02:18 2025

Begin working on a VCDS log viewer with interactive plotting.
 - import data series from a log
 - plot results simply by selecting X-axis variable, Y-axis variable(s)
 - interactive plot tool GUI for no-code analysis

@author: noursec
"""
# %% imports
import re 
# %% read file for testing
folder = "VCDS logs"
file = "LOG-01-IDE00149_&11.CSV"
print_lines = 20
with open(f'{folder}/{file}', 'r') as f:
    i=0
    for line in f:
        if i<print_lines:
            print(line)
        i+=1
# %% parse logfile into object
with open(f'{folder}/{file}', 'r') as f:
    log = {'info':{}, 
           'data':{'timestamps':[], 
                   'data':[]}}
    i=0
    for line in f:
        line = line.rstrip(',\n')
        i+=1
        match i:
            case 1:
                # log information
                # eg. "Tuesday,08,April,2025,18:09:12:57411-VCID:46D54548C829E90A257-8012,VCDS Version: Release 24.7.1 (x64),Data version: 20240919 DS356.3"
                p = r'^(?P<date_DoW>[a-zA-Z]+),(?P<date_day>[0-9]+),(?P<date_month>[a-zA-Z]+),(?P<date_year>[0-9]+),(?P<date_time>[0-9:]+)\-VCID:(?P<VCID>[0-9A-Z\-]+),VCDS Version: (?P<VCDS_version>.+?),Data version: (?P<data_version>.+?)$'
                m = re.match(p,line)
                if m is not None:
                    log['info'].update(m.groupdict())
                else:
                    raise ValueError(f'incorrect log format file: line{i}')
            case 2:
                # engine info
                # eg. "8V0 906 264 M,ADVMB,1.8l R4 TFSI  H13 0001,"
                p = r'^(?P<engine_sw_mpn>[A-Z0-9\ ]+),(?P<measuring_blocks>.+?),(?P<engine_component>.+?)$'
                m = re.match(p,line)
                if m is not None:
                    log['info'].update(m.groupdict())
                else:
                    raise ValueError(f'incorrect log format file: line {i}')
            case 3:
                # measuring block group and field info
                # eg. ",,G018,F0,G021,F0,..."
                line = line.strip().split(',')
                groups = [g.strip('G') for g in line[::2]] # strip 'G' and 'F' from group/field numbers
                fields = [f.strip('F') for f in line[1::2]] 
                log['data']['groups'] = groups # marker column has empty group and field;
                log['data']['fields'] = fields # length is number of measurements + 1 for marker
            case 4:
                continue # blank
            case 5:
                # measuring bloc locations 
                # eg. "Marker,TIME,Loc. IDE00149,TIME,Loc. IDE00155,..."
                line=line.strip().split(',')
                locations = [l.strip('Loc. ') for l in line[::2]]
                log['data']['locations'] = locations
                continue
            case 6:
                # measuring bloc labels 
                # eg. ",STAMP,Ignition angle of current cylinder: actual value,STAMP,Ignition timing angle retard cylinder 1,..."
                line=line.strip().split(',')
                labels = [l.strip() for l in line[::2]]
                # set first label to 'Marker' (blank in this row)
                labels[0] = 'Marker'
                log['data']['labels'] = labels
                continue
            case 7:
                # measurment data units
                # eg: ",,  ,,  ,,  ,,  ,,  ,,  ,,  ,,  ,, Degrees,, ,,  ,,  ,"
                line = line.strip().split(',')
                units = [u.strip() for u in line[::2]]
                log['data']['units'] = units
                continue
            case _:
                # data row
                # eg: ",0.47,3.75,0.05,0.00,0.08,0.00,0.10,0.00,0.18,0.00,0.21,0.0,0.26,0.0,0.27,-1.8,0.31,3.0,0.34,0,0.40,27.00,0.42,3.00,"
                line = line.strip().split(',')
                data = line[::2]         # should have same length as labels
                timestamps = line[1::2]  # one shorter than labels, because marker doesn't have timestamp
                log['data']['data'].append(data)
                log['data']['timestamps'].append(timestamps)
                continue
