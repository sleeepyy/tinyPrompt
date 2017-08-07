import smtplib
from email.mime.text import MIMEText
from email.header import Header


sender = 'qingacfun@163.com'
receivers = ['994819188@qq.com']
print (receivers[0])
content = "It\'s time to sleep"
# print content# print(message)
message = MIMEText(content, "plain")
# print type(message)
message['From'] = Header('QingAcFun@163.com')
message['To'] = Header('you')
message['Subject'] = Header('TimeToSleep', 'utf-8')

host = 'smtp.163.com'
user = '18867102166@163.com'
passw = 'yanghan123'

try:
	smtpObj = smtplib.SMTP_SSL(host, 465)
	# smtpObj.connect(host, 587)
	smtpObj.login(user, passw)
	smtpObj.sendmail(sender,receivers,message.as_string())
	smtpObj.quit()
	print("success")
except smtplib.SMTPException as e:
	print(e)
