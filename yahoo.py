#!/usr/bin/python
# -*- coding: utf-8 -*-





import smtplib
from email.mime.text import MIMEText
from email.header import Header

smtp_host = 'smtp.mail.yahoo.com'  # yahoo
login = "zalet1289@yahoo.com"
password =  "kysbkdnzursvttmw"
recipients_emails = "galatimus@mail.ru"

msg = MIMEText('Есть 30 тая неделя...Лови', 'plain', 'utf-8')
msg['Subject'] = Header('Superkopilka', 'utf-8')
msg['From'] = login
msg['To'] = recipients_emails

s = smtplib.SMTP(smtp_host, 587, timeout=100)
s.set_debuglevel(1)
try:
    s.starttls()
    s.login(login, password)
    s.sendmail(msg['From'], recipients_emails, msg.as_string())
finally:
    print(msg)
    s.quit()