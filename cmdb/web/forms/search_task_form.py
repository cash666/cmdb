#coding:utf8

from django import forms

class SearchTaskForm(forms.Form):
	search_task=forms.CharField(max_length=20)
