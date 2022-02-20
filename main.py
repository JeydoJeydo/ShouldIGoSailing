import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.windfinder.com/weatherforecast/salzgittersee')

if r.status_code != 200:
    print("error while getting weather data")

weatherArray = []
rainArray = []
minWind = 14
maxWind = 30
maxRain = 0

pulled = r.content.decode("utf-8")
soup = BeautifulSoup(r.content, 'html.parser')
s = soup.select("div.weathertable__body > div:nth-of-type(8)")

#print(soup.select("h3.weathertable__headline")[0].text)
print("Min and Max Wind")
for index, wind in zip(range(48), soup.select("span.units-ws")) :
    print(wind.text) #prints min and max wind variables
    weatherArray.append(float(wind.text))

print("Rain")
for index, rain in zip(range(24), soup.select("div.data-rain")) :
    if(rain.find("span")) != None:
        print(rain.select('span')[0].text)
        rainArray.append(float(rain.select('span')[0].text))
    else:
        print(0)
        rainArray.append(0)

rainStep = 0
for x in range(0, 48, 2):
    #print(weatherArray[x], weatherArray[x+1])
    if weatherArray[x] >= minWind and weatherArray[x+1] <= maxWind and rainArray[rainStep] <= maxRain:
        print("go sail!")
    else:
        print("dont go sail")

    rainStep = rainStep+1

with open('scapes.txt', 'w') as f:
    f.write(str(weatherArray) + str(rainArray))