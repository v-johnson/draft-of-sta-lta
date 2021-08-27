#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''
Last Updated 8/26/2021, V1
This code reads a csv file of shot times, converts the time to UTCDateTime.

Applies a highpass filter to data and uses STA/LTA detection method to save all detections.

The compares the time of detection to all shots and creates a list of matching times and indices.

'''


# In[ ]:


import obspy
from obspy import UTCDateTime
from obspy.clients.fdsn import Client

from obspy.signal.trigger import plot_trigger
import matplotlib.pyplot as plt


from obspy.signal.trigger import trigger_onset
from obspy.signal.trigger import classic_sta_lta

import re

#%matplotlib notebook

import pandas as pd
from pandas import DataFrame, read_csv
import os
pd.__version__


# In[2]:


data = 'shooting_location_data_new.csv'
df = pd.read_csv(data)
# os.remove(data)
print(df['date'])


# In[3]:


'''
format: 2019-01-08T00:00:00.000000Z
date = year-mm-dd
Unnamed: 5 = hr
Unnamed: 6 = min
Unnamed: 7 = ss.sss
'''

# desire: date + 'T' + hr + ':' + min + ':' + ss + 'Z'

df.dtypes
time_list = []
time_list =  df['date'] + 'T' + df['Unnamed: 5'] + ':' + df['Unnamed: 6'] + ':' + df['Unnamed: 7'] + 'Z'
# time_list =  df['date'] + 'T' + df['Unnamed: 5'] + ':' + df['Unnamed: 6']
time_list = time_list[1:]
for t in time_list:
    print(t)


# In[4]:


trig_on = 150
trig_off = 75

pth = "/data/fast1/time/"
dirs = os.listdir(pth)

detections = []

for file_name in dirs:
    print(file_name)
    st = obspy.read('/data/fast1/time/'+ file_name)
    data = st.select(component="Z")
    # data = data[5:7]
    # data = data[8:]
    data.filter("highpass", freq = 5)
    for tr in data:
        print(tr)
        df = int(tr.stats.sampling_rate)
        cft = classic_sta_lta(tr, (0.01 * df), (2 * df))
        det = trigger_onset(cft, trig_on, trig_off)
        if det != []:
            for d in det:
                detections.append(tr.stats.starttime + (d[0]/df))
            # print((det/df))


# In[5]:


print(det/df)


# In[6]:


# print(data)

print(time_list)


# In[25]:


'''
Reformats time_list into specific UTCDateTime format

UTCDateTime(year,month,day,hour,min,ssms)

'''
shot_times = []
for t in time_list:
    shot_times.append(UTCDateTime(t, iso8601 = "true"))

for s in shot_times:
    print(s)


# In[8]:


'''
Examples breaking down the two portions of the for loop in the below cell.
First tests a single detection time against a specific shot time.
'''


# det_time = UTCDateTime(2019,1,10,23,55,4,17000)
# # det_time = det_UTC[0]
# delta = 8 # seconds
# if ((shot_times[0] - delta) < det_time < (shot_times[0] + delta)):
#     print(det_time)
#     print(shot_times[0])
#     print("Detection occurred near shot")
    

'''
Longer example, testing single detection time for all shot times.
'''

# det_time = UTCDateTime(2019,1,10,23,55,4,17000)

# delta = 8 # seconds
# for t in shot_times:
#     if ((t - delta) < det_time < (t + delta)):
#         print(det_time)
#         print(shot_times[0])
#         print("Detection occurred near shot")

'''
Longer example, testing all detection times for one shot time.
'''

# # det_time = UTCDateTime(2019,1,10,23,55,4,17000)
# # det_time = det_UTC[0]
# delta = 8 # seconds
# for d in det_UTC:
#     print(d[0])
#     if ((shot_times[0] - delta) < d[0] < (shot_times[0] + delta)):
#         print(shot_times[0])
#         print("Detection occurred near shot")
    


# In[16]:


'''
Loops through every detection time and compares to every shot time.
Delay is used to match to actual shot detections and not airblast at time of shot.
'''
delta = 4.033
delay = 5
det_matches = []
shot_matches = []

for t in shot_times:
    for d in detections:
        if (((t + delay) - delta) < d < ((t + delay) + delta)):
            #print("                  Detection occurred near shot.")
            det_matches.append(d)
            shot_matches.append(t)
for match in det_matches:
    print(match)
# for match in shot_matches:
#     print(match)
print(len(det_matches))


# In[11]:


len(detections)


# In[23]:


'''
Creates a list of indices corresponding to what detections match a shot.
'''
indices = []
for d in det_matches:
    indices.append(detections.index(d)+1)
    
print(indices)

for i in indices:
    print(detections[i-1])


# In[ ]:




