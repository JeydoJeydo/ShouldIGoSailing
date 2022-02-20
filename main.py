import keys # remove line,private smtp credentials are stored there
import requests
from bs4 import BeautifulSoup
import smtplib

url = requests.get('https://www.windfinder.com/weatherforecast/salzgittersee')

if url.status_code != 200:
    print("error while getting weather data")

windArray = [] #stores all wind data in pairs of two, starting from min
rainArray = [] #stores all rain data
minWind = 14 #minimal amount of wind (kts)
maxWind = 30 #maximal amount of wind (kts)
maxRain = 0 #maximal amount of rain (mm/h)
minHours = 1 #minimal amount of hours in which the conditions are met
minTime = 6 #time from which one can sail
maxTime = 21 #time to which one can sail

def sendEmail():
    emailSender = keys.emailSenderOwn #put your own credentials here
    emailReceiver = keys.emailReceiverOwn #put your own credentials here
    emailPassword = keys.emailPasswordOwn #put your own credentials here

    smtp_server = smtplib.SMTP(keys.emailServerOwn, 587)
    smtp_server.ehlo()
    smtp_server.starttls()
    smtp_server.ehlo()
    smtp_server.login(emailSender, emailPassword)
    msg_to_send="""From: Siling reminder <{emailFrom}>\nTo: <{emailReceiver}>\nSubject: You should go siling today\nThe Wind is perfect at {weatherTime}\nHave fun!""".format(emailFrom = emailSender, emailReceiver = emailReceiver, weatherTime = sailingPossibilitys)
    print(msg_to_send)
    smtp_server.sendmail(emailSender, emailReceiver, msg_to_send)
    smtp_server.quit()
    print("email send")

pulled = url.content.decode("utf-8")
soup = BeautifulSoup(url.content, 'html.parser')
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
sail = False
sailingPossibilitys = ""
for x in range(0, 48, 2):
    if windArray[x] >= minWind and windArray[x+1] <= maxWind and rainArray[singleSteps] <= maxRain and countHour+1 >= minTime and countHour+1 <= maxTime:
        if countHour >= minHours:
            dataString = """\n{hour} o'clock with {mWind} - {xWind}(kts) of wind and {rain} (mm/h) of rain""".format(hour = countHour+1, mWind = windArray[x], xWind = windArray[x+1], rain = rainArray[singleSteps])
            sailingPossibilitys = sailingPossibilitys + dataString
            sail = True

    if singleSteps >= 0:
        countHour = singleSteps
    singleSteps = singleSteps+1

if sail == True:
    sendEmail()

with open('scrapes.txt', 'w') as f:
    f.write(str(windArray) + str(rainArray))