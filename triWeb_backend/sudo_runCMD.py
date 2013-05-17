#-*- coding: utf-8 -*-
import paramiko
import threading
import time, sys
host = '192.168.91.157'
port = 22
usr = 'alex'
pwd = 'alex3714'
timeout = 3

trans = paramiko.Transport((host, port))
trans.connect(username=usr, password=pwd)

chan = trans.open_session()
chan.get_pty()
chan.invoke_shell()


def func(channel, f):
    while True:
        txt = channel.recv(256)
        if not txt:
            f.flush()
            break
        f.write(txt)
        f.flush()

def cmd(cmd_str):

    chan.sendall(cmd_str + '\n')
    time.sleep(timeout)
    
t = threading.Thread(target=func, args=(chan, sys.stdout))
t.setDaemon(1)
t.start()

while True:
    msg = raw_input('')
    if msg == 'exit' or msg == 'quit':
        print 'You input %s command,so i will close session!' % msg
        break
    else:
        cmd(msg)
trans.close()
