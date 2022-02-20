import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.windfinder.com/weatherforecast/salzgittersee')

if r.status_code != 200:
    print("error while getting weather data")

windArray = [] #stores all wind data in pairs of two, starting from min
rainArray = [] #stores all rain data
minWind = 14 #minimal amount of wind (kts)
maxWind = 30 #maximal amount of wind (kts)
maxRain = 0 #maximal amount of rain (mm/h)
minHours = 1 #minimal amount of hours in which the conditions are met
minTime = 6 #time from which one can sail
maxTime = 21 #time to which one can sail

pulled = r.content.decode("utf-8")
soup = BeautifulSoup(r.content, 'html.parser')
s = soup.select("div.weathertable__body > div:nth-of-type(8)")

for index, wind in zip(range(48), soup.select("span.units-ws")) :
    windArray.append(float(wind.text))

for index, rain in zip(range(24), soup.select("div.data-rain")) :
    if(rain.find("span")) != None:
        rainArray.append(float(rain.select('span')[0].text))
    else:
        rainArray.append(0)

singleSteps = 0
countHour = 23
for x in range(0, 48, 2):
    if windArray[x] >= minWind and windArray[x+1] <= maxWind and rainArray[singleSteps] <= maxRain and countHour+1 >= minTime and countHour+1 <= maxTime:
        if countHour >= minHours:
            print("go sail!", countHour+1)
    else:
        print("dont go sail", countHour+1)

    if singleSteps >= 0:
        countHour = singleSteps
    singleSteps = singleSteps+1

with open('scapes.txt', 'w') as f:
    f.write(str(windArray) + str(rainArray))