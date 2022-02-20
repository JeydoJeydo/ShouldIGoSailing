import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.windfinder.com/forecast/salzgittersee')
print(r)
pulled = r.content.decode("utf-8")
soup = BeautifulSoup(r.content, 'html.parser')
s = soup.find('div', class_='fc-day-index-1')

with open('scapes.txt', 'w') as f:
    f.write(str(s))