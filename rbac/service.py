#!/usr/bin/env python
#encoding:utf-8
from rbac import models
from django.utils.safestring import mark_safe
import re
#生成菜单，权限html
#传入1，request.path_info
def menu(user_id,current_url):
    """
        根据用户ID，当前URL获取用户所有菜单以及权限，是否显示以及打开
        :param request:
        :return:
        """
    user = models.User.objects.filter(id=user_id).first()

    # 所有菜单，处理成当前用户关联的菜单
    all_menu_list = models.Menu.objects.all().values('id', 'caption', 'parent_id')

    # 当前用户所有的角色
    role_list = models.Role.objects.filter(users__user=user)

    # 当前用户所有的权限
    permission_list = models.Permission2Action2Role.objects.filter(
        role__in=role_list).values(
        'permission_id',
        'permission__url', 'permission__menu_id', 'permission__caption').distinct()

    # 将权限挂扣到菜单上
    all_menu_dict = {}
    for row in all_menu_list:
        row['child'] = []  # 添加孩子
        row['status'] = False  ##是否显示菜单
        row['opened'] = False  # 当前默认菜单是否应该展开
        all_menu_dict[row['id']] = row

    for per in permission_list:
        if not per['permission__menu_id']:  # 没有父级id的时候，直接跳过
            continue
        item = {
            'id': per['permission_id'],
            'caption': per['permission__caption'],
            'parent_id': per['permission__menu_id'],
            'url': per['permission__url'],
            'status': True,
            'opened': False

        }

        #
        if re.match(per['permission__url'],current_url):
            item['opened'] = True

        # 将权限挂扣到菜单上
        all_menu_dict[item['parent_id']]['child'].append(item)

        # 将当前权限的前辈status等于True
        pid = item['parent_id']
        temp = pid  # 父亲ID
        while not all_menu_dict[temp]['status']:
            all_menu_dict[temp]['status'] = True
            temp = all_menu_dict[temp]['parent_id']
            if not temp:
                break

        # 将当前权限的前辈opened等于True
        if item['opened']:
            temp1 = pid  # 父亲ID
            while not all_menu_dict[temp1]['opened']:
                all_menu_dict[temp1]['opened'] = True
                temp1 = all_menu_dict[temp1]['parent_id']
                if not temp1:
                    break

    # 处理菜单和菜单之间的等级关系
    result = []
    for row in all_menu_list:
        pid = row['parent_id']
        if pid:
            all_menu_dict[pid]['child'].append(row)
        else:
            result.append(row)

    # 结构化处理结果
    for row in result:
        print(row['caption'], row['status'], row['opened'], row)

    # 通过结构化处理结果，生成菜单

    def menu_tree(menu_list):
        tpl1 = """
               <div class='menu-item'>
                   <div class='menu-header'>{0}</div>
                   <div class='menu-body {2}'>{1}</div>
               </div>
               """
        tpl2 = """
            <a href='{0}' class='{1}'>{2}</a>
            """
        menu_str = ""
        for menu in menu_list:
            if not menu['status']:
                continue
            # menu 菜单，权限(url)
            if menu.get('url'):
                # 权限
                menu_str += tpl2.format(menu['url'], 'active' if menu['opened'] else '', menu['caption'])
            else:
                # 菜单
                if menu['child']:
                    child_html = menu_tree(menu['child'])
                else:
                    child_html = ''
                menu_str += tpl1.format(menu['caption'], child_html, '' if menu['opened'] else 'hide')

                # v=tpl1.format(menu['caption'],'所有孩子','是否隐藏')

        return menu_str
    menu_html = menu_tree(result)
    return menu_html

#simple_tag
def css():
    v="""
     <style>
        .hide{
            display: none;
        }
        .menu-body{
            margin-left: 20px;
        }

        .menu-body a{
            display: block;
        }

        .menu-body a.active{
            color: red;
        }
    </style>
    """
    return v

def js():
    v="""
    <script>
        $(function () {
            $(".menu-header").click(function () {
                $(this).next().removeClass('hide').parent().siblings().find(".menu-body").addClass("hide")

            })
        })
    </script>
    """
    return mark_safe(v)

#登录成功写入session
def permission_session(user_id,request):
    user_permission_dict = {
        '/ah-index.html': ["GET", "POST", "DEL", "Edit"],
        '/index-(\d+).html': ["GET", "POST", "DEL", "Edit"],
        '/order.html': ["GET", "POST", "DEL", "Edit"]
    }

    request.session['user_permission_dict'] = user_permission_dict
