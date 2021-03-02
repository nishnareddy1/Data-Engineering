#!/usr/bin/env python
# coding: utf-8

# In[5]:


# Validation of assertions

import pandas as pd
import numpy as np
import math

df = pd.read_csv ('Downloads/oregon-crash2019.csv')


# In[53]:


# 41 to 46 Latitude Degrees

fasle_records=0
nan_records=0
for data in df['Latitude Degrees']:
    if (data<41 or data>46):
        fasle_records+=1
    elif math.isnan(data):
        nan_records+=1
        
print('fasle_records',fasle_records)
print('nan_records',nan_records)


# In[7]:


# 0 to 59 Latitude Minutes

fasle_records=0
nan_records=0
for data in df['Latitude Minutes']:
    if (data>=0 and data<=59):
        pass
    elif math.isnan(data):
        nan_records+=1
    else:
        fasle_records+=1
        
print('fasle_records',fasle_records)
print('nan_records',nan_records)


# In[8]:


# 0.00 to 59.99 Latitude Seconds

fasle_records=0
nan_records=0

for data in df['Latitude Seconds']:
    if (data>=0 and data<=59.99):
        pass
    elif math.isnan(data):
        nan_records+=1
    else:
        fasle_records+=1
        
print('false_records',fasle_records)
print('nan_records',nan_records)


# In[9]:


# A crash hour should be between 0-24

fasle_records=0
nan_records=0

for data in df['Crash Hour']:
    if (data>=0 and data<=24):
        pass
    elif math.isnan(data):
        nan_records+=1
    else:
        fasle_records+=1
        
print('false_records',fasle_records)
print('nan_records',nan_records)


# In[27]:


#On average, more crashes occur when the weather is clear.
from collections import defaultdict
dic=defaultdict(int)
weather = {
0: 'Unknown',
1: 'Clear',
2: 'Cloudy',
3: "Rain",
4: 'Sleet / Freezing Rain / Hail',
5: 'Fog',
6: 'Snow',
7: 'Dust',
8: 'Smoke',
9: 'Ash'
}

for data in df['Weather Condition']:
    if math.isnan(data):
        dic['nan_records']+=1
    else:
        dic[weather[data]]+=1
        
print(dic)


# In[46]:


from collections import defaultdict
count=defaultdict(int)
df1=list(zip(df['Weather Condition'], df['Road Surface Condition']))
road={
0:'Unknown',
1: 'Dry',
2: 'Wet',
3: 'Snow',
4: 'Ice'
}

wrong_entries=0
for data in df1:
    if data[0]==1 and data[1] in road:
        count[road[data[1]]]+=1
    elif math.isnan(data[1]):
        pass
    elif data[1] not in road:
        wrong_entries+=1
        
print('wrong entries', wrong_entries)
## Suprisingly more crashes occured when the when the weather condition is clear and road surface is dry (o_O)
print(str(dic['Clear'])+' crashes on clear weather condition with road surface condition: '+str([(i,dic[i]) for i in dic]))


# In[38]:


#All the crashes occurred during the day light.
from collections import defaultdict
light=defaultdict(int)
light_condition = {0: 'Unknown',
1: 'Daylight',
2: 'Darkness',
3: 'Darkness',
4: 'Dawn (Twilight)',
5: 'Dusk (Twilight)'}

for data in df['Light Condition']:
    if math.isnan(data):
        light['nan_records']+=1
    else:
        light[light_condition[data]]+=1
        
print(light)


# In[52]:


# Vehicle ID should be 7 digits

false_entries=0
correct_entries=0
nan_entries=0

for data in df['Vehicle ID']:
    if math.isnan(data):
        nan_entries+=1
    else:
        if len(str(int(data)))==7:
            correct_entries+=1
        else:
            false_entries+=1
            
print('false_entries',false_entries)
print('correct_entries',correct_entries)
print('nan_entries',nan_entries)
