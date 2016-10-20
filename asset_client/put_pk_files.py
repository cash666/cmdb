#!/usr/bin/env python
#coding:utf8

import paramiko
import time

def PutPkFile(ip,port,username,passwd,src_file,dst_file):
	try:
		t = paramiko.Transport((ip,port))
		t.connect(username=username,password=passwd)
	except Exception,e:
		f=open('logs/put.log','a')
		now=time.strftime("%Y-%m-%d %X", time.localtime())
		f.write('%s put fail:%s\n' % (now,e))
		f.close()
		pass
	else:
		sftp = paramiko.SFTPClient.from_transport(t)
		sftp.put(src_file,dst_file)
	finally:
		t.close()
