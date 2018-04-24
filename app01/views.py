from django.shortcuts import render,HttpResponse,redirect
from app01 import models
from app01.forms import RegisterForm
from django.core.exceptions import NON_FIELD_ERRORS
from django.db.models import F
from django.db import transaction
import json
# Create your views here.
def index(request,*args,**kwargs):
    type_id=int(kwargs.get('type_id')) if kwargs.get('type_id') else 0
    type_choices_list=models.Article.type_choices
    print(request.path_info)  #打印访问的后缀url
    condition={}
    if type_id:
        condition['article_type_id']=type_id

    article_list=models.Article.objects.filter(**condition)

    return render(request,'index.html',
                  {'type_choices_list':type_choices_list,
                   'article_list':article_list,
                   'type_id':type_id
                                        })

def login(request):
    if request.method=="GET":
        return render(request,'login.html')
    else:
        input_code=request.POST.get("code")
        if input_code:
            session_code=request.session.get("code")
            if input_code.upper()==session_code.upper():
                return redirect('/index/')
            else:
                return render(request, 'login.html')
        return render(request, 'login.html')

def check_code(request):
    #读取硬盘中的文件在页面上显示
    # f=open('static/imgs/yingjie.jpg','rb')
    # data=f.read()
    # f.close()
    # return HttpResponse(data)

    #创建文件并保存
    #pip3 install pillow

    # from PIL import Image
    # f=open('code.png','wb')
    #创建一个白色的图片
    # img = Image.new(mode='RGB', size=(120, 30), color=(255, 255, 255))
    # img.save(f,'png')
    # f.close()
    # return HttpResponse("...")

    # from PIL import Image,ImageDraw,ImageFont
    # from io import BytesIO
    # f=BytesIO()
    # img = Image.new(mode='RGB', size=(120, 30), color=(187, 255, 255))
    # #创建画笔，用于在图片上画任意内容
    # draw = ImageDraw.Draw(img, mode='RGB')
    # #画点
    # #  第一个参数：表示坐标
    # # 第二个参数：表示颜色
    # draw.point([10,10],fill="red")
    # draw.point([80,10],fill=(255,255,255))
    # #画线
    # # 第一个参数：表示起始坐标和结束坐标
    # # 第二个参数：表示颜色
    # draw.line((15,10,50,50),fill=(0,255,0))
    # #画圈
    # # 第一个参数：表示起始坐标和结束坐标（圆要画在其中间）
    # # 第二个参数：表示开始角度
    # # 第三个参数：表示结束角度
    # # 第四个参数：表示颜色
    # draw.arc((0, 0, 30, 30), 0, 360, fill="red")
    # #选择字体，写字。前面是字体，后面是字体大小
    # # font = ImageFont.truetype("kumo.ttf", 28)
    # # 第一个参数：表示起始坐标
    # # 第二个参数：表示写入内容
    # # 第三个参数：表示颜色
    # # draw.text([0, 0], 'python', "red",font=font)
    #
    # #生成随机字符
    # import random
    # # char_list=[]
    # # for i in range(5):
    # #     char=chr(random.randint(65,90))
    # #     char_list.append(char)
    # # ''.join(char_list)
    #
    # # v=''.join([ chr(random.randint(65,90)) for i in range(5) ])
    #
    # char_list=[]
    # for i in range(5):
    #     char=chr(random.randint(65,90))
    #     font = ImageFont.truetype("kumo.ttf", 28)
    #     draw.text([i*24, 0], char, (random.randint(0,255),random.randint(0,255),random.randint(0,255)),font=font)
    #     char_list.append(char)
    # code=''.join(char_list)
    #
    # #保存图片
    # img.save(f, 'png')
    # #获取生成的图片
    # data = f.getvalue()
    # #保存在session
    # request.session['code']=code

    from io import BytesIO
    from utils.random_check_code import rd_check_code
    stream=BytesIO()
    img,code=rd_check_code()
    img.save(stream, 'png')
    request.session['code'] = code
    return HttpResponse(stream.getvalue())

def register(request):
    """
    用户注册
    :param request:
    :return:
    """
    if request.method=="GET":
        obj=RegisterForm(request)
        return render(request,'register.html',{'obj':obj})

    else:
        obj=RegisterForm(request,request.POST,request.FILES)  #定制的init需要request
        if obj.is_valid():
            pass
        else:
            # print(obj.errors['__all__'])
            # print(obj.errors[NON_FIELD_ERRORS])
            pass
        return render(request, 'register.html', {'obj': obj})

def home(request,site):
    """
    访问个人博客主页
    :param request:请求相关信息
    :param site:个人博客后缀 如:http://www.xx.com/xxxx/
    :return:
    """
    blog=models.Blog.objects.filter(site=site).first()
    if not blog:
        return redirect("/")

    #按照分类，标签，时间group by
    from django.db.models import Count
    category_list=models.Article.objects.filter(blog=blog).values('category_id','category__title').annotate(ct=Count('nid'))

    #标签
    tag_list=models.Article2Tag.objects.filter(article__blog=blog).values('tag_id','tag__title').annotate(ct=Count("id"))

    #时间
    date_list=models.Article.objects.filter(blog=blog).extra(select={'ctime':"strftime('%%Y-%%m',create_time)"}).values('ctime').annotate(ct=Count("nid"))

    #所有的文章
    article_list=models.Article.objects.filter(blog=blog).all()
    return render(
        request,
        'home.html',
        {'blog':blog,
        'category_list':category_list,
         'tag_list':tag_list,
         'date_list':date_list,
         'article_list':article_list,
         }
    )
    # return HttpResponse("...")

    # cate_list=models.Category.objects.filter(blog=blog)
    # for item in cate_list:
    #     c=item.article_set.all().count()  #取该分类的总文章数
    #     print(item,c)

    # 取该分类的总文章数,推荐
    # from django.db.models import Count
    # cate_list=models.Article.objects.filter(blog=blog).values('category_id','category__title').annotate(c=Count("nid"))
    #

    # 取该标签的总文章数
    # tag_list=models.Tag.objects.filter(blog=blog)
    # for tag in tag_list:
    #     c=tag.article_set.all().count()
    #     print(tag,c)

    # from django.db.models import Count
    # # models.Article2Tag.objects.values('article_id','tag_id','article__title','tag__title')
    #
    # #自定义第三章表取 该标签的数量
    # # models.Article2Tag.objects.filter(tag__blog=blog).values('tag_id','tag__title').annotate(c=Count('id'))
    #
    # #用django创建的第三章表，取该标签的文章数量
    # # models.Article.objects.filter(blog=blog).values('tags__id','tags__title').annotate(c=Count("nid"))
    #
    # #时间分类
    # #mysql
    # data_list=models.Article.objects.filter(blog=blog).extra(select={'c':"date_format(create_time,'%%Y-%%m')"}).values("c").annotate(ct=Count("nid"))
    # #sqlite
    # data_list=models.Article.objects.filter(blog=blog).extra(select={'c':"strftime('%%Y-%%m',create_time)"}).values("c").annotate(ct=Count("nid"))
    # #select date_format(create_time,'%Y-%m') as c,count(nid) as ct from article where blog_id=1 group by date_format(create_time,'%Y-%m')
    #
    # #django内置函数
    # """
    # from .base import (
    # Cast, Coalesce, Concat, ConcatPair, Greatest, Least, Length, Lower, Now,
    # Substr, Upper,
    # )
    # from .datetime import (
    # Extract, ExtractDay, ExtractHour, ExtractMinute, ExtractMonth,
    # ExtractSecond, ExtractWeekDay, ExtractYear, Trunc, TruncDate, TruncDay,
    # TruncHour, TruncMinute, TruncMonth, TruncSecond, TruncYear,
    # )
    # """
    # # 时间类函数
    # from django.db.models import functions
    # """
    #  1. 时间截取，不保留其他：Extract, ExtractDay, ExtractHour, ExtractMinute, ExtractMonth,ExtractSecond, ExtractWeekDay, ExtractYear,
    # """
    # data_list = models.Article.objects.filter(blog=blog).annotate(x=functions.Extract('create_time','year'))
    # data_list = models.Article.objects.filter(blog=blog).annotate(x=functions.ExtractYear('create_time'))
    # #2018
    #
    # """
    # 2. 时间截图，保留其他：Trunc, TruncDate, TruncDay,TruncHour, TruncMinute, TruncMonth, TruncSecond, TruncYear
    # """
    # data_list = models.Article.objects.filter(blog=blog).annotate(x=functions.Trunc('create_time', 'year'))
    # data_list = models.Article.objects.filter(blog=blog).annotate(x=functions.TruncYear('create_time'))
    # #2018-01-01 01:01:01
    #
    # """3.内置函数，都会生成新的一列"""
    # from django.db.models import FloatField
    # from django.db.models import Value
    # v=models.Article.objects.annotate(x=functions.Cast("nid",FloatField)) #将nid列转成浮点型
    # v=models.Article.objects.annotate(x=functions.Coalesce("title","summary")) #从前向后，查询第一个不为空的值
    # #ConcatPair，拼接（仅两个参数）
    # #Now，获取当前时间
    # v=models.Article.objects.annotate(x=functions.Concat("nid","title","summary")) #将nid，title，summary的值获取拼接成字符串
    # v=models.Article.objects.annotate(x=functions.Concat("nid","title",Value("666"))) #拼接普通字符串
    # v=models.Article.objects.annotate(x=functions.Greatest("nid","num")) #获取两列最大的值
    # v=models.Article.objects.annotate(x=functions.Length("title"))  #获取长度，只能传一个参数
    # v=models.Article.objects.annotate(x=functions.Substr("title",1,1)) #截取title列，必须从第一个开始，截取一个
    # """原理:  select upper('title') from xxx"""
    #
    # #django自定义函数
    # from django.db.models.functions.base import Func
    # class YearMothFunc(Func):
    #     function = 'DATE_FORMAT'
    #     template = '%(function)s(%(expressions)s,%(format)s)'
    #     """DATE_FORMAT(create_time,'%Y-%m')"""
    #
    #     def __init__(self, expression, **extra):
    #         expressions = [expression]
    #         super(YearMothFunc, self).__init__(*expressions, **extra)
    #
    # v=models.UserInfo.objects.annotate(c=YearMothFunc('create_time',format="%%Y-%%m"))
    #
    #
    # #当前博客的所有文章
    # # models.Article.objects.filter(blog=blog)
    #
    # #当前博客所有分类
    # models.Category.objects.filter(blog=blog)
    #
    # # blog.user.username  #获取用户信息
    # #获取个人当前博客所有的文章
    # # models.Article.objects.filter(blog=blog)
    # # models.Article.objects.filter(blog_id=blog.nid) #和以上一样
    # # blog.article_set.all()
    #
    # #一句代码将blog和userinfo连接在一起，再根据site进行筛选
    # # models.Blog.objects.filter(site=site).values('site','user__nickname')
    #
    # #获取一对一onetoone
    # # v=models.UserInfo.objects.filter(blog__site=site).values('blog__site','nickname')
    # # print(v)
    #
    # #获取访问site的用户名一对一
    # # obj=models.Blog.objects.filter(site=site).first()
    # # print(obj.user.nickname)
    #
    # #根据用户名查找site一对一
    # # obj=models.UserInfo.objects.filter(username='zxy').first()
    # # print(obj.blog.site)
    #


    # return HttpResponse("...")

def filter(request,site,key,val):
    blog = models.Blog.objects.filter(site=site).first()
    if not blog:
        return redirect("/")

    # 按照分类，标签，时间group by
    from django.db.models import Count
    category_list = models.Article.objects.filter(blog=blog).values('category_id', 'category__title').annotate(
        ct=Count('nid'))

    # 标签
    tag_list = models.Article2Tag.objects.filter(article__blog=blog).values('tag_id', 'tag__title').annotate(
        ct=Count("id"))

    # 时间
    date_list = models.Article.objects.filter(blog=blog).extra(
        select={'ctime': "strftime('%%Y-%%m',create_time)"}).values('ctime').annotate(ct=Count("nid"))

    if key=="category":
        article_list=models.Article.objects.filter(blog=blog,category_id=val)
    elif key=="tag":
        #通过manytomany字段查询
        article_list=models.Article.objects.filter(blog=blog,tags__nid=val)
        # print(article_list)
        #自定义第三张表
        #自己反向关联
        # article_list=models.Article.objects.filter(blog=blog,article2tag__tag_id=val)
    else:
        article_list=models.Article.objects.filter(blog=blog).extra(where=["strftime('%%Y-%%m',create_time)=%s"],params=[val,])

    return render(
        request,
        'filter.html',
        {'blog': blog,
         'category_list': category_list,
         'tag_list': tag_list,
         'date_list': date_list,
         'article_list': article_list,
         }
    )

def article(request,site,nid):
    blog = models.Blog.objects.filter(site=site).first()
    if not blog:
        return redirect("/")

    # 按照分类，标签，时间group by
    from django.db.models import Count
    category_list = models.Article.objects.filter(blog=blog).values('category_id', 'category__title').annotate(
        ct=Count('nid'))

    # 标签
    tag_list = models.Article2Tag.objects.filter(article__blog=blog).values('tag_id', 'tag__title').annotate(
        ct=Count("id"))

    # 时间
    date_list = models.Article.objects.filter(blog=blog).extra(
        select={'ctime': "strftime('%%Y-%%m',create_time)"}).values('ctime').annotate(ct=Count("nid"))

    obj=models.Article.objects.filter(blog=blog,nid=nid).first()

    ###########################评论#################################
    msg_list = [
        {'id': 1, 'content': '太好了', 'parent_id': None},
        {'id': 2, 'content': '你说得对', 'parent_id': None},
        {'id': 3, 'content': '顶楼上', 'parent_id': None},
        {'id': 4, 'content': '你眼瞎吗', 'parent_id': 1},
        {'id': 5, 'content': '我看是', 'parent_id': 4},
        {'id': 6, 'content': '嘿嘿', 'parent_id': 2},
        {'id': 7, 'content': '是你没呀', 'parent_id': 5},
        {'id': 8, 'content': 'xxxxxxx', 'parent_id': 3},

    ]
    result = []
    msg_list_dict = {}
    for i in msg_list:
        i['child'] = []
        msg_list_dict[i['id']] = i
        pid = i['parent_id']
        if pid:
            msg_list_dict[pid]['child'].append(i)
        else:
            result.append(i)

    #评论
    from utils.comment import comment_tree
    comment_str=comment_tree(result)

    return render(
        request,
        'article.html',
        {'blog': blog,
         'category_list': category_list,
         'tag_list': tag_list,
         'date_list': date_list,
         'obj': obj,
         'comment_str':comment_str
         }
    )

def up(request):
    #是谁，文章，赞1或踩0
    #当前登录信息，session获取
    #文章
    response={'status':True,'msg':None}

    try:
        user_id = request.session.get('user_id')
        article_id = request.POST.get('nid')
        val = int(request.POST.get("val"))
        obj=models.UpDown.objects.filter(user_id=user_id,article_id=article_id).first()
        if obj:
            #已经赞
            pass
        else:
            #没有赞
            #事务，一旦出现错误就不再执行下面得操作
            with transaction.atomic():
                if val:
                    models.UpDown.objects.create(user_id=user_id, article_id=article_id, up=True)
                    models.Article.objects.filter(nid=article_id).update(up_count=F("up_count")+1)

                else:
                    models.UpDown.objects.create(user_id=user_id, article_id=article_id, up=False)
                    models.Article.objects.filter(nid=article_id).update(down_count=F("down_count")+1)


    except Exception as e:
        response['status']=False
        response['msg']=str(e)
    return HttpResponse(json.dumps(response))

def lizhi(request,**kwargs):
    print(kwargs)
    condition={}
    for k,v in kwargs.items():
        kwargs[k]=int(v)
        if v!='0':
            condition[k]=v

    #大分类
    type_list=models.Article.type_choices

    #个人的分类
    category_list=models.Category.objects.filter(blog_id=1)

    #个人标签
    tag_list=models.Tag.objects.filter(blog_id=1)

    #进行筛选
    condition['blog_id']=1
    # article_list=models.Article.objects.filter(blog_id=1)
    article_list=models.Article.objects.filter(**condition)
    return render(
        request,'lizhi.html',
        {'type_list':type_list,
        'category_list':category_list,
        'tag_list':tag_list,
        'article_list':article_list,
         'kwargs':kwargs,
         },
    )

from app01.forms import ArticleForm
CONTENT=""
def wangzhe(request):
    if request.method=="GET":
        obj=ArticleForm()
        return render(request,'wangzhe.html',{'obj':obj})
    else:
        obj=ArticleForm(request.POST)
        if obj.is_valid():
            content=obj.cleaned_data['content']
            # content=request.POST.get('content')
            global CONTENT
            CONTENT=content
            print(content)
            return HttpResponse("...")

def see(request):
    return render(request,'see.html',{'con':CONTENT})

#文件上传
import os
def upload_img(request):
    upload_type=request.GET.get("dir")  #上传的是什么类型，文件、视频、图片
    file_obj=request.FILES.get('imgFile')  #获取文件对象
    file_path=os.path.join('static/imgs',file_obj.name)
    with open(file_path,'wb') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)

    # print(request.FILES,request.POST)
    dic={
        'error':0,
        'url':'/'+file_path,
        'message':'错误了'
    }  #只能返回这个字典。不能修改key
    return HttpResponse(json.dumps(dic))


def comments(request,nid):
    response={'status':True,'data':None,'msg':None}
    try:
        msg_list = [
            {'id': 1, 'content': '太好了', 'parent_id': None},
            {'id': 2, 'content': '你说得对', 'parent_id': None},
            {'id': 3, 'content': '顶楼上', 'parent_id': None},
            {'id': 4, 'content': '你眼瞎吗', 'parent_id': 1},
            {'id': 5, 'content': '我看是', 'parent_id': 4},
            {'id': 6, 'content': '嘿嘿', 'parent_id': 2},
            {'id': 7, 'content': '是你没呀', 'parent_id': 5},
            {'id': 8, 'content': 'xxxxxxx', 'parent_id': 3},

        ]
        result = []
        msg_list_dict = {}
        for i in msg_list:
            i['child'] = []
            msg_list_dict[i['id']] = i
            pid = i['parent_id']
            if pid:
                msg_list_dict[pid]['child'].append(i)
            else:
                result.append(i)
        response['data']=result
    except Exception as e:
        response['status']=False
        response['msg']=str(e)

    return HttpResponse(json.dumps(response))