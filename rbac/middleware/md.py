
#!/usr/bin/env python
#encoding:utf-8
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from rbac.config import VALID_URL
import re
class RbacMiddleware(MiddlewareMixin):
    #只完成权限验证
    def process_request(self,request):
        for pattern in VALID_URL:
            if re.match(pattern,request.path_info):  #如果匹配成功，不走该验证
                return None

        # valid=['/auth-login.html','/index.html']  #设置白名单。
        #http://127.0.0.1:8000/index-1.html?md=GET 测试
        action=request.GET.get('md')
        user_permission_dict=request.session.get('user_permission_dict')
        if not user_permission_dict:
            return HttpResponse("无权限")

        flag=False
        for k,v in user_permission_dict.items():  #匹配正则
            if re.match(k,request.path_info):
                #re.match('/index-(\d+).html','/index-11.html')
                if action in v:
                    flag=True
                    break

        if not flag:
            return HttpResponse("无权限")
