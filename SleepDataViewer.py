# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 09:59:05 2022
Updated on Mon Aug  7 13:22:00 2023
@author: luc-girod
"""


folder='DataExport20240313'
filepath = folder + "/Lea_sleep.csv"

# Cleanup the file (comments break the csv structure)

import re


# – Define our search and replace
s1 = "\n"
r1 = ""
s2 = r'"Lea",'
r2 = r'\n"Lea",'
s3 = r'","'
r3 = r'XXXXXXXXXXXXXXXXXX'
s4 = r','
r4 = r''
s5 = r'XXXXXXXXXXXXXXXXXX'
r5 = r'","'
s6 = r'\nLea","'
r6 = r'"\n"Lea","'
s7 = r'Baby.*Note'
r7 = r'Baby,Time,Duration (min),Note'
s8 = r',"\Z'
r8 = r',""'


#In file, replace:
# \n by nothing
# "Lea", by \n"Lea",
# "," by XXXXXXXXXXXXXXXXXX
# , by nothing
# XXXXXXXXXXXXXXXXXX by ","
# \nLea"," by "\n"Lea","
# add " on the last line



# – Get our input and output files
output_file1 = folder + "/Lea_sleep_clean1.csv"
output_file2 = folder + "/Lea_sleep_clean2.csv"
output_file =  folder + "/Lea_sleep_clean.csv"

# – Write the file with the replacement values
with open(filepath, 'r') as read_stream:
    with open(output_file1, 'w') as write_stream:
        # – Use a regex to do the substitution as that is very quick
        regex = re.compile(s1)
        write_stream.write(regex.sub(r1, read_stream.read()))

with open(output_file1, 'r') as read_stream:
    with open(output_file2, 'w') as write_stream:        
        regex = re.compile(s2)
        write_stream.write(regex.sub(r2, read_stream.read()))

with open(output_file2, 'r') as read_stream:
    with open(output_file1, 'w') as write_stream:
        # – Use a regex to do the substitution as that is very quick
        regex = re.compile(s3)
        write_stream.write(regex.sub(r3, read_stream.read()))

with open(output_file1, 'r') as read_stream:
    with open(output_file2, 'w') as write_stream:        
        regex = re.compile(s4)
        write_stream.write(regex.sub(r4, read_stream.read()))

with open(output_file2, 'r') as read_stream:
    with open(output_file1, 'w') as write_stream:
        # – Use a regex to do the substitution as that is very quick
        regex = re.compile(s5)
        write_stream.write(regex.sub(r5, read_stream.read()))

with open(output_file1, 'r') as read_stream:
    with open(output_file2, 'w') as write_stream:        
        regex = re.compile(s6)
        write_stream.write(regex.sub(r6, read_stream.read()))

with open(output_file2, 'r') as read_stream:
    with open(output_file1, 'w') as write_stream:
        # – Use a regex to do the substitution as that is very quick
        regex = re.compile(s7)
        write_stream.write(regex.sub(r7, read_stream.read()))

with open(output_file1, 'r') as read_stream:
    with open(output_file, 'w') as write_stream:        
        regex = re.compile(s8)
        write_stream.write(regex.sub(r8, read_stream.read()))

# f = open(output_file, "a+")
# f.write(r'"')
# f.close()




import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_rows', 500)
pd.options.mode.chained_assignment = None


SleepData = pd.read_csv(output_file)
SleepData["Time"] = pd.to_datetime(SleepData["Time"])
# Anonimize data by placing birth at 2000-01-01
Birthday=SleepData.Time.dt.date[0]
SleepData.Time=SleepData.Time - pd.Timestamp(Birthday)
SleepData.Time=pd.Timestamp("2000-01-01 00:00:00")+SleepData.Time
SleepData.set_index('Time',inplace=True)

# Convert to hours
SleepData["Duration"]=SleepData["Duration (min)"]/60

#Crop time slice Anon
# 1st year
SleepDataSlice=SleepData['20000101':'20001231']
filename_time='_1y_0-12'
# 2nd year
SleepDataSlice=SleepData['20010101':'20011231'] 
filename_time='_1y_13-24'
# 1st 6m
SleepDataSlice=SleepData['20000101':'20000630'] 
filename_time='_6m_0-6'
# 2nd 6m
SleepDataSlice=SleepData['20000701':'20001231'] 
filename_time='_6m_7-12'
# 3rd 6m
SleepDataSlice=SleepData['20010101':'20010630'] 
filename_time='_6m_13-18'
# 4th 6m
SleepDataSlice=SleepData['20010701':'20011231'] 
filename_time='_6m_19-24'
# 2 years
SleepDataSlice=SleepData['20000101':'20011231'] 
filename_time='_2y_0-24'

# Separate daytime naps and night sleep, assign all night periods to same day (end of night day)
SleepDataNap=SleepDataSlice.between_time('08:00','18:30').reset_index()
SleepDataNight=SleepDataSlice.between_time('18:30','08:00').reset_index()
SleepDataNight.Time=SleepDataNight.Time + pd.Timedelta(hours=12)

# Plot all duration data
PlotScatter=SleepDataNap.plot(x='Time', y="Duration",kind='scatter', fontsize=12, figsize=(15,6),ylim=(0, 14))
SleepDataNight.plot(ax=PlotScatter, x='Time',y="Duration",kind='scatter', fontsize=12, figsize=(15,6), c='r')
PlotScatter.legend(['Naps (start of sleep between 08:00-18:30)','Night (start of sleep between 18:30-08:00)'],loc='upper left')
PlotScatter.figure.savefig('SleepRecord'+filename_time+'.png')


# Count naps and night sections
NbDailyNaps=SleepDataNap.groupby(SleepDataNap.Time.dt.date)['Duration'].count().reset_index()
NbDailyNaps['RollingAvg14d'] = NbDailyNaps['Duration'].rolling(14).mean()
NbDailyNight=SleepDataNight.groupby(SleepDataNight.Time.dt.date)['Duration'].count().reset_index()
NbDailyNight.Duration=NbDailyNight.Duration-1
NbDailyNight['RollingAvg14d'] = NbDailyNight['Duration'].rolling(14).mean()



# Plot count of daily naps
PlotLine=NbDailyNaps.plot(x='Time',y="Duration",kind='scatter', fontsize=12, figsize=(15,6), c='r', alpha=0.1)
NbDailyNaps.plot(ax=PlotLine, x='Time',y="RollingAvg14d",kind='line', fontsize=12, figsize=(15,6), c='r',
xlabel="Date",ylabel="Count")
PlotLine.legend(['Number of daily Naps (start of sleep between 08:00-18:30)','14d moving average'])
PlotLine.figure.savefig('SleepRecord_NbNapsSections.png')

# Plot count of daily night wake-ups
PlotLine=NbDailyNight.plot(x='Time',y="Duration",kind='scatter', fontsize=12, figsize=(15,6), c='b', alpha=0.1)
NbDailyNight.plot(ax=PlotLine, x='Time',y="RollingAvg14d",kind='line', fontsize=12, figsize=(15,6), c='b',
xlabel="Date",ylabel="Count")
PlotLine.legend(['Number of daily Night wake-ups (between 18:30-08:00)','14d moving average'])
PlotLine.figure.savefig('SleepRecord_NbNightSections.png')

# Plot count of both
PlotLine=NbDailyNaps.plot(x='Time',y="Duration",kind='scatter', fontsize=12, figsize=(15,6), c='r', alpha=0.1)
NbDailyNaps.plot(ax=PlotLine, x='Time',y="RollingAvg14d",kind='line', fontsize=12, figsize=(15,6), c='r')
NbDailyNight.plot(ax=PlotLine, x='Time',y="Duration",kind='scatter', fontsize=12, figsize=(15,6), c='b', alpha=0.1)
NbDailyNight.plot(ax=PlotLine, x='Time',y="RollingAvg14d",kind='line', fontsize=12, figsize=(15,6), c='b',
xlabel="Date",ylabel="Count")
PlotLine.legend(['Number of daily Naps (start of sleep between 08:00-18:30)','14d moving average','Number of daily Night wake-ups (between 18:30-08:00)','14d moving average'])
PlotLine.figure.savefig('SleepRecord_Nb_Naps_NightSections.png')


# plot single months example
SleepDataNightSeptember = SleepDataNight[SleepDataNight['Time'].dt.month == 9]
SleepDataNightFebruary  = SleepDataNight[SleepDataNight['Time'].dt.month == 2]
plt.figure()
SleepDataNightSeptember["Duration"].hist(bins=12)
plt.savefig('September.png')
plt.figure()
SleepDataNightFebruary["Duration"].hist(bins=12)
plt.savefig('February.png')


#Plot sleep start time vs length
SleepDataNightNoDate=SleepDataNight.copy(deep=True)
SleepDataNightNoDate["Timeh"]=pd.Timedelta(days=1)
for i in range(0,len(SleepDataNightNoDate)):
    SleepDataNightNoDate["Timeh"][i]=SleepDataNightNoDate.Time[i] - pd.Timestamp(SleepDataNightNoDate.Time.dt.date[i])
SleepDataNightNoDate.Timeh=pd.Timestamp("2000-01-01 00:00:00")+SleepDataNightNoDate.Timeh

#Create line for "wakeup at 7am"
line7am=SleepDataNightNoDate[0:2].copy(deep=True)
line7am.Duration[0]=12.5
line7am.Duration[1]=0
line7am.Timeh[0]=pd.Timestamp('2000-01-01 06:30:00')
line7am.Timeh[1]=pd.Timestamp('2000-01-01 19:00:00')
#Create line for "wakeup at 5am"
line5am=SleepDataNightNoDate[0:2].copy(deep=True)
line5am.Duration[0]=10.5
line5am.Duration[1]=0
line5am.Timeh[0]=pd.Timestamp('2000-01-01 06:30:00')
line5am.Timeh[1]=pd.Timestamp('2000-01-01 17:00:00')


PlotScatter=SleepDataNightNoDate.plot(x='Timeh', y="Duration",kind='scatter', fontsize=12, figsize=(15,6),
c='Time',cmap='cool')
xtl=[item.get_text()[6:] for item in PlotScatter.get_xticklabels()]
PlotScatter.set_xticklabels(['18:00', '20:00', '22:00', '00:00', '02:00', '04:00', '06:00', '08:00'])
line5am.plot(ax=PlotScatter, x='Timeh',y="Duration",kind='line', fontsize=12, figsize=(15,6), c='r', alpha=1)
line7am.plot(ax=PlotScatter, x='Timeh',y="Duration",kind='line', fontsize=12, figsize=(15,6), c='b', alpha=1,
xlabel="Start of sleep time",ylabel="Sleep duration")
PlotScatter.legend(['','Woke up at 05:00','Woke up at 07:00'])
plt.savefig('SleepRecord_NightSectionDuration.png')



#Diaper
#DiaperData = pd.read_csv("DataExport2023-08-07/Lea_diaper.csv")
#DiaperData["Time"] = pd.to_datetime(DiaperData["Time"])
#DiaperData.set_index('Time',inplace=True)
## Separate wet/poop/mixed
#DiaperDataWet=DiaperData[DiaperData.Status=="Wet"]
#DiaperDataDirty=DiaperData[DiaperData.Status=="Dirty"]
#DiaperDataMixed=DiaperData[DiaperData.Status=="Mixed"]
#DiaperDataDaily=DiaperData.groupby(DiaperData.index.date).count().reset_index()
#DiaperDataWetDaily=DiaperDataWet.groupby(DiaperDataWet.index.date).count().reset_index()
#DiaperDataDirtyDaily=DiaperDataDirty.groupby(DiaperDataDirty.index.date).count().reset_index()
#DiaperDataMixedDaily=DiaperDataMixed.groupby(DiaperDataMixed.index.date).count().reset_index()
#plt.figure(figsize=(15,6))
#plt.plot(DiaperDataDaily["index"],DiaperDataDaily["Baby"])
#plt.plot(DiaperDataWetDaily["index"],DiaperDataWetDaily["Baby"])
#plt.plot(DiaperDataDirtyDaily["index"],DiaperDataDirtyDaily["Baby"])
#plt.plot(DiaperDataMixedDaily["index"],DiaperDataMixedDaily["Baby"])
#plt.legend(['All','Wet','Dirty','Mixed'])
#plt.savefig('DiaperRecord.png')


if():
    #Crop time slice Lea
    #SleepData=SleepData['20220312':'20230313'] # Lea's 1st year
    #SleepData=SleepData['20220312':'20220913'] # Lea's 1st 6m
    #SleepData=SleepData['20220914':'20230313'] # Lea's 2nd 6m
    #SleepData=SleepData['20230313':'20240313'] # Lea's 2nd year
    #SleepData=SleepData['20230314':'20230913'] # Lea's 3rd 6m
    #SleepData=SleepData['20230914':'20240313'] # Lea's 4th 6m