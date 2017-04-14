
try:
    from . import main
except Exception as e:
    import main


main.send_mail(10, 10)