## 
import pandas as pd
from datetime import timedelta
import re
df = pd.read_csv('Downloads/data_file (1).csv')
tstamp_df = pd.DataFrame(columns=['TIME STAMP'])
timestamps=[]
dic={'JAN':'01', 'FEB':'02', 'MAR':'03', 'APR':'04','MAY':'05','JUN':'06',
     'JUL':'07','AUG':'08','SEP':'09','OCT':'10','NOV':'11','DEC':'12'}
t_stamp= df.filter(['OPD_DATE','ACT_TIME'])
print(t_stamp['OPD_DATE'].head())
from datetime import datetime
for index in range(len(df['OPD_DATE'])):
    date=df['OPD_DATE'][index][0:2]
    month=dic[df['OPD_DATE'][index][3:6]]
    year=df['OPD_DATE'][index][7:10]
    time=df['ACT_TIME'][index]
    str_time = str(timedelta(seconds=int(time)))
    # str time can be '1 day 00:00:34'
    if 'day' in str_time:
        add_days = ''
        for i in range(len(str_time)):
            if str_time[i] == ' ':
                s = str_time[i + 1:]
                break
            add_days += str_time[i]
        date = int(date) + int(add_days)
        # remove 1 day from str_time
        str_time = re.sub("[^0-9:]", "", s)
    dt=str(date)+month+year+str_time
    tstamp=datetime.strptime(dt, '%d%m%y%H:%M:%S')
    timestamps.append(tstamp)

df.insert(2, "TIME STAMP", timestamps)
df.drop(columns=['OPD_DATE','ACT_TIME'],inplace=True, axis=1)


## For each trip id, have a single route no, service key and direction
## stop_df --> trip_id, vehicle_id, direction, service_key, route_id

groupby_trip = stopdf.groupby('trip_id')
groups = groupby_trip.groups.keys()
column_names = ['trip_id','vehicle_id','route_id', 'direction', 'service_key']
finaldf = pd.DataFrame(columns = column_names)
for group in groups:
    group_df = groupby_trip.get_group(group)
    groupby_labels =group_df.groupby(['route_id', 'direction', 'service_key'])
    size=max(groupby_labels.size())
    # Delete all the groups whose size is less than max size
    groupby_labels=groupby_labels.filter(lambda x: len(x) == size, dropna=True)
    finaldf=finaldf.append(groupby_labels, ignore_index = True)

finaldf = finaldf.drop_duplicates()

invalid_trip_id_list = []
    # TRANSFORMATION 4 : Change the value of direction to out and back if its 0 and 1 respectively
for index in range(len(finaldf['direction'])):
    if (pd.isnull(finaldf['direction'][index])):
        finaldf['direction'][index]=''
        invalid_trip_id_list.append(finaldf['trip_id'][index])
        #finaldf = finaldf.drop(finaldf.index[index])
    elif finaldf['direction'][index]=='1':
        finaldf['direction'][index]='Out'
    elif finaldf['direction'][index]=='0':
        finaldf['direction'][index]='Back'
    else:
        finaldf['direction'][index]=''
        invalid_trip_id_list.append(finaldf['trip_id'][index])
print(finaldf.head())

# TRANSFORMATION 5: Change W to Weekday, S to Saturday and U to Sunday
for index in range(len(finaldf['service_key'])):
    if (pd.isnull(finaldf['service_key'][index])):
        finaldf['service_key'][index] == ''
        invalid_trip_id_list.append(finaldf['trip_id'][index])
    if finaldf['service_key'][index]=='W':
        finaldf['service_key'][index]='Weekday'
    elif finaldf['service_key'][index]=='S':
        finaldf['service_key'][index]='Saturday'
    elif finaldf['service_key'][index]=='U':
        finaldf['service_key'][index]='Sunday'
    else:
        finaldf['service_key'][index]=''
        invalid_trip_id_list.append(finaldf['trip_id'][index])

newdf=tripdf.merge(finaldf, on=['trip_id','vehicle_id'], how='left')
newdf = newdf.drop(newdf.columns[[2, 3, 4]], axis=1)
print("NEWDF: \n",newdf.head())