import smtplib

username = 'test'
password = 'test'
fromaddr = 'test@gmail.com'
toaddr = 'test@txt.att.net'


def send_text():
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddr, msg)
    server.quit()

send_text()
