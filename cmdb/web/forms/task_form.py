#coding:utf8

from django import forms
from web import models

class TaskForm(forms.Form):
	task_name=forms.CharField(max_length=64)
	target_host=forms.CharField(widget=forms.Select())
	task=forms.CharField(max_length=64)
	task_time=forms.CharField(max_length=32,required=False)

	def __init__(self,*args,**kwargs):
                super(TaskForm,self).__init__(*args,**kwargs)
                self.fields['target_host'].widget.choices=models.HostList.objects.all().values_list('id','OuterIp')

