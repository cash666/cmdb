#coding:utf8
from django import forms
from web import models

class GroupSearchForm(forms.Form):
	group=forms.CharField(widget=forms.Select())

	def __init__(self,*args,**kwargs):
                super(GroupSearchForm,self).__init__(*args,**kwargs)
                self.fields['group'].widget.choices=models.Group.objects.all().values_list('id','name')
	
