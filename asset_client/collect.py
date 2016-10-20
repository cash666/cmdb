#!/usr/bin/env python
#coding:utf8

import platform
import os
import pickle
from put_pk_files import PutPkFile
import settings
import time
import hashlib

asset_info={}
ip=os.popen("ifconfig | grep 'eth1' -A 1 | grep 'inet addr:' | awk '{print $2}' | cut -d':' -f2").read().strip()
pick_file="%s.pk" % ip

def collect():
	operate_system=platform.uname()[0]
	hostname=os.popen('hostname').read().strip('\n')
	InnerIp=os.popen("ifconfig | grep 'eth1' -A 1 | grep 'inet addr:' | awk '{print $2}' | cut -d':' -f2").read().strip()
	OuterIp=os.popen("ifconfig | grep 'eth1' -A 1 | grep 'inet addr:' | awk '{print $2}' | cut -d':' -f2").read().strip()
	manufacturer=os.popen('dmidecode -t system | grep "Manufacturer" | cut -d":" -f2').read().strip()
	productname=os.popen('dmidecode -t system | grep "Product Name" | cut -d":" -f2').read().strip()
	sn=os.popen('dmidecode -t system | grep "Serial Number" | cut -d":" -f2').read().strip()
	cpu_model=os.popen('cat /proc/cpuinfo | grep "model name" | cut -d":" -f2').read().strip()
	cpu_nums=os.popen('cat /proc/cpuinfo | grep "physical id" | sort | uniq -d | wc -l').read().strip()
	cpu_cores=os.popen('cat /proc/cpuinfo | grep "cpu cores" | cut -d":" -f2').read().strip()
	mem=os.popen("cat /proc/meminfo  | grep 'MemTotal' | cut -d':' -f2").read().strip()
	disk=os.popen("lsblk  | grep '^sd' | awk '{print $4}'").read().strip()
	asset_info['os']=operate_system
	asset_info['hostname']=hostname
	asset_info['InnerIp']=InnerIp
	asset_info['OuterIp']=OuterIp
	asset_info['manufacturer']=manufacturer
	asset_info['productname']=productname
	asset_info['sn']=sn
	asset_info['cpu_model']=cpu_model
	asset_info['cpu_nums']=cpu_nums
	asset_info['cpu_cores']=cpu_cores
	asset_info['mem']=mem
	asset_info['disk']=disk
	asset_info['timestamp']=time.time()
	hash=hashlib.md5('cmdb')
	token=settings.token
	unhash_token="%s%s" % (token,time.time())
	hash.update(unhash_token)
	hash_token=hash.hexdigest()
	asset_info['hash_token']=hash_token
	return asset_info

def transmit_asset():
	with open(pick_file,'w') as f:
        	pickle.dump(collect(),f)
	dst_file='/root/py/cmdb/web/collect_assets/%s' % pick_file
	PutPkFile(settings.master,settings.port,settings.username,settings.passwd,pick_file,dst_file)

if __name__ == '__main__':
	transmit_asset()
