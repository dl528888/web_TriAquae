#!/usr/bin/env python
# -*- coding: gbk -*-
#import smtplib and MIMEText
import smtplib,sys
from email.mime.text import MIMEText


#send list 
mailto_list=["axli@advent.com","triaquae@mail.com"]


#SMTP server
mail_host="smtp.126.com"
mail_user="lijie3721"
mail_pass="Alex3714!"
mail_postfix="126.com"
#----------------
subject = sys.argv[1]
content = sys.argv[2]

#subject
def send_mail(to_list,sub,content):
    
    '''to_list: to who
    sub: subject
    content:
    send_mail("axli@advent.com","sub","content")
   '''
    me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content)
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False
if __name__ == '__main__':
    if send_mail(mailto_list,subject,content):
        print "Send email success"
    else:
        print "Send email failure"


