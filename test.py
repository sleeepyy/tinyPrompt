
try:
    from . import main
except Exception as e:
    import main


# main.send_mail(10, 10)
import  requests

r = requests.get("http://wthrcdn.etouch.cn/weather_mini?city=北京")
print(r.read())
