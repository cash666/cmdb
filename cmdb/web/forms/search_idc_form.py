#coding:utf8

from django import forms

class SearchIdcForm(forms.Form):
	search_idc=forms.CharField(max_length=20)
