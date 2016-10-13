#coding:utf8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Idc(models.Model):
	'''	
	IDC表:名称和备注	
	'''
	idc_name = models.CharField(max_length=40, verbose_name=u'机房名称')
	remark = models.CharField(max_length=40, verbose_name=u'备注')

	def __unicode__(self):
		return self.idc_name

	class Meta:
		verbose_name = u'机房列表'          #admin后台定义显示的名称        
		verbose_name_plural = u'机房列表'

class HostList(models.Model):
	'''
	主机表
	'''
	number = models.CharField(max_length=30,unique=True,verbose_name=u'资产编号')
	InnerIp = models.GenericIPAddressField(verbose_name=u'内网IP地址',null=True,blank=True,unique=True)
	OuterIp = models.GenericIPAddressField(verbose_name=u'外网IP地址',null=True,blank=True,unique=True)
	hostname = models.CharField(max_length=30, verbose_name=u'主机名',null=True,blank=True)
	group = models.ManyToManyField('Group',verbose_name=u'组名')
	application = models.CharField(max_length=20, verbose_name=u'应用')
	idc_name = models.ForeignKey(Idc)

	def __unicode__(self):
		return self.number

	class Meta:
		verbose_name = u'主机列表'		
		verbose_name_plural = u'主机列表'

class Assets(models.Model):
	'''
	资产表
	'''
	asset_number=models.OneToOneField(HostList)
	hostname = models.CharField(max_length=30, verbose_name=u'主机名')
	InnerIp = models.GenericIPAddressField(verbose_name=u'内网IP地址',null=True,blank=True,unique=True)
	OuterIp = models.GenericIPAddressField(verbose_name=u'外网IP地址',null=True,blank=True,unique=True)
	manufacturer = models.CharField(max_length=20, verbose_name=u'厂商')    
	productname = models.CharField(max_length=30, verbose_name=u'产品型号')
	sn=models.CharField(max_length=80, unique=True, verbose_name=u'序列号')
	cpu_model = models.CharField(max_length=50, verbose_name=u'CPU型号')
	cpu_nums = models.SmallIntegerField(verbose_name=u'CPU线程数')
	cpu_cores = models.PositiveSmallIntegerField(verbose_name=u'CPU物理核数')
	mem = models.CharField(max_length=100, verbose_name=u'内存大小')
	disk = models.CharField(max_length=300, verbose_name=u'硬盘大小')
	os = models.CharField(max_length=20, verbose_name=u'操作系统')
	token = models.CharField(max_length=20,default='cmdb',verbose_name=u'资产令牌')

	def __unicode__(self):        
		return '%s' % self.hostname

	class Meta:        
		verbose_name = u'主机资产信息'        
		verbose_name_plural = u'主机资产信息管理'

class Group(models.Model):    
	name = models.CharField(max_length=50,unique=True)    

	def __unicode__(self):        
		return self.name    

		class Meta:        
			verbose_name = u'主机组信息'        
			verbose_name_plural = u'主机组信息管理'

class Upload(models.Model):    
	headImg = models.FileField(upload_to = './uploads/')    

	def __unicode__(self):        
		return self.headImg    

	class Meta:		
		verbose_name = u'文件上传'        
		verbose_name_plural = u'文件上传'

class Task(models.Model):
	task_name=models.CharField(max_length=64)
	target_host=models.ManyToManyField(HostList)
	task=models.CharField(max_length=64)
	task_time=models.CharField(max_length=32,null=True,blank=True)
	create_time=models.DateTimeField(auto_now_add=True)
	is_finished=models.BooleanField(default=False)

	def __unicode__(self):
		return self.task_name

	class Meta:
		verbose_name=u'任务流程'
		verbose_name_plural=u'任务流程'

class UserProfile(models.Model):
        '''
        账户信息表
        '''
        #一对一关联django自带user表
        user=models.OneToOneField(User)
        name=models.CharField(max_length=32)
        groups=models.ManyToManyField('UserGroup')

        def __unicode__(self):
                return self.name

	class Meta:
                verbose_name=u'账户信息'
                verbose_name_plural=u'账户信息'

class UserGroup(models.Model):
        '''
        用户组
        '''
        name=models.CharField(max_length=64,unique=True)

        def __unicode__(self):
                return self.name

	class Meta:
                verbose_name=u'用户组'
                verbose_name_plural=u'用户组'
