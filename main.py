import pandas as pd
import matplotlib.pyplot as plt


# Uses linear projection to identify what the total GHG emissions will be in the given year


#Data retevied from [Climate Watch 2021. Washington, DC: World Resources Institute. Available online at: https://www.climatewatchdata.org.]
df = pd.read_excel("climatewatch-usemissions.xlsx")
colGHG = "Unnamed: 2"
emissionsVal2018 = df[colGHG][1459:] 
avgChangeDict = {}
statesDict = {}

#Getts all the states and puts them into a dictionary for later use
def getStateData():
    statesData = df["Climate Watch - U.S States Greenhouse Gas Emissions"]

    for i in statesData[3:]:
        if i not in avgChangeDict.keys():
            avgChangeDict[i] = 0
            statesDict[i] = 0

#Literally just fill up the dict with states
def populateStatesDict():
    cont = 1459
    for state in statesDict.keys():
        statesDict[state] = emissionsVal2018[cont]
        cont += 1

#get avg rate of change (Hard coded and trash)
def avgRateOfChange():
    yearRange = max(df["Unnamed: 1"][3:]) - min(df["Unnamed: 1"][3:])

    val2018 = df[colGHG][1459:]
    val1990 = df[colGHG][3:55]

    cont = 1459
    for val in val1990:
        val2018[cont] -= val
        cont += 1

    avgChange = [i/yearRange for i in val2018]
    
    cont = 0
    for state in avgChangeDict.keys():
        avgChangeDict[state] = avgChange[cont]
        cont += 1
    
#gets the value for the furute using linear projection
def extrapolate(state, year):
    constant = -((1990 * avgChangeDict[state]) - statesDict[state])
    equationVal = avgChangeDict[state] * year + constant
    return equationVal  

#use usr input to return a readable sentance
def translateInput(input, curYear):
    split = input.split(" ")
    state = split[0]
    year = int(split[1])

    if state in statesDict.keys():
        value = extrapolate(state, year)

        print(f"{state} will have {value} Metric Tons Of CO2 Equivalent Total of GHG Emissions Excluding LUCF")
    else:
        print("Bad Input, silly goose. Run Program again lmao")

if __name__ == '__main__':
    getStateData()
    populateStatesDict()
    avgRateOfChange()
 
    cYear = int(input("Current Year (Ex: '2021')"))
    usrInp = input("Enter state and year to predict GHG emissions excluding LUCF (Ex: 'Alabama 2030')")
    translateInput(usrInp, cYear)