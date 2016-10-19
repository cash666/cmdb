#coding:utf8
from django.shortcuts import render,HttpResponse,redirect
from django.db.models import Q
from web import models
from core import exec_cmd,upload
from conf import config
from cmdb import settings
from pager import page
from django.contrib.auth import authenticate,login,logout
from web.forms import idc_form,host_form,group_form,single_command_form,put_file_form,multi_command_form,task_form,asset_collect_form,group_search_form,search_host_form,search_idc_form,search_task_form,search_log_form
import paramiko
import multiprocessing
import datetime
import urllib
import json
import time
import os
import sys
import pickle
import csv
# Create your views here.

def paging(request,obj1,url,obj2):
	current_page=int(request.GET.get('page',1))
	count=obj1
        page_nums=int(count)
        quotient,reminder=divmod(page_nums,10)
        if reminder>0:
                pager_num=quotient+1
        else:
                pager_num=quotient   #3
        p=page.pager(current_page)
        pager_str=p.generate_pager_str(pager_num,"/cmdb/%s/?page=" % url)
        pager_obj=obj2[p.start:p.end]
	result=(pager_obj,pager_str)
        return result

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
	hosts_count=models.HostList.objects.all().count()
	assets_count=models.Assets.objects.all().count()
	idcs_count=models.Idc.objects.all().count()
	groups_count=models.Group.objects.all().count()
	today = datetime.date.today()
	date_list=[today - datetime.timedelta(days=6),today - datetime.timedelta(days=5),today - datetime.timedelta(days=4),today - datetime.timedelta(days=3),today - datetime.timedelta(days=2),today - datetime.timedelta(days=1),today]
	asset_count_dic={}
	asset_count_dic['name']=u'资产入库统计'
	asset_count_dic['data']=[]
	host_count_dic={}
	host_count_dic['name']=u'主机添加统计'
	host_count_dic['data']=[]
	for i in date_list:
		asset_count=models.Assets.objects.filter(create_time=i).count()
		asset_count_dic['data'].append(asset_count)
		host_count=models.HostList.objects.filter(create_time=i).count()
		host_count_dic['data'].append(host_count)
	series=[asset_count_dic,host_count_dic]
	json_series=json.dumps(series,separators=(',',':'))
	return render(request,"index.html",{'hosts_count':hosts_count,'assets_count':assets_count,'idcs_count':idcs_count,'groups_count':groups_count,'json_series':json_series})

@check_login()
def idc(request):
	idc_obj,pager_str=paging(request,models.Idc.objects.all().count(),'idc',models.Idc.objects.all())
	SearchIdcForm=search_idc_form.SearchIdcForm()
	if request.method == 'POST':
		search_idc=request.POST.get('search_idc')
		search_idc_obj=models.Idc.objects.filter(idc_name__icontains=search_idc)
		return render(request,'idc.html',{'idc_obj':idc_obj,'SearchIdcForm':SearchIdcForm,'search_idc_obj':search_idc_obj})
	return render(request,'idc.html',{'idc_obj':idc_obj,'SearchIdcForm':SearchIdcForm,'pager_str':pager_str})

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
	host_obj,pager_str=paging(request,models.HostList.objects.all().count(),'host',models.HostList.objects.all())
	idc_id=0
	group_obj=None
	SearchHostForm=search_host_form.SearchHostForm()
	if request.method == 'POST':
		search_host=request.POST.get('search_host')
		try:
			idc_obj=models.Idc.objects.get(idc_name__icontains=search_host)
		except Exception,e:
			pass
		else:
			idc_id=idc_obj.id
		try:
			group_obj=models.Group.objects.get(name=search_host)
		except Exception,e:
			pass
		if group_obj:
			search_host_obj=group_obj.hostlist_set.all()
		else:
			search_host_obj=models.HostList.objects.filter(Q(number__icontains=search_host)|Q(InnerIp__icontains=search_host)|Q(OuterIp__icontains=search_host)|Q(hostname__icontains=search_host)|Q(application__icontains=search_host)|Q(idc_name_id=idc_id))
		return render(request,'host.html',{'SearchHostForm':SearchHostForm,'search_host_obj':search_host_obj})
	message=request.GET.get('message','')
	return render(request,'host.html',{'host_obj':host_obj,'SearchHostForm':SearchHostForm,'message':message,'pager_str':pager_str})

@check_login()
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
	asset_obj,pager_str=paging(request,models.Assets.objects.all().count(),'asset_count',models.Assets.objects.all())
	export_csv_file=request.GET.get('file','')
	if request.method == 'POST':
		asset_number_id=0
		search_asset=request.POST.get('search_asset')
		try:
			asset_number_obj=models.HostList.objects.get(number=search_asset)
		except Exception,e:
			pass
		else:
			asset_number_id=asset_number_obj.assets.asset_number_id
		search_asset_obj=models.Assets.objects.filter(Q(asset_number_id=asset_number_id)|Q(hostname__icontains=search_asset)|Q(InnerIp__contains=search_asset)|Q(OuterIp__contains=search_asset)|Q(manufacturer__icontains=search_asset)|Q(productname__icontains=search_asset)|Q(os__icontains=search_asset))
		return render(request,'asset_count.html',{'export_csv_file':export_csv_file,'search_asset_obj':search_asset_obj})
	message=request.GET.get('message','')
	return render(request,'asset_count.html',{'asset_obj':asset_obj,'message':message,'export_csv_file':export_csv_file,'pager_str':pager_str})

@check_login()
def export_asset(request):
	if request.method == 'POST':
		status={}
		export_csv_file='%s/static/downloads/asset_%s.csv' % (settings.BASE_DIR,time.strftime("%Y%m%d%H%M%S"))
		csvFile=open(export_csv_file,'wb')
		csvWriter = csv.writer(csvFile)
		asset_fields=['id','hostname','InnerIp','OuterIp','manufacturer','productname','sn','cpu_model','cpu_nums','cpu_cores','mem','disk','os']
		csvWriter.writerow(asset_fields)
		data=models.Assets.objects.all()
		for item in data:
			csvWriter.writerow([item.id,item.hostname,item.InnerIp,item.OuterIp,item.manufacturer,item.productname,item.sn,item.cpu_model,item.cpu_nums,item.cpu_cores,item.mem,item.disk,item.os])
		csvFile.close()
		if os.path.exists(export_csv_file):
			status['message']=u'导出成功'
			export_csv_file=os.path.basename(export_csv_file)
			status['export_csv_file']=export_csv_file
			json_result=json.dumps(status)
			return HttpResponse(json_result)
		else:
			status['message']=u'导出失败'
			json_result=json.dumps(status)
			return HttpResponse(json_result)

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
	group_obj,pager_str=paging(request,models.Group.objects.all().count(),'group_manage',models.Group.objects.all())
        GroupForm=group_form.GroupForm()
        GroupSearchForm=group_search_form.GroupSearchForm()
	if request.method == 'POST':
		search_group_id=request.POST.get('group','')
		search_group_obj=models.Group.objects.filter(id=search_group_id)
		return render(request,"group_manage.html",{'group_obj':group_obj,'GroupForm':GroupForm,'GroupSearchForm':GroupSearchForm,'search_group_obj':search_group_obj})
	message=request.GET.get('message','')
	return render(request,"group_manage.html",{'group_obj':group_obj,'GroupForm':GroupForm,'message':message,'GroupSearchForm':GroupSearchForm,'pager_str':pager_str})

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
		#f=open('logs/command.log','a')
		hostname_id=request.POST.get('hostname')
		command=request.POST.get('command')
		host_obj=models.HostList.objects.get(id=hostname_id)
		hostname=host_obj.OuterIp
		#f.write("%s %s exec %s in %s\n" % (time.ctime(),request.user.userprofile.user,command,hostname))
		#f.close()
		type='Single command'
		name=request.user.userprofile.user
		hostname=hostname
		cmd=command
		models.cmd_log.objects.create(type=type,name=name,hostname=hostname,cmd=cmd)
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
			type='Upload file'
                	name=request.user.userprofile.user
                	hostname=item.OuterIp
                	cmd="Upload %s" % put_file
                	models.cmd_log.objects.create(type=type,name=name,hostname=hostname,cmd=cmd)
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
			type='Multi command'
                        name=request.user.userprofile.user
                        hostname=item.OuterIp
                        cmd=command
                        models.cmd_log.objects.create(type=type,name=name,hostname=hostname,cmd=cmd)
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
	SearchTaskForm=search_task_form.SearchTaskForm()
	message=request.GET.get('message','')
	TaskForm=task_form.TaskForm()
	if request.method == 'POST':
		search_task=request.POST.get('search_task')
		search_host_obj=models.HostList.objects.filter(Q(InnerIp__icontains=search_task)|Q(OuterIp__icontains=search_task))
		if search_host_obj:
			search_task_obj=[]
			for item in search_host_obj:
				search_host_obj2=models.HostList.objects.get(Q(InnerIp=item.InnerIp)|Q(OuterIp=item.OuterIp))
				search_task_obj.append(search_host_obj2.task_set.all())
			return render(request,'task.html',{'search_task_obj':search_task_obj,'TaskForm':TaskForm,'message':message,'SearchTaskForm':SearchTaskForm})
		else:
			if search_task.lower()=="false" or search_task.lower()=="true":
				if search_task.lower()=="false":
					search_task=0
				else:
					search_task=1
				search_task_obj=models.Task.objects.filter(is_finished=search_task)
				return render(request,'task.html',{'search_task_obj':search_task_obj,'TaskForm':TaskForm,'message':message,'SearchTaskForm':SearchTaskForm})
			else:
				search_task_obj=models.Task.objects.filter(Q(task_name__icontains=search_task)|Q(task__icontains=search_task)|Q(task_time__icontains=search_task))
				return render(request,'task.html',{'search_task_obj':search_task_obj,'TaskForm':TaskForm,'message':message,'SearchTaskForm':SearchTaskForm})
	task_obj,pager_str=paging(request,models.Task.objects.all().count(),'task',models.Task.objects.all())
	return render(request,'task.html',{'task_obj':task_obj,'TaskForm':TaskForm,'message':message,'SearchTaskForm':SearchTaskForm,'pager_str':pager_str})

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
		type='Exec task'
                name=request.user.userprofile.user
                hostname=target_host
                cmd="%s" % task
                models.cmd_log.objects.create(type=type,name=name,hostname=hostname,cmd=cmd)	
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

@check_login()
def log_count(request):
	SearchLogForm=search_log_form.SearchLogForm()
	log_obj,pager_str=paging(request,models.cmd_log.objects.all().count(),'log_count',models.cmd_log.objects.all())
	search_log_obj=None
	if request.method == 'POST':
		search_log=request.POST.get('search_log')
		search_log_obj=models.cmd_log.objects.filter(Q(type__icontains=search_log)|Q(name__icontains=search_log)|Q(cmd__icontains=search_log)|Q(hostname__icontains=search_log))
	return render(request,'log_count.html',{'log_obj':log_obj,'pager_str':pager_str,'SearchLogForm':SearchLogForm,'search_log_obj':search_log_obj})
