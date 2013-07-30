#!/usr/bin/env python
# -*- coding: gbk -*-

import smtplib,sys
from email.mime.text import MIMEText
#############
#TO WHOM you want to send!

'''try:
	help_msg ='Usage: python mailer.py -u "axli@gmail.com jerry@baidu.com"  -c "service down!" ' 
	if '-u' and '-c' in sys.argv:
		mailto_list =  sys.argv[sys.argv.index('-u') + 1].split()
		mail_content = sys.argv[sys.argv.index('-c') + 1]
	else:
		print help_msg
		sys.exit()

except IndexError:
	print help_msg,sys.exit()
'''
#mailto_list=["axli@advent.com"]
#####################
#server address, user, pass
mail_host="smtp.126.com"
mail_user="lijie3721"
mail_pass="youPassword"
mail_postfix="126.com"
######################
def send_mail(to_list,sub,content):
    '''
    to_list:to who
    sub: subject
    content: content
    send_mail("aaa@126.com","sub","content")
    '''
    me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content)
    msg['Subject'] = sub
    msg['From'] = me
    #msg['To'] = ";".join(to_list)
    msg['To'] = to_list.strip()
    print "SENDING EMAIL TO:",msg['To']
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
	try:
		help_msg ='''Usage: python mailer.py -u "axli@gmail.com;jerry@baidu.com"  -c "service down!" '''
		if '-u' and '-c' in sys.argv:
			mailto_list =  sys.argv[sys.argv.index('-u') + 1]
			mail_content = sys.argv[sys.argv.index('-c') + 1]
		else:
			print help_msg
			sys.exit()

	except IndexError:
		print help_msg,sys.exit()

	if send_mail(mailto_list,"subject",mail_content):
        	print "Mail sent success!"
    	else:
        	print "Mail sent failed!"
else:pass
