from django.shortcuts import render,HttpResponse,redirect

# Create your views here.
from app02 import models
from django.db.models import Count
from rbac.service import permission_session
import re
def login(request):
    if request.method=="GET":
        return render(request,'login2.html')
    else:
        #传userid和request
        permission_session(1,request)
        return HttpResponse("")

def index(request):

    print(request.path_info)
    user_permission_dict=request.session.get('user_permission_dict')
    print(user_permission_dict)
    return HttpResponse('登录，并且有权限才能看见我')

def test(request):

    obj=models.User.objects.filter(username='杨明').first()
    # x=models.User2Role.objects.filter(user_id=obj.id)
    # [user2role]
    role_list=models.Role.objects.filter(users__user_id=obj.id)
    #[role]
    # permission_list=models.Permission2Action2Role.objects.filter(role__in=role_list).values('permission__url','action__code').annotate(c=Count('id'))
    permission_list=models.Permission2Action2Role.objects.filter(role__in=role_list).values('permission__url','action__code').distinct()
    # 个人的所有权限,并去重
    # 放在session中
    # index.html?md=GET

    # msg_dct=[
    #     {'permission__url':'/index.html','action__code':'GET'},
    #     {'permission__url':'/index.html','action__code':'POST'},
    #     {'permission__url':'/index.html','action__code':'Edit'},
    #     {'permission__url':'/index.html','action__code':'DEL'},
    #     {'permission__url':'/order.html','action__code':'GET'},
    #     {'permission__url':'/order.html','action__code':'POST'},
    #     {'permission__url':'/order.html','action__code':'DEL'},
    #     {'permission__url':'/order.html','action__code':'Edit'},
    # ]

    # user_permission_dict = {
    #     'index.html': ["GET", "POST", "DEL", "Edit"],
    #     'order.html': ["GET", "POST", "DEL", "Edit"]
    # }
    #
    # request.session['user_permission_dict']=user_permission_dict


def menu(request):
    """
    需要用户名或者用户ID,产出用户关联的所有菜单
    :param request:
    :return:
    """
    user=models.User.objects.filter(username='youqingbing').first()

    #所有菜单，处理成当前用户关联的菜单
    all_menu_list=models.Menu.objects.all().values('id','caption','parent_id')

    #当前用户所有的角色
    role_list=models.Role.objects.filter(users__user=user)

    #当前用户所有的权限
    permission_list=models.Permission2Action2Role.objects.filter(
        role__in=role_list).values(
        'permission_id',
        'permission__url','permission__menu_id','permission__caption').distinct()

    #将权限挂扣到菜单上
    all_menu_dict={}
    for row in all_menu_list:
        row['child']=[]      #添加孩子
        row['status']=False ##是否显示菜单
        row['opened']=False #当前默认菜单是否应该展开
        all_menu_dict[row['id']]=row

    for per in permission_list:
        if not per['permission__menu_id']: #没有父级id的时候，直接跳过
            continue
        item={
            'id':per['permission_id'],
            'caption':per['permission__caption'],
            'parent_id':per['permission__menu_id'],
            'url':per['permission__url'],
            'status':True,
            'opened':False

        }

        #
        # if re.match(per['permission__url'],request.path_info):
        if re.match(per['permission__url'],'/yuhao.html'):
            item['opened']=True


        #将权限挂扣到菜单上
        all_menu_dict[item['parent_id']]['child'].append(item)

        #将当前权限的前辈status等于True
        pid = item['parent_id']
        temp = pid  # 父亲ID
        while not all_menu_dict[temp]['status']:
            all_menu_dict[temp]['status'] = True
            temp=all_menu_dict[temp]['parent_id']
            if not temp:
                break

        #将当前权限的前辈opened等于True
        if item['opened']:
            temp1 = pid  # 父亲ID
            while not all_menu_dict[temp1]['opened']:
                all_menu_dict[temp1]['opened'] = True
                temp1 = all_menu_dict[temp1]['parent_id']
                if not temp1:
                    break

    #处理菜单和菜单之间的等级关系
    result=[]
    for row in all_menu_list:
        pid=row['parent_id']
        if pid:
            all_menu_dict[pid]['child'].append(row)
        else:
            result.append(row)

    #结构化处理结果
    for row in result:
        print(row['caption'],row['status'],row['opened'],row)

    #通过结构化处理结果，生成菜单

    def menu_tree(menu_list):
        tpl1 = """
           <div class='menu-item'>
               <div class='menu-header'>{0}</div>
               <div class='menu-body {2}'>{1}</div>
           </div>
           """
        tpl2="""
        <a href='{0}' class='{1}'>{2}</a>
        """
        menu_str=""
        for menu in menu_list:
            if not menu['status']:
                continue
            #menu 菜单，权限(url)
            if menu.get('url'):
               #权限
               menu_str += tpl2.format(menu['url'], 'active' if menu['opened'] else '', menu['caption'])
            else:
                #菜单
                if menu['child']:
                    child_html=menu_tree(menu['child'])
                else:
                    child_html=''
                menu_str+=tpl1.format(menu['caption'],child_html,'' if menu['opened'] else 'hide')

            # v=tpl1.format(menu['caption'],'所有孩子','是否隐藏')

        return menu_str
    menu_html=menu_tree(result)

    return render(request,'menu.html',{'menu_html':menu_html})