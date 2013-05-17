
#!/usr/bin/python
import smtplib
#!/usr/bin/python
import smtplib

from email.mime.text import MIMEText

textfile = 'textmail'
fp = open(textfile,'rb')

msg = MIMEText(fp.read())

fp.close()

msg['Subject'] = 'The contents of %s' % textfile
msg['From'] = 'test@mail.com'
msg['To'] = 'lijie3721@126.com'

s = smtplib.SMTP('smtp.126.com')
s.sendmail('test@mail.com',['lijie3721@126.com'], msg.as_string())
s.quit()
