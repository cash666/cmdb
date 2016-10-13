#coding:utf8

from django import forms
from web import models

class SingleCommandForm(forms.Form):
	hostname=forms.CharField(widget=forms.Select())
	command=forms.CharField(max_length=100)

	def __init__(self,*args,**kwargs):
                super(SingleCommandForm,self).__init__(*args,**kwargs)
                self.fields['hostname'].widget.choices=models.HostList.objects.all().values_list('id','OuterIp')
