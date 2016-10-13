#coding:utf8

from django import forms
from web import models

class AssetCollectForm(forms.Form):
	hostname=forms.CharField(widget=forms.Select())

	def __init__(self,*args,**kwargs):
                super(AssetCollectForm,self).__init__(*args,**kwargs)
                self.fields['hostname'].widget.choices=models.HostList.objects.all().values_list('id','OuterIp')
