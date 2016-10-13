#coding:utf8

from django import forms
from web import models

class MultiCommandForm(forms.Form):
	group=forms.CharField(widget=forms.Select())
	command=forms.CharField(max_length=100)

	def __init__(self,*args,**kwargs):
                super(MultiCommandForm,self).__init__(*args,**kwargs)
                self.fields['group'].widget.choices=models.Group.objects.all().values_list('id','name')
