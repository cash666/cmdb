#coding:utf8
from django.utils.safestring import mark_safe

class pager(object):

        def __init__(self,current_page):
                self.current_page=current_page

        @property
        def start(self):
                return (self.current_page-1)*10

        @property
        def end(self):
                return self.current_page*10

        def generate_pager_str(self,pager_num,pager_url):
                if pager_num==1:
			start=1
			end=2
		elif pager_num<=11:
                        start=1
                        end=pager_num+1
                elif pager_num>11:  #26
			if self.current_page<=6:
				start=1
				end=12
			elif self.current_page>6 and self.current_page<=pager_num-5:
				start=self.current_page-5
				end=self.current_page+6
			elif self.current_page==pager_num:
				start=self.current_page-10
				end=pager_num+1
			else:
				start=pager_num-10
				end=pager_num+1
                pager_list=[]
                for i in range(start,end):
                        if i == self.current_page:
                                temp="<a style='color:red;font-size:20px' href=%s%d>%d</a>" % (pager_url,i,i)
                        else:
                                temp="<a style='margin-left:5px' href=%s%d>%d</a>" % (pager_url,i,i)
                        pager_list.append(temp)

		#首页
                first_page="<a style='margin-right:5px' href=%s%d>首页</a>" % (pager_url,1)
                #末页
                last_page="<a style='margin-left:5px' href=%s%d>末页</a>" % (pager_url,pager_num)
                #上一页
                if self.current_page > 1:
                        pre_page="<a style='margin-left:5px' href=%s%d>上一页</a>" % (pager_url,self.current_page-1)
                else:
                        pre_page="<a style='margin-left:5px' href='javascript:void(0)'>上一页</a>"
                #下一页
                if self.current_page < pager_num:
                        next_page="<a style='margin-left:5px;margin-right:5px' href=%s%d>下一页</a>" % (pager_url,self.current_page+1)
                else:
                        next_page="<a style='margin-left:5px;margin-right:5px' href='javascript:void(0)'>下一页</a>"
		
		pager_list.insert(0,first_page)	
		pager_list.insert(1,pre_page)
		pager_list.append(next_page)
		pager_list.append(last_page)
                return mark_safe(''.join(pager_list))
