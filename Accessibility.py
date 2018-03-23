##---------------------------------------------------------------------
## Program: Accessibility.py
## Version: 1.0
##
## Author: Nick Joslyn
## Institution: Simpson College
##
## Purpose: Identify average distances between demand nodes and facility nodes
##
##---------------------------------------------------------------------

##=====================================================================
import numpy as np
import time
import pandas as pd

start = time.time()

#Read-in Files
demandNumbersExcel = 'Demands/Demand.txt'
demandFileExcel = 'Demands/DemandString.csv'
supplyNumbersExcel = 'Facilities/AHA_Numbers_Class_Text.txt'
distanceMatrixExcel = 'DistanceMatrix/2017Time.txt'

DemandNumbers = np.genfromtxt(demandNumbersExcel)
DemandInfo = pd.read_csv(demandFileExcel)
SupplyNumbers = np.genfromtxt(supplyNumbersExcel)
DistanceMatrix = np.genfromtxt(distanceMatrixExcel)

numberOptimized = 71
totalDistance = 0
optimalLocations = np.arange(numberOptimized)

numberOfSupplyNodes = SupplyNumbers.shape[0]
numberOfDemandNodes = DemandNumbers.shape[0]

#---------------------------------------------
# Identify list of distances to closest facility

solutionMatrix = np.ndarray(shape = (numberOfDemandNodes, numberOptimized))
demandDistances = np.empty(numberOfDemandNodes)

for i in range(numberOptimized):
    solutionMatrix[:,i] = DistanceMatrix[:,optimalLocations[i]]

for i in range(numberOfDemandNodes):
    closestSupplyLocation = np.amin(solutionMatrix[i,:])
    demandDistances[i] = round(closestSupplyLocation/3600, 5)

#---------------------------------------------
# Identify the indexes corresponding to each region

northeastRegion = ["Connecticut", "Maine", "Massachusetts", "New Hampshire", "Rhode Island", "Vermont", "New Jersey", "New York", "Pennsylvania"]
NEindexes = []
midwestRegion = ["Illinois", "Indiana", "Michigan", "Ohio", "Wisconsin", "Iowa", "Kansas", "Minnesota", "Missouri", "Nebraska", "North Dakota", "South Dakota"]
MWindexes = []
southRegion = ["Delaware", "District of Columbia", "Florida", "Georgia", "Maryland", "North Carolina", "South Carolina", "Virginia", "West Virginia", "Alabama", "Kentucky", "Mississippi", "Tennessee", "Arkansas", "Louisiana", "Oklahoma", "Texas"]
Sindexes = []
westRegion = ["Arizona", "Colorado", "Idaho", "Montana", "Nevada", "New Mexico", "Utah", "Wyoming", "California", "Oregon", "Washington"]
Windexes = []

for i, row in DemandInfo.iterrows():
    if (row[1] in northeastRegion):
        NEindexes.append(i)
    if (row[1] in midwestRegion):
        MWindexes.append(i)
    if (row[1] in southRegion):
        Sindexes.append(i)
    if (row[1] in westRegion):
        Windexes.append(i)

#---------------------------------------------
# Convert raw populations in millions to DS estimates (not millions)

NEConversion = 1/1413
MWConversion = 1/1405
SConversion = 1/1757
WConversion = 1/1784

for location in NEindexes:
    DemandNumbers[location,1] = DemandNumbers[location,1] * NEConversion * 10**6

for location in MWindexes:
    DemandNumbers[location,1] = DemandNumbers[location,1] * MWConversion * 10**6

for location in Sindexes:
    DemandNumbers[location,1] = DemandNumbers[location,1] * SConversion * 10**6

for location in Windexes:
    DemandNumbers[location,1] = DemandNumbers[location,1] * WConversion * 10**6

DemandNumbers[:,1] = DemandNumbers[:,1].round(0)

#---------------------------------------------
# Print National Level Stats
national1 = [0,0]
national2 = [0,0]
national3 = [0,0]
national4 = [0,0]
national5 = [0,0]
counter = 0
for national in demandDistances:
    if (national <= 0.5):
        national1[0] = national1[0] + 1
        national1[1] = national1[1] + DemandNumbers[counter, 1]
    if (0.5 < national <= 1.0):
        national2[0] = national2[0] + 1
        national2[1] = national2[1] + DemandNumbers[counter, 1]
    if (1.0 <= national <= 1.5):
        national3[0] = national3[0] + 1
        national3[1] = national3[1] + DemandNumbers[counter, 1]
    if (1.5 < national <= 2.0):
        national4[0] = national4[0] + 1
        national4[1] = national4[1] + DemandNumbers[counter, 1]
    if (national > 2.0):
        national5[0] = national5[0] + 1
        national5[1] = national5[1] + DemandNumbers[counter, 1]

    counter = counter + 1

#---------------------------------------------
# Print Regional Level Stats




#---------------------------------------------

end = time.time()
print(national1)
print(national2)
print(national3)
print(national4)
print(national5)
#print(demandDistances)
total = 0
for i in range(numberOfDemandNodes):
    total = total + DemandNumbers[i,1]
print(total)
#print(optimalLocations)
print("Wall Time: " + str(round(end-start, 2)) + " seconds")
