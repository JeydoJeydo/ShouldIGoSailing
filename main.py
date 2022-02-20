import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.windfinder.com/weatherforecast/salzgittersee')
print(r)
pulled = r.content.decode("utf-8")
soup = BeautifulSoup(r.content, 'html.parser')
#s = soup.findAll('div', class_='weathertable__body')
s = soup.select("div.weathertable__body > div:nth-of-type(8)")

for weather in s.findAll('span'):
    print(weather)

with open('scapes.txt', 'w') as f:
    f.write(str(s))