import time

from pip._vendor import requests
import json
import smtplib

if __name__ == '__main__':
    zipCode = 84115
    distance = 6
    repeatMinutes = 1
    sender = 'tempforpython123@gmail.com'
    receiver = 'email@gmail.com'
    password = "t3mp124!"

    paramaters = {
        "zipCode": zipCode,
        "format": "application/json",
        "distance": distance,
        "api_key": "1FF55248-313C-4A68-984E-35E7FE1EB44A"
    }

    while True:
        time.sleep(repeatMinutes * 60)
        response = requests.get("https://www.airnowapi.org/aq/observation/zipCode/current", params=paramaters)
        data = response.json()
        jsonObj = json.loads(response.text)
        reportingArea = jsonObj[0]["ReportingArea"]

        ozone = jsonObj[0]["AQI"]
        ozoneConcern = jsonObj[0]["Category"]["Name"]
        ozoneDate = jsonObj[0]["DateObserved"]
        ozoneHour = jsonObj[0]["HourObserved"]

        particulate = jsonObj[1]["AQI"]
        particulateConcern = jsonObj[1]["Category"]["Name"]
        particulateDate = jsonObj[1]["DateObserved"]
        particulateHour = jsonObj[1]["HourObserved"]

        msg = "\r\n".join([
            f"From: {sender}",
            f"To: {receiver}",
            f"Subject: {reportingArea} Air Quality Update",
            "",
            f"Ozone level is {ozone} which is considered {ozoneConcern}. Timestamp: {ozoneDate} at {ozoneHour}:00",
            f"PM2.5 level is {particulate} which is considered {particulateConcern}. Timestamp: {particulateDate} at {particulateHour}:00 "
        ])

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, receiver, msg)
            server.quit()
            print("Email was sent!")
        except:
            print('Something went wrong, email was not sent')

