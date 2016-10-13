#coding:utf8
from django.shortcuts import render,HttpResponse,redirect
from web import models
from core import exec_cmd,upload
from conf import config
from cmdb import settings
from django.contrib.auth import authenticate,login,logout
from web.forms import idc_form,host_form,group_form,single_command_form,put_file_form,multi_command_form,task_form,asset_collect_form
import paramiko
import multiprocessing
import urllib
import json
import time
import os
import sys
import pickle
# Create your views here.

def check_login():
        def decorator(func):
                def wrapper(request):
                        if request.user.is_authenticated:
                                return func(request)
                        else:
                                return redirect('/')
                return wrapper
        return decorator

def acc_login(request):
	message=''
        if request.method == 'POST':
                username=request.POST.get('username')
                password=request.POST.get('password')
                user=authenticate(username=username,password=password)
                if user is not None:
                        login(request,user)
                        return redirect('/cmdb/index/')
                else:
                        message=u"用户名或密码错误"
        return render(request,'login.html',{'message':message})

def acc_logout(request):
	logout(request)
        return redirect('/')

@check_login()
def index(request):
	return render(request,"index.html")

@check_login()
def idc(request):
	idc_obj=models.Idc.objects.all()
	return render(request,'idc.html',{'idc_obj':idc_obj})

@check_login()
def create_idc(request):
	IDCForm=idc_form.IDCForm(request.POST)
	message=''
	if request.method == 'POST':
		idc_name=request.POST.get('idc_name')
		remark=request.POST.get('remark')
		idc_info={'idc_name':idc_name,'remark':remark}
		is_ok=models.Idc.objects.create(**idc_info)
		if is_ok:
			message='添加成功'
		else:
			message='添加失败'
	return render(request,'create_idc.html',{'IDCForm':IDCForm,'message':message})

@check_login()
def delete_idc(request):
	if request.method == 'POST':
		idc_id=request.POST.get('id')
		is_ok=models.Idc.objects.filter(id=idc_id).delete()
		if is_ok:
			message=u'删除成功'
		else:
			message=u'删除失败'
		return HttpResponse(message)

@check_login()
def save_idc(request):
	if request.method == 'POST':
		idc_id=int(request.POST.get('id'))
                idc_name=request.POST.get('idc_name')
                remark=request.POST.get('remark')
		is_ok=models.Idc.objects.filter(id=idc_id).update(idc_name=idc_name,remark=remark)
		if is_ok:
			message=u'保存成功'
		else:
			message=u'保存失败'
		return HttpResponse(message)

@check_login()
def host(request):
	message=request.GET.get('message','')
	host_obj=models.HostList.objects.all()
	return render(request,'host.html',{'host_obj':host_obj,'message':message})

def delete_host(request):
	if request.method == 'POST':
		host_number=request.POST.get('number')
		is_ok=models.HostList.objects.filter(number=host_number).delete()
		if is_ok:
			message=u'删除成功'
		else:
			message=u'删除失败'
		return HttpResponse(message)

@check_login()
def modify_host(request):
	if request.method == 'POST':
		number=request.POST.get('number')
		InnerIp=request.POST.get('InnerIp')
		OuterIp=request.POST.get('OuterIp')
		hostname=request.POST.get('hostname')
		application=request.POST.get('application')
		idc_name_id=request.POST.get('idc_name')
		is_ok=models.HostList.objects.filter(number=number).update(InnerIp=InnerIp,OuterIp=OuterIp,hostname=hostname,application=application,idc_name_id=idc_name_id)
		if is_ok:
			message=u'修改成功'
		else:
			message=u'修改失败'
		print message
		return redirect("/cmdb/host/?message=%s" % message)
	else:
		HostForm=host_form.HostForm()
		id=request.GET.get('id')
		host_info=models.HostList.objects.get(id=id)
		return render(request,'modify_host.html',{'HostForm':HostForm,'host_info':host_info})

@check_login()
def create_host(request):
	if request.method == 'POST':
		number=request.POST.get('number')
                InnerIp=request.POST.get('InnerIp')
                OuterIp=request.POST.get('OuterIp')
                hostname=request.POST.get('hostname')
                application=request.POST.get('application')
		group_id=request.POST.get('group')
                idc_name=request.POST.get('idc_name')
		is_ok=models.HostList.objects.create(number=number,InnerIp=InnerIp,OuterIp=OuterIp,hostname=hostname,application=application,idc_name_id=idc_name)
		if is_ok:
			host_obj=models.HostList.objects.get(number=number)
			group=models.Group.objects.filter(id=group_id)
			host_obj.group.add(*group)
			message=u'主机添加成功!'
		else:
		
			message=u'主机添加失败，请检查!'
		return redirect("/cmdb/host/?message=%s" % message)
	else:
		HostForm=host_form.HostForm()
		return render(request,'create_host.html',{'HostForm':HostForm})

@check_login()
def asset_count(request):
	asset_obj=models.Assets.objects.all()
	return render(request,'asset_count.html',{'asset_obj':asset_obj})

@check_login()
def delete_asset(request):
	if request.method == 'POST':
		asset_number=request.POST.get('asset_number')
		asset_number_obj=models.HostList.objects.get(number=asset_number)
		asset_number_id=asset_number_obj.id
		is_ok=models.Assets.objects.filter(asset_number_id=asset_number_id).delete()
		if is_ok:
			message=u'删除成功'
		else:
			message=u'删除失败'
		return HttpResponse(message)

@check_login()
def group_manage(request):
	message=request.GET.get('message','')
	group_obj=models.Group.objects.all()
	GroupForm=group_form.GroupForm()
	return render(request,"group_manage.html",{'group_obj':group_obj,'GroupForm':GroupForm,'message':message})

@check_login()
def delete_group(request):
	if request.method == 'POST':
		group_name=request.POST.get('name')
		is_ok=models.Group.objects.filter(name=group_name).delete()
		if is_ok:
			message=u'删除成功'
                else:
                        message=u'删除失败'
                return HttpResponse(message)

@check_login()
def create_group(request):
	if request.method == 'POST':
                group_name=request.POST.get('group_name')
		is_ok=models.Group.objects.create(name=group_name)
		if is_ok:
                        message=u'添加成功'
                else:
                        message=u'添加失败'
		return redirect('/cmdb/group_manage/?message=%s' % message)

@check_login()	
def show_hosts(request):
	id=request.GET.get('id')
	group_obj=models.Group.objects.get(id=id)
	hosts_list=group_obj.hostlist_set.all()
	return render(request,'show_hosts.html',{'hosts_list':hosts_list})

@check_login()
def single_command(request):
	SingleCommandForm=single_command_form.SingleCommandForm()
	if request.method == 'POST':
		f=open('logs/command.log','a')
		hostname_id=request.POST.get('hostname')
		command=request.POST.get('command')
		host_obj=models.HostList.objects.get(id=hostname_id)
		hostname=host_obj.OuterIp
		f.write("%s %s exec %s in %s\n" % (time.ctime(),request.user.userprofile.user,command,hostname))
		f.close()
		result=exec_cmd.ExecCommand(hostname,config.port,config.username,config.passwd,command)
		json_result=json.dumps(result)
		return render(request,'single_command.html',{'json_result':json_result,'SingleCommandForm':SingleCommandForm})
	else:
		return render(request,'single_command.html',{'SingleCommandForm':SingleCommandForm})

@check_login()
def upload_files(request):
	if request.method == 'POST':
		file_obj=request.FILES.get('uploadFile','')
		if file_obj:
			file_name=file_obj.name
			f=open('uploads/'+file_name,'wb')
			for line in file_obj.chunks():
				f.write(line)
			f.close()
			is_ok=models.Upload.objects.create(headImg='uploads/%s' % file_name)
			if is_ok and os.path.exists('uploads/'+file_name) and os.path.getsize('uploads/'+file_name)>0:
				message=u'上传成功'
			else:
				message=u'上传失败'
		else:
			message=u'请先上传文件'
	return redirect('/cmdb/put_files/?message=%s' % message)
	
@check_login()
def put_files(request):
	PutFileForm=put_file_form.PutFileForm()	
	if request.method == 'POST':
		group_id=request.POST.get('host_groups')
		put_file_id=request.POST.get('put_files')
		put_file_obj=models.Upload.objects.get(id=put_file_id)
		put_file=put_file_obj.headImg
		put_dir="%s/%s" % (settings.BASE_DIR,put_file)
		dst_dir=request.POST.get('put_dir')
		group_obj=models.Group.objects.get(id=group_id)
		host_lists=group_obj.hostlist_set.all()
		hosts_count=group_obj.hostlist_set.all().count()
		#pool=multiprocessing.Pool(processes=4)
		result=[]
		result_dic={}
		#for item in host_lists:
		#	result.append(pool.apply_async(upload.UploadFiels,(item.OuterIp,config.port,config.username,config.passwd,put_file,dst_dir,)))
		#pool.close()
		#pool.join()
		##print result
		#for ret in result:
		#	ret.get()
		for item in host_lists:
			ret=upload.UploadFiels(item.OuterIp,config.port,config.username,config.passwd,put_dir,dst_dir)
			if ret:
				result.append(ret)
		fail_count=len(result)
		result_dic[u'推送成功个数']=int(hosts_count)-int(fail_count)
		result_dic[u'推送失败个数']=int(fail_count)
		if result:
			result_dic[u'推送失败的IP']=[]
			for item in result:
				for k in item.keys():
					result_dic[u'推送失败的IP'].append(k)
		json_result=json.dumps(result_dic)
		return render(request,'put_files.html',{'PutFileForm':PutFileForm,'json_result':json_result})
	else:
		message=request.GET.get('message','')
		return render(request,'put_files.html',{'PutFileForm':PutFileForm,'message':message})

@check_login()
def multi_command(request):
	MultiCommandForm=multi_command_form.MultiCommandForm()
	if request.method == 'POST':
		group_id=request.POST.get('group')
		group_obj=models.Group.objects.get(id=group_id)
                host_lists=group_obj.hostlist_set.all()
		command=request.POST.get('command')
		result={}
		f=open('logs/multi_command.log','a')
		for item in host_lists:
			ret=exec_cmd.ExecCommand(item.OuterIp,config.port,config.username,config.passwd,command)
			result[item.OuterIp]=ret
			f.write("%s %s exec %s in %s\n" % (time.ctime(),request.user.userprofile.user,command,item.OuterIp))
		f.close()
		json_result=json.dumps(result)
		return render(request,"multi_command.html",{'MultiCommandForm':MultiCommandForm,'json_result':json_result})
	else:
		return render(request,"multi_command.html",{'MultiCommandForm':MultiCommandForm})

@check_login()
def task(request):
	message=request.GET.get('message','')
	task_obj=models.Task.objects.all()
	TaskForm=task_form.TaskForm()
	return render(request,'task.html',{'task_obj':task_obj,'TaskForm':TaskForm,'message':message})

@check_login()
def create_task(request):
	if request.method == 'POST':
		task_name=request.POST.get('task_name')
		task=request.POST.get('task')
		task_time=request.POST.get('task_time','')
		target_host_id=request.POST.get('target_host')
		target_host_obj=models.HostList.objects.get(id=target_host_id)
		target_host=target_host_obj.OuterIp
		if task_time.strip():
			try:
				task_time_split=task_time.split(' ')
				date=task_time_split[0]
				date_time=task_time_split[1]
				date_split=date.split('-')
				date_time_split=date_time.split(':')
				cmd="%d %d %d %d \* %s" % (int(date_time_split[1]),int(date_time_split[0]),int(date_split[2]),int(date_split[1]),task)
				remote_cmd='echo %s >>/var/spool/cron/root' % cmd
			except Exception,e:
				message=u'日期格式有问题'
				return redirect('/cmdb/task/?message=%s' % message)
		else:
			task=task.replace('*','\*')
			remote_cmd="echo %s >>/var/spool/cron/root" % task
		result=exec_cmd.ExecCommand(target_host,config.port,config.username,config.passwd,remote_cmd)
		if not result:
			is_finished=1
			is_ok=models.Task.objects.create(task_name=task_name,task=task,task_time=task_time,is_finished=is_finished)
			if is_ok:
				task_obj=models.Task.objects.get(task_name=task_name,task=task,task_time=task_time)
                        	target_host_obj.task_set.add(task_obj)	
				message=u'任务添加成功'
		else:
			is_finished=0
			is_ok=models.Task.objects.create(task_name=task_name,task=task,task_time=task_time,is_finished=is_finished)
			if is_ok:
				task_obj=models.Task.objects.get(task_name=task_name,task=task,task_time=task_time)
                                target_host_obj.task_set.add(task_obj)
				message=u'任务添加失败，失败原因是:%s' % result[0]
		return redirect('/cmdb/task/?message=%s' % message)

@check_login()
def delete_task(request):
	if request.method == 'POST':
		task_name=request.POST.get('task_name')
                task=request.POST.get('task')
		create_time=request.POST.get('create_time')
		is_ok=models.Task.objects.filter(task_name=task_name,task=task,create_time=create_time).delete()
		if is_ok:
			message=u'删除成功'
		else:
			message=u'删除失败'
		return HttpResponse(message)

@check_login()
def asset_collect(request):
	if request.method == 'POST':
		hostname_id=request.POST.get('hostname')
		hostname_obj=models.HostList.objects.get(id=hostname_id)
		hostname=hostname_obj.OuterIp
		command="python /root/py/asset_client/collect.py"
		ret=exec_cmd.ExecCommand(hostname,config.port,config.username,config.passwd,command)
		if ret:
			message=u'收集%s的资产失败' % hostname
		else:
			pk_file='%s/web/collect_assets/%s.pk' % (settings.BASE_DIR,hostname)
			if os.path.exists(pk_file) and os.path.getsize(pk_file)>0:
				with open(pk_file,'r') as f:
					asset_info=pickle.load(f)
				if time.time()-float(asset_info['timestamp']) > 300:
					message=u'资产文件已过期'
				else:
					hostname=asset_info['hostname']
					InnerIp=asset_info['InnerIp']
					OuterIp=asset_info['OuterIp']
					manufacturer=asset_info['manufacturer']
					productname=asset_info['productname']
					sn=asset_info['sn']
					cpu_model=asset_info['cpu_model']
					cpu_nums=asset_info['cpu_nums']
					cpu_cores=asset_info['cpu_cores']
					mem=asset_info['mem']
					disk=asset_info['disk']
					operate_system=asset_info['os']
					asset_number_obj=models.HostList.objects.get(OuterIp=OuterIp)
					asset_number_id=asset_number_obj.id
					token='cmdb'
					is_ok=models.Assets.objects.create(hostname=hostname,InnerIp=InnerIp,OuterIp=OuterIp,manufacturer=manufacturer,productname=productname,sn=sn,cpu_model=cpu_model,cpu_nums=cpu_nums,cpu_cores=cpu_cores,mem=mem,disk=disk,os=operate_system,asset_number_id=asset_number_id,token=token)
					if is_ok:
						message=u'资产入库成功'
					else:
						message=u'资产入库失败'
		return redirect("/cmdb/asset_collect/?message=%s" % message)
	message=request.GET.get('message','')
	AssetCollectForm=asset_collect_form.AssetCollectForm()
	return render(request,'asset_collect.html',{'AssetCollectForm':AssetCollectForm,'message':message})
