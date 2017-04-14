import requests
import config
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime
import logging


logging.basicConfig(filename="log.log", level=logging.INFO)


def send_mail(high_temperature, low_temperature):
    content = "Temperature changes a lot.\n"
    content += "Today temperature:" + str(high_temperature) + "to" +str(low_temperature) +"."
    sender = config.sender
    receivers = config.receivers

    message = MIMEText(content, "plain")
    message["From"] = Header("qingacfun@163.com")
    message["To"] = Header("994819188@qq.com")
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

send_mail(10, 10)
# if __name__ == "__main__":
#     citys = ["hangzhou", "shanghai"]
#     for city in citys:
#         url = config.weather_url + city
#         html = requests.get(url).text
#         soup = BeautifulSoup(html, "lxml")
#         temperature = soup.find("p", {"class": "wt_fc_c0_i_temp"}).get_text().split(' ')
#         try:
#             logging.info(str(datetime.now()))
#             high_temperature = int(temperature[0][:-3])
#             low_temperature = int(temperature[2][:-3])
#
#             with open("var.txt", "r") as var:
#                 prev_high_temperature, prev_low_temperature =list(map( int, var.read().split()))
#                 print(prev_high_temperature, prev_low_temperature)
#             with open("var.txt", "w") as var:
#                 write_str = str(high_temperature) + ' ' + str(low_temperature)
#                 var.write(write_str)
#             logging.info("Start to handle temperature:")
#             if abs(prev_low_temperature-low_temperature) >=4 or abs(prev_high_temperature-high_temperature)>=4:
#                 logging.info("send mail")
#                 send_mail(high_temperature, low_temperature)
#             else:
#                 logging.info("Don't need to send mail")
#         except Exception as e:
#             logging.error(str(e))
#
