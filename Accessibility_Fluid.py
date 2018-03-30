##---------------------------------------------------------------------
## Program: Accessibility_Fluid.py
## Version: 1.0
##
## Author: Nick Joslyn
## Institution: Simpson College
##
## Purpose: Identify average distances between demand nodes and facility nodes
##  Solves for state fluidity metric.
##---------------------------------------------------------------------

##=====================================================================
import numpy as np
import time
import pandas as pd

start = time.time()

#Read-in Files
demandNumbersExcel = '../../Demands/Demand.txt'
demandFileExcel = '../../Demands/DemandString.csv'
supplyNumbersExcel = '../../Facilities/AHA_Numbers_Class_Text.txt'
distanceMatrixExcel = '../../DistanceMatrix/2017Time.txt'

DemandNumbers = np.genfromtxt(demandNumbersExcel)
DemandInfo = pd.read_csv(demandFileExcel, header = None)
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
    elif (row[1] in midwestRegion):
        MWindexes.append(i)
    elif (row[1] in southRegion):
        Sindexes.append(i)
    elif (row[1] in westRegion):
        Windexes.append(i)
    else:
        print("No region for " + str(row))
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
# Northeast:
northeast1 = [0,0]
northeast2 = [0,0]
northeast3 = [0,0]
northeast4 = [0,0]
northeast5 = [0,0]

for index in NEindexes:
    if (demandDistances[index] <= 0.5):
        northeast1[0] = northeast1[0] + 1
        northeast1[1] = northeast1[1] + DemandNumbers[index, 1]
    if (0.5 < demandDistances[index] <= 1.0):
        northeast2[0] = northeast2[0] + 1
        northeast2[1] = northeast2[1] + DemandNumbers[index, 1]
    if (1.0 <= demandDistances[index] <= 1.5):
        northeast3[0] = northeast3[0] + 1
        northeast3[1] = northeast3[1] + DemandNumbers[index, 1]
    if (1.5 < demandDistances[index] <= 2.0):
        northeast4[0] = northeast4[0] + 1
        northeast4[1] = northeast4[1] + DemandNumbers[index, 1]
    if (demandDistances[index] > 2.0):
        northeast5[0] = northeast5[0] + 1
        northeast5[1] = northeast5[1] + DemandNumbers[index, 1]

# Midwest:
midwest1 = [0,0]
midwest2 = [0,0]
midwest3 = [0,0]
midwest4 = [0,0]
midwest5 = [0,0]

for index in MWindexes:
    if (demandDistances[index] <= 0.5):
        midwest1[0] = midwest1[0] + 1
        midwest1[1] = midwest1[1] + DemandNumbers[index, 1]
    if (0.5 < demandDistances[index] <= 1.0):
        midwest2[0] = midwest2[0] + 1
        midwest2[1] = midwest2[1] + DemandNumbers[index, 1]
    if (1.0 <= demandDistances[index] <= 1.5):
        midwest3[0] = midwest3[0] + 1
        midwest3[1] = midwest3[1] + DemandNumbers[index, 1]
    if (1.5 < demandDistances[index] <= 2.0):
        midwest4[0] = midwest4[0] + 1
        midwest4[1] = midwest4[1] + DemandNumbers[index, 1]
    if (demandDistances[index] > 2.0):
        midwest5[0] = midwest5[0] + 1
        midwest5[1] = midwest5[1] + DemandNumbers[index, 1]

# South:
south1 = [0,0]
south2 = [0,0]
south3 = [0,0]
south4 = [0,0]
south5 = [0,0]

for index in Sindexes:
    if (demandDistances[index] <= 0.5):
        south1[0] = south1[0] + 1
        south1[1] = south1[1] + DemandNumbers[index, 1]
    if (0.5 < demandDistances[index] <= 1.0):
        south2[0] = south2[0] + 1
        south2[1] = south2[1] + DemandNumbers[index, 1]
    if (1.0 <= demandDistances[index] <= 1.5):
        south3[0] = south3[0] + 1
        south3[1] = south3[1] + DemandNumbers[index, 1]
    if (1.5 < demandDistances[index] <= 2.0):
        south4[0] = south4[0] + 1
        south4[1] = south4[1] + DemandNumbers[index, 1]
    if (demandDistances[index] > 2.0):
        south5[0] = south5[0] + 1
        south5[1] = south5[1] + DemandNumbers[index, 1]

# West:
west1 = [0,0]
west2 = [0,0]
west3 = [0,0]
west4 = [0,0]
west5 = [0,0]

for index in Windexes:
    if (demandDistances[index] <= 0.5):
        west1[0] = west1[0] + 1
        west1[1] = west1[1] + DemandNumbers[index, 1]
    if (0.5 < demandDistances[index] <= 1.0):
        west2[0] = west2[0] + 1
        west2[1] = west2[1] + DemandNumbers[index, 1]
    if (1.0 <= demandDistances[index] <= 1.5):
        west3[0] = west3[0] + 1
        west3[1] = west3[1] + DemandNumbers[index, 1]
    if (1.5 < demandDistances[index] <= 2.0):
        west4[0] = west4[0] + 1
        west4[1] = west4[1] + DemandNumbers[index, 1]
    if (demandDistances[index] > 2.0):
        west5[0] = west5[0] + 1
        west5[1] = west5[1] + DemandNumbers[index, 1]

#---------------------------------------------
# Identify number of people in each region

# National
totalPeople = 0
for i in range(numberOfDemandNodes):
    totalPeople = totalPeople + DemandNumbers[i,1]

# Northeast
NEpeople = 0
for index in NEindexes:
    NEpeople = NEpeople + DemandNumbers[index,1]

# Midwest
MWpeople = 0
for index in MWindexes:
    MWpeople = MWpeople + DemandNumbers[index,1]

# South
Speople = 0
for index in Sindexes:
    Speople = Speople + DemandNumbers[index,1]

# West
Wpeople = 0
for index in Windexes:
    Wpeople = Wpeople + DemandNumbers[index,1]

#---------------------------------------------
# Print results

end = time.time()

print("Number of Cities: " + str(numberOfDemandNodes))
print("Total People: " + str(totalPeople))
print("National Stats:")
print(national1)
print(national2)
print(national3)
print(national4)
print(national5)
print()

print("Number of Cities in NE: " + str(len(NEindexes)))
print("Number of People in NE: " + str(NEpeople))
print("Northeast Stats:")
print(northeast1)
print(northeast2)
print(northeast3)
print(northeast4)
print(northeast5)
print()

print("Number of Cities in MW: " + str(len(MWindexes)))
print("Number of People in MW: " + str(MWpeople))
print("Midwest Stats:")
print(midwest1)
print(midwest2)
print(midwest3)
print(midwest4)
print(midwest5)
print()

print("Number of Cities in South: " + str(len(Sindexes)))
print("Number of People in South: " + str(Speople))
print("South Stats:")
print(south1)
print(south2)
print(south3)
print(south4)
print(south5)
print()

print("Number of Cities in West: " + str(len(Windexes)))
print("Number of People in West: " + str(Wpeople))
print("West Stats:")
print(west1)
print(west2)
print(west3)
print(west4)
print(west5)
print()


#print(optimalLocations)
print("Wall Time: " + str(round(end-start, 2)) + " seconds")
