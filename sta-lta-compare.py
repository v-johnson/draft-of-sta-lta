#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''
Last Updated 8/26/2021, V1
Updates to filtering needed.

This code applies an STA-LTA method to given data, applying a highpass filter and saves plots of traces and detections.

'''


# In[ ]:


import obspy
from obspy import UTCDateTime
from obspy.clients.fdsn import Client

from obspy.signal.trigger import plot_trigger
import matplotlib.pyplot as plt


from obspy.signal.trigger import trigger_onset
from obspy.signal.trigger import z_detect
from obspy.signal.trigger import classic_sta_lta
from obspy.signal.trigger import recursive_sta_lta

import re
import os

#%matplotlib notebook


# In[ ]:


'''
Handles instrument response and reads desired files.
'''

# Applicable to Whillans Ice Plain Data only.
# client = Client("IRIS")
# t1 = UTCDateTime("2011-01-01T00:00:00")
# t2 = UTCDateTime("2011-01-10T00:00:00")
# st = client.get_waveforms("2C", "BB01", "--", "HHZ", t1, t2, attach_response=True)

# pre_filt = (0.001, 0.002, 50, 100)
# # pre_filt = (0.001, 0.002, 0.05, 0.1)
# # st.remove_response(output='VEL', pre_filt=pre_filt)
# st.remove_response(output='DISP', pre_filt=pre_filt)
# # st.plot()

# for tr in st: 
#     tr.write(tr.id + ".MSEED", format="MSEED") 

# data = obspy.read('/data/fast1/wip/2C.BB01..HHZ.MSEED') # Whillans Ice Plain
data = obspy.read('/data/fast1/time/TIME_WAIS_2000_20190105_20190116.mseed') #TIME Data at WAIS


# In[ ]:


'''
Creates a list of all station files in given TIME directory.
'''

pth = "/data/fast1/time/"
dirs = os.listdir(pth)
print(dirs)


# In[ ]:


'''
Statment to review stats of individual trace.
'''

print(data[18].stats)


# In[ ]:


'''
Filters data, needs updating.
'''

# pre_filt = (1, 2, 250, 500)
# data.remove_response(output='VEL', pre_filt=pre_filt)


# In[ ]:


'''
Chooses which data set is being used and the time frame.
Can trim desired time frame, while commented out, uses full trace.
'''

#For whillans:
# t0 = UTCDateTime("2011-01-01T09:00:00")
# t1 = UTCDateTime("2011-01-01T12:00:00")
# tr = data[0].trim(t0,t1)

#For time:
# tr = data[18]

# t0 = UTCDateTime("2019-01-07T02:00:00")
# t1 = UTCDateTime("2019-01-07T06:00:00")
# data[18] = data[18].trim(t0,t1)


# In[ ]:


'''
Applies a high pass filter.
'''
data.filter("highpass", freq = 5)


# In[ ]:


'''
Shows a trigger plot for each trace and saves them.
det holds the start and stop times of when the STA/LTA ratio reaches the desired triggers.

'''
trig_on = 10
trig_off = 5

for file_name in dirs:
    name = re.search(r'(?<=TIME_WAIS_)\d+', file_name).group(0)
    det_count = 0
    st = obspy.read('/data/fast1/time/'+ file_name)
    data = st.select(component="Z")
    data.filter("highpass", freq = 5)
    for tr in data:
        '''
        Applies STA/LTA method.
        '''
        df = tr.stats.sampling_rate
        cft = classic_sta_lta(tr, (0.25 * df), (5 * df))
        det = trigger_onset(cft, trig_on, trig_off)
        plot_trigger(tr, cft, trig_on, trig_off)
        # print((det/df/60))
        for d in det:
            det_count += 1
            # print(d)
            save_name = ("Run/detection_%f.png" %  det_count)
            data.plot(starttime = tr.stats.starttime + d[0]/df, endtime = tr.stats.starttime + d[1]/df, outfile = save_name)
        # plt.savefig("Trigger_Plot_Station_%s_trace_%f.png" % (name, count))


# In[ ]:


'''
Loops through every trace to make a plot after applying STA/LTA. Could become a function held elsewhere.

'''
trig_on = 10
trig_off = 5

for file_name in dirs:
    name = re.search(r'(?<=TIME_WAIS_)\d+', file_name).group(0)
    d = obspy.read('/data/fast1/time/'+ file_name)
    data = d.select(component="Z")
    data.filter("highpass", freq = 5)
    for tr in data:
        df = tr.stats.sampling_rate
        cft = classic_sta_lta(tr, (0.25 * df), (5 * df))
        plt.plot(cft)
        plt.show()
        print((det/df/60))
        plt.savefig("pyplot_Station_%s_trace_%f.png" % (name, i))


# In[ ]:


'''
Plots a trigger plot and STA/LTA plot for a single trace. Could become a function held elsewhere. 
'''
trig_on = 10
trig_off = 5

df = tr.stats.sampling_rate

# Classic STA-LTA method
cft = classic_sta_lta(tr, (0.25 * df), (5 * df))

# Z-Detect method
# cft = z_detect(data[0], (df*1))

# Recursive STA-LTA method
# cft = recursive_sta_lta(data[0], (5 * df), (10 * df))

plt.plot(cft)
# plt.savefig("pyplot_trace_18.jpeg")
plt.show()
det = trigger_onset(cft, trig_on, trig_off)
plot_trigger(tr, cft, trig_on, trig_off)
# plt.savefig("triggerplot_trace_18.jpeg")


# In[ ]:


'''
Prints time after UTC starttime in minutes for start and stop of events. 
'''

print((det/df/60))
print(len(det))


# In[ ]:


'''
Plots time surrounding events
'''

for d in det:
    print(d)
    data.plot(starttime = data[18].stats.starttime + d[0]/df, endtime = data[18].stats.starttime + d[1]/df)
#     plt.plot(cft[d[0]:d[1]])
#     plt.show()
    #plt.savefig("detplot_trace_18_%f.jpeg" %d)


# In[ ]:




