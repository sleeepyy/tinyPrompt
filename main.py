import requests
import config
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime
import logging
import os
import json

logging.basicConfig(filename="log.log", level=logging.INFO)


def send_mail(high_temperature, low_temperature, city):
    content = "Temperature in " + city +" changes a lot compared to yesterday.\n"
    content += "Today temperature is:" + str(high_temperature) + "to" +str(low_temperature) +"."
    content += "Powered by yh."
    sender = config.sender
    print(sender)
    receivers = config.receivers[city]
    host = config.host

    message = MIMEText(content, "plain")
    message["From"] = Header(sender)
    message["To"] = Header("you")
    message["Subject"] = Header("weather prompt", "utf-8")

    try:
        smtp_obj = smtplib.SMTP_SSL(config.host, 465)
        smtp_obj.login(config.user, config.password)
        smtp_obj.sendmail(sender, receivers, message.as_string())
        smtp_obj.quit()
        logging.info("Send Success.")
    except Exception as e:
        logging.error(e)
        logging.info("Failed")

if __name__ == "__main__":
    citys = ["hangzhou","shanghai"]
    last_temp = dict()
    if os.path.isfile("var.json"):
        logging.info(str(datetime.now())+"begin to loads file")
        with open("var.json", "r") as f:
            try:
                last_temp = json.load(f)
            except Exception as e:
                logging.error(str(e))
    for city in citys:
        url = config.weather_url + city
        html = requests.get(url).text
        soup = BeautifulSoup(html, "lxml")
        temperature = soup.find("p", {"class": "wt_fc_c0_i_temp"}).get_text().split(' ')
        try:
            logging.info(str(datetime.now())+city)
            high_temperature = int(temperature[0][:-3])
            low_temperature = int(temperature[2][:-3])
            # high_temperature, low_temperature = 10, 10
            try:
                prev_high_temperature, prev_low_temperature = last_temp[city]["high"], last_temp[city]["low"]
            except Exception as e:
                logging.warning(str(e))
                last_temp[city] = dict()
                last_temp[city]["high"], last_temp[city]["low"] = 0, 0
                prev_high_temperature, prev_low_temperature = last_temp[city]["high"], last_temp[city]["low"]
                print(last_temp[city]["high"])
            print(prev_high_temperature, prev_low_temperature)
            last_temp[city]["high"], last_temp[city]["low"] = high_temperature, low_temperature
            logging.info("Start to handle temperature:")
            if abs(prev_low_temperature-low_temperature) >=4 or abs(prev_high_temperature-high_temperature)>=4:
                logging.info("send mail")
                send_mail(high_temperature, low_temperature, city)
            else:
                logging.info("Don't need to send mail")
        except Exception as e:
            logging.error(str(e))
    try:
        with open("var.json", "w") as f:
            json.dump(last_temp, f)
        logging.info(str(datetime.now())+"begin to dump file")
    except Exception as e:
        logging.error(str(e))
