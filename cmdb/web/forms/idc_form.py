#!/usr/bin/env python
#coding:utf8

from django import forms

class IDCForm(forms.Form):
	idc_name=forms.CharField(max_length=32)
	remark=forms.CharField(max_length=100,required=False,widget=forms.widgets.Textarea(attrs={'class':'form-control','placeholder':u'备注','rows':7}))
