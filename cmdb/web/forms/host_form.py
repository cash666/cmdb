#coding:utf8
from django import forms
from web import models
from django.core.exceptions import ValidationError
import re

def ip_validate(value):
	ip_re=re.compile(r'^([1-9][0-9]|[12][0-5][0-4])\.([1-9][0-9]|[12][0-5][0-4])\.([1-9][0-9]|[12][0-5][0-4])\.([1-9][0-9]|[12][0-5][0-4])$')
	if not ip_re.match(value):
			raise forms.ValidationError('IP格式错误')

class HostForm(forms.Form):
	number=forms.CharField(max_length=10)
	InnerIp=forms.CharField(validators=[ip_validate])
	OuterIp=forms.CharField(validators=[ip_validate])
	hostname=forms.CharField(max_length=20)
	group=forms.CharField(widget=forms.Select())
	application=forms.CharField(max_length=30)
	idc_name=forms.CharField(widget=forms.Select())

	def __init__(self,*args,**kwargs):
                super(HostForm,self).__init__(*args,**kwargs)
                self.fields['idc_name'].widget.choices=models.Idc.objects.all().values_list('id','idc_name')
                self.fields['group'].widget.choices=models.Group.objects.all().values_list('id','name')
	
