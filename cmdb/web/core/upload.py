#!/usr/bin/env python
#coding:utf8

import paramiko

def UploadFiels(hostname,port,username,passwd,src_file,dst_file):
	result={}
	try:
		t = paramiko.Transport((hostname,port))
		t.connect(username=username,password=passwd)
	except Exception,e:
		result[hostname]='fail'
		pass
	else:
		sftp = paramiko.SFTPClient.from_transport(t)
                sftp.put(src_file,dst_file)
		t.close()
	finally:
		return result

#UploadFiels('192.168.47.154',22122,'root','caoshuai666','/root/1.txt','/tmp/2.txt')
