#!/usr/bin/env python
#-*- coding:UTF-8 -*-
import paramiko, socket, threading

result = {}
lock = threading.Lock()

def runcmd(servers, cmd):
    global result
    thread_pool = []
    for s in servers:
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(100)
        try:
            sk.connect((s.ip, int(s.port)))
        except :
            result[s.ip] = "connect to address %s on Port %s fail!" % (s.ip, s.port)
            sk.close()
        else:
            thread_pool.append(commandThread(s, cmd))
    for work in thread_pool:
        work.start()
    for work in thread_pool:
        work.join()
    r = result
    result = {}
    return r
    
class commandThread(threading.Thread):
    global result, lock
    
    def __init__(self, s, cmd):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.server = s
    
    def res(self, info):
         if lock.acquire():
            result[self.server.ip] = info
            lock.release()
    
    def ssh_client(self):
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            s.connect(self.server.ip, int(self.server.port), self.server.username, self.server.password)
        except paramiko.AuthenticationException, e:
            self.res(e)
            s = None
        return s
    
    def run(self):
        client = self.ssh_client()
        if client:
            stdin, stdout, stderr = client.exec_command(self.cmd)
            error = stderr.read()
            if error:
                self.res(error)
            else:
                self.res(stdout.read())
                    
        client.close()
