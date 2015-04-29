# -*- coding: utf-8 -*
"""
Created 20140520

@author: G. Kettlewell

Plot sensor data for Sandpit noise tests
"""

#import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime as dt
import sys

sys.path.append('c:/PythonScripts')

from DatabaseManipulation import ReadDatabase, LoadData, ConvertToDateTime, CalculateNoise, CalculateDelta

basePath = 'c:/users/grahamk/Dropbox/OooftiData/'
#database = basePath + 'Sandpit/141014/Database/141014.db'
database = basePath + 'Eddy/1409_UoWAir/Database/1409_UoWAir.db'
#database = basePath + 'B1Darwin/1407_Darwin/Database/1407_Darwin.db'

startDate = '2015-02-02 17:00'
finishDate = '2015-02-05 24:00'

#startDate = '2014-06-10 16:00'
#finishDate = '2014-12-31 24:00'

selectSTR = 'SELECT Collection_Start_Time FROM sysvariables where Collection_Start_Time between '
selectSTR += chr(39) + startDate + chr(39) + ' and ' + chr(39) +  finishDate + chr(39)
selectSTR += ' and Inlet = ' + chr(39) + 'Inlet_1' + chr(39)
selectSTR += ' and Cell_Temperature_Avg > 29'
selectSTR += ' and CV_del13C_cal_a != ' + chr(39)  + chr(39)
selectSTR += ' and CV_del13C_cal_e != ' + chr(39)  + chr(39)
selectSTR += ' and Flow_In_Avg > 0.45'

averagingPeriod = 3

rows = ReadDatabase(database, selectSTR)

dates = ConvertToDateTime(rows, 0)
temperature = LoadData(rows, 1)
CO2 = LoadData(rows, 2)
CO2_12 = LoadData(rows, 3)
CO2_13 = LoadData(rows, 4)
del13C = LoadData(rows, 5)

temperatureNoise = CalculateNoise(temperature, averagingPeriod)
CO2Noise = CalculateNoise(CO2, averagingPeriod)
CO2_12Noise = CalculateNoise(CO2_12, averagingPeriod)
CO2_13Noise = CalculateNoise(CO2_13, averagingPeriod)
del13CNoise = CalculateNoise(del13C, averagingPeriod)

temperatureDelta = CalculateDelta(temperature)


# Create a figure with the sensor data.
serial_time = mpl.dates.date2num(dates)

fig = plt.figure('Scatter around running means')
suptitleSTR = 'Scatter around running means\n'
suptitleSTR += database + '\n' + str(dates[0]) + ' to ' + str(dates[len(dates) -1])
fig.suptitle(suptitleSTR, fontsize=14, fontweight='bold')
fig.subplots_adjust(hspace=0.1)

Ax1 = fig.add_subplot(411)
Ax1.scatter(dates, temperature)
Ax1.set_ylabel("Cell temperature")
Ax1.grid(True)

Ax2 = fig.add_subplot(412, sharex=Ax1)
Ax2.scatter(dates[:len(temperatureNoise)], temperatureNoise, marker='+')
Ax2.yaxis.tick_right()
Ax2.yaxis.set_label_position("right")
Ax2.set_ylabel('Cell temp noise ($^\circ$C)')
Ax2.grid(True)

Ax3 = fig.add_subplot(413, sharex=Ax1)
Ax3.scatter(dates[:len(CO2Noise)], CO2Noise, marker='+', c='b', label='CO2')
Ax3.scatter(dates[:len(CO2_12Noise)], CO2_12Noise, marker='+', c='r', label='12CO2')
Ax3.scatter(dates[:len(CO2_12Noise)], CO2_13Noise, marker='+', c='g', label='13CO2')
Ax3.set_ylabel('CO2 noise (ppm)')
Ax3.legend(loc=2,ncol=1)
Ax3.grid(True)

Ax4 = fig.add_subplot(414, sharex=Ax1)
Ax4.scatter(dates[:len(del13CNoise)], del13CNoise, marker='+')
Ax4.yaxis.tick_right()
Ax4.yaxis.set_label_position("right")
Ax4.set_ylabel('Del13C noise (0/00)')
Ax4.grid(True)

# Set x axis range
t0 = dates[0] - dt.timedelta(0,3600)
t1= dates[len(dates) -1 ] + dt.timedelta(0,3600)
Ax4.set_xlim(t0,t1)
fig.autofmt_xdate()

fig2 = plt.figure('xCO2 noise Vs Temperature noise')
suptitleSTR = '13CO2 noise Vs Temperature noise\n'
fig2.suptitle(suptitleSTR, fontsize=14, fontweight='bold')
fig2.subplots_adjust(hspace=0.1)
'''
Ax5 = fig2.add_subplot(111)
Ax5.scatter(temperatureNoise, CO2Noise)
Ax5.set_xlabel('Temperature noise ($^\circ$C)')
Ax5.set_ylabel('CO2 noise (ppm)')

Ax5 = fig2.add_subplot(111)
Ax5.scatter(temperatureNoise, CO2_12Noise)
Ax5.set_xlabel('Temperature noise ($^\circ$C)')
Ax5.set_ylabel('12CO2 noise (ppm)')
'''
Ax5 = fig2.add_subplot(111)
Ax5.scatter(temperatureNoise, CO2_13Noise)
Ax5.set_xlabel('Temperature noise ($^\circ$C)')
Ax5.set_ylabel('13CO2 noise (ppm)')



Ax5.grid(True)

plt.show()
