#coding:utf8

from django import forms
from web import models

class PutFileForm(forms.Form):
	host_groups=forms.CharField(widget=forms.Select())
	put_files=forms.CharField(widget=forms.Select())
	put_dir=forms.CharField(max_length=64,widget=forms.TextInput(attrs={'placeholder': u'写全路径和文件名,如/tmp/1.txt'}))

	def __init__(self,*args,**kwargs):
                super(PutFileForm,self).__init__(*args,**kwargs)
                self.fields['host_groups'].widget.choices=models.Group.objects.all().values_list('id','name')
                self.fields['put_files'].widget.choices=models.Upload.objects.all().values_list('id','headImg')
