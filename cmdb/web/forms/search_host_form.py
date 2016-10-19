#coding:utf8

from django import forms

class SearchHostForm(forms.Form):
	search_host=forms.CharField(max_length=20)
