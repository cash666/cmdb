#coding:utf8

from django import template
from django.utils.safestring import mark_safe
  
register = template.Library()

@register.simple_tag
def is_list(str):
	if isinstance(str,list):
		return True
	else:
		return False
