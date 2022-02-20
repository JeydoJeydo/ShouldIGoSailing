import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.windfinder.com/weatherforecast/salzgittersee')
print(r)
pulled = r.content.decode("utf-8")
soup = BeautifulSoup(r.content, 'html.parser')
#s = soup.findAll('div', class_='weathertable__body')
s = soup.select("div.weathertable__body > div:nth-of-type(8)")

print("Min and Max Wind")
for wind in soup.select("span.units-ws"):
    print(wind.text) #prints min and max wind variables

print("Rain")
for rain in soup.select("div.data-rain"):
    #print(rain.select('span'))

    if(rain.find("span")) != None:
        print(rain.select('span')[0].text)
    else:
        print(0)

#for div in s:
#    test = div.findAll('span')
#    print(test)
#    finalStr+=str(test)
    
#print(finalStr[finalStr.find('>')+1 : finalStr.find('</')])

with open('scapes.txt', 'w') as f:
    f.write(str(s))