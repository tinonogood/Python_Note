
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. This is the dataset to use for this assignment. Note: The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.


import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import numpy as np
import matplotlib.dates as mdates

def read_df():
    
#     Date organize

    df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
    df_max = df[df['Element'] == 'TMAX']
    
    df[['year','date']] = df['Date'].str.split("-", n=1, expand=True)

    df['year'] = df['year'].astype(int)
    df['Data_Value'] = df['Data_Value'] / 10
    df['year'] = df['year'].astype(int) 
    df_bf_2015 = df[df['year'] < 2015] 
    df_2015 = df[df['year'] == 2015] 
    
    
    df_bf_2015_max = df_bf_2015[df_bf_2015['Element'] == 'TMAX'][['date','Data_Value']]
    df_bf_2015_max[['Month','Date']] = df_bf_2015_max['date'].str.split("-", n=1, expand=True)
    df_bf_2015_max = df_bf_2015_max.groupby(['Month','Date'])['Data_Value'].agg(max)
    df_bf_2015_max = df_bf_2015_max.reset_index(level=[0,1])
    df_bf_2015_max.rename(columns={"Data_Value": "05-14_Max"},inplace=True)
    
    df_bf_2015_min = df_bf_2015[df_bf_2015['Element'] == 'TMIN'][['date','Data_Value']]
    df_bf_2015_min[['Month','Date']] = df_bf_2015_min['date'].str.split("-", n=1, expand=True)
    df_bf_2015_min = df_bf_2015_min.groupby(['Month','Date'])['Data_Value'].agg(min)
    df_bf_2015_min = df_bf_2015_min.reset_index(level=[0,1])
    df_bf_2015_min.rename(columns={"Data_Value": "05-14_Min"},inplace=True)
    
    
    df_2015_max= df_2015[df_2015['Element'] == 'TMAX'][['date','Data_Value']]
    df_2015_max[['Month','Date']] = df_2015_max['date'].str.split("-", n=1, expand=True)
    df_2015_max = df_2015_max.groupby(['Month','Date'])['Data_Value'].agg(max)
    df_2015_max = df_2015_max.reset_index(level=[0,1])
    df_2015_max.rename(columns={"Data_Value": "15_Max"},inplace=True)
    
    df_2015_min= df_2015[df_2015['Element'] == 'TMIN'][['date','Data_Value']]
    df_2015_min[['Month','Date']] = df_2015_min['date'].str.split("-", n=1, expand=True)
    df_2015_min = df_2015_min.groupby(['Month','Date'])['Data_Value'].agg(min)
    df_2015_min = df_2015_min.reset_index(level=[0,1])
    df_2015_min.rename(columns={"Data_Value": "15_Min"},inplace=True)
    
    df = df_2015_max.merge(df_2015_min, how='inner',left_on=['Month','Date'], right_on=['Month','Date'])
    df = df.merge(df_bf_2015_max, how='inner',left_on=['Month','Date'], right_on=['Month','Date'])
    df = df.merge(df_bf_2015_min, how='inner',left_on=['Month','Date'], right_on=['Month','Date'])
    df['Date'] = df['Month'] + "/" + df['Date']
    
    
    df['15_Max'] = np.where((df['15_Max'] > df['05-14_Max']),df['15_Max'],np.nan)
    df['15_Min'] = np.where((df['15_Min'] < df['05-14_Min']),df['15_Min'],np.nan)
    
    return df


  
    
#     Chart display
get_ipython().magic('matplotlib inline')

df = read_df() 

#observation_dates = np.arange('2015-01-01','2016-01-01',dtype='datetime64[D]')
#observation_dates = list(map(pd.to_datetime,observation_dates))

y1 = df['05-14_Max']
y2 = df['05-14_Min']
y3 = df['15_Max']
y4 = df['15_Min']


plt.figure()
plt.plot(y1 , '-k', y2 , '-k', y3 , 'ro', y4 , 'bo')

ax = plt.gca()
ax.fill_between(range(len(y1)), y1, y2, facecolor = 'black', alpha = 0.1)
ax.set_xlabel('Day')
ax.set_ylabel('Temperture (Celsius)')
ax.set_title('Weather Patterns: 2015 Record Breaking vs. 2005-2014 Historic Temperature')
ax.legend(['Historic temperature','2005-2014','2015 record breaking High', '2015 record breaking low'])




