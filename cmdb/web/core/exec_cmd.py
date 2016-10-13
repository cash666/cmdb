#!/usr/bin/env python
#coding:utf8

import paramiko

def ExecCommand(host,port,username,passwd,cmd):
	result=[]
	try:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(host, port, username, passwd)
		stdin, stdout, stderr = ssh.exec_command(cmd)
	except Exception,e:
		result.append(e[1])
		pass
	else:
		err=stderr.read()
		if err:
			result.append(err)	
		else:
			for ret in stdout.readlines():
				result.append(ret)
	finally:
		ssh.close()
		return result

