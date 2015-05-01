# -*- coding: utf-8 -*
"""
Created 20140520

@author: G. Kettlewell

Plot sensor data for noise tests
"""

#import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys

sys.path.append('c:/PythonScripts')

from DatabaseManipulation import NumTables, ReadDatabase, LoadData, ConvertToDateTime, CalculateNoise, CalculateDelta
from PlottingTools import DrawHist

basePath = 'c:/users/grahamk/Dropbox/OooftiData/'
#database = basePath + 'Sandpit/141014/Database/141014.db'
database = basePath + 'Eddy/1409_UoWAir/Database/1409_UoWAir.db'
#database = basePath + 'Eddy/1504_UoWAir/Database/1504_UoWAir.db'
#database = basePath + 'B1Darwin/1407_Darwin/Database/1407_Darwin.db'

''' Pre the increase in noise on Eddy '''
#startDate = '2015-01-30 00:00'
#finishDate = '2015-02-03 00:00'

''' Post the increase in noise on Eddy '''
startDate = '2015-02-04 05:00'
finishDate = '2015-02-08 05:05'

''' Post the laser change on Eddy '''
#startDate = '2015-04-26 00:00'
#finishDate = '2015-04-29 24:00'

averagingPeriod = 3


if (NumTables(database) < 3):

    selectSTR = 'SELECT Collection_Start_Time, Cell_Temperature_Avg, CO2, CO2_1,CO2_2,CV_del13C '
    selectSTR += 'FROM sysvariables where Collection_Start_Time between '
    selectSTR += chr(39) + startDate + chr(39) + ' and ' + chr(39) +  finishDate + chr(39)

    fullData = ReadDatabase(database, selectSTR)
else:
    # It is the new database with multiple tables.

    # Primary key and date/time from sysvariables
    selectSTR = 'SELECT  sysvariablesPK, Collection_Start_Time FROM sysvariables where Collection_Start_Time between '
    selectSTR += chr(39) + startDate + chr(39) + ' and ' + chr(39) +  finishDate + chr(39)
    rows1 = ReadDatabase(database, selectSTR)
    sysvariablesPK = LoadData(rows1, 0)

    readStartPos = str(sysvariablesPK[0])
    readFinishPos = str(sysvariablesPK[len(sysvariablesPK) -1])

    # AI averages
    selectSTR = 'SELECT Cell_Temperature_Avg FROM aiaverages where aiaveragesID between '
    selectSTR += readStartPos + ' and ' + readFinishPos
    rows2 = ReadDatabase(database, selectSTR)

    # Uncorrected species.
    selectSTR = 'SELECT CO2, CO2_1, CO2_2 FROM analysisprimary '
    selectSTR += 'where analysisprimaryID between ' + readStartPos + ' and ' + readFinishPos
    rows3 = ReadDatabase(database, selectSTR)

     # Calculated vals
    selectSTR = 'SELECT CV_del13C FROM calcvals where calcvalsID between ' + readStartPos + ' and ' + readFinishPos
    rows4 = ReadDatabase(database, selectSTR)

    # Assemble all data into a single list
    fullData = []
    for i in range(0, len(rows1) -1):
        tmpRows1 = rows1[i]
        fullData.append(tmpRows1[1:] + rows2[i] + rows3[i] + rows4[i])

# Filter out lines that don't have all the data
filteredData = []
for row in fullData:
    if (str(row).find('None') == -1):
        filteredData.append(row)

dates = ConvertToDateTime(filteredData, 0)
temperature = LoadData(filteredData, 1)
CO2 = LoadData(filteredData, 2)
CO2_12 = LoadData(filteredData, 3)
CO2_13 = LoadData(filteredData, 4)
del13C = LoadData(filteredData, 5)



temperatureNoise = CalculateNoise(temperature, averagingPeriod)
CO2Noise = CalculateNoise(CO2, averagingPeriod)
CO2_12Noise = CalculateNoise(CO2_12, averagingPeriod)
CO2_13Noise = CalculateNoise(CO2_13, averagingPeriod)
del13CNoise = CalculateNoise(del13C, averagingPeriod)

temperatureDelta = CalculateDelta(temperature)


# Create a figure with the sensor data.
serial_time = mpl.dates.date2num(dates)
'''
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
'''
numBins = 300

fig2 = plt.figure('Temperature, xCO2 Del13C Noise Histograms')
suptitleSTR = 'Temperature noise\n'
suptitleSTR += database + '\n' + str(dates[0]) + ' to ' + str(dates[len(dates) -1])
suptitleSTR += '\n ' + str(len(dates)) + ' data points'
fig2.suptitle(suptitleSTR, fontsize=14, fontweight='bold')
fig2.subplots_adjust(hspace=0.3)

DrawHist(fig2, 321, temperatureNoise, numBins, 'Temperature u"\u2103"', -0.02, 0.02)
share_ax = DrawHist(fig2, 322, CO2Noise, numBins, 'CO2 noise (ppm)')
DrawHist(fig2, 323, CO2_12Noise, numBins, '12CO2 noise (ppm)', 'NA', 'NA', 'NA', 'NA', share_ax)
DrawHist(fig2, 324, CO2_13Noise, numBins, '13CO2 noise (ppm)', -4, 4, 'NA', 'NA', share_ax)
DrawHist(fig2, 325, del13CNoise, numBins, 'Del13C noise (ppm)', -1, 1)

'''
fig2 = plt.figure('xCO2 noise Vs Temperature noise')
suptitleSTR = '13CO2 noise Vs Temperature noise\n'
fig2.suptitle(suptitleSTR, fontsize=14, fontweight='bold')
fig2.subplots_adjust(hspace=0.1)

Ax5 = fig2.add_subplot(111)
Ax5.scatter(temperatureNoise, CO2Noise)
Ax5.set_xlabel('Temperature noise ($^\circ$C)')
Ax5.set_ylabel('CO2 noise (ppm)')

Ax5 = fig2.add_subplot(111)
Ax5.scatter(temperatureNoise, CO2_12Noise)
Ax5.set_xlabel('Temperature noise ($^\circ$C)')
Ax5.set_ylabel('12CO2 noise (ppm)')

Ax5 = fig2.add_subplot(111)
Ax5.scatter(temperatureNoise, CO2_13Noise)
Ax5.set_xlabel('Temperature noise ($^\circ$C)')
Ax5.set_ylabel('13CO2 noise (ppm)')
'''


#Ax5.grid(True)

plt.show()
