#coding:utf8

from django import forms

class SearchLogForm(forms.Form):
	search_log=forms.CharField(max_length=20)
