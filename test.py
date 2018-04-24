# # #!/usr/bin/env python
# # #coding:utf-8
# mag_list=[
#     {'id':1,'content':'xxx','parent_id':None},
#     {'id':2,'content':'xxx','parent_id':None},
#     {'id':3,'content':'xxx','parent_id':None},
#     {'id':4,'content':'xxx','parent_id':1},
#     {'id':5,'content':'xxx','parent_id':1},
#     {'id':6,'content':'xxx','parent_id':2},
#     {'id':7,'content':'xxx','parent_id':5},
#     {'id':8,'content':'xxx','parent_id':3},
#
# ]
# result=[]
# msg_list_dict={}
# for i in mag_list:
#     i['child']=[]
#     msg_list_dict[i['id']]=i
#     pid=i['parent_id']
#     if pid:
#         msg_list_dict[pid]['child'].append(i)
#     else:
#         result.append(i)
#
#
# for v in result:
#     print(v)
#
#
#
#
#
# # v=[item.setdefault('child',[]) for item in mag_list]
# # print(mag_list)
#
# '''
# msg_list=[
# {'id':1,'content':'xxx','parent_id':None,
# 'child':[{'id':4,'content':'xxx','parent_id':1},
# {'id':5,'content':'xxx','parent_id':1,
# 'child':[{'id':7,'content':'xxx','parent_id':5}]},]},
# {'id':2,'content':'xxx','parent_id':None,
# 'child':[{'id':6,'content':'xxx','parent_id':2}]},
# {'id':3,'content':'xxx','parent_id':None,
# 'child':[{'id':8,'content':'xxx','parent_id':3}]},
#
# ]
# '''
#




msg_dct=[
    {'permission__url':'/index.html','action__code':'GET'},
    {'permission__url':'/index.html','action__code':'POST'},
    {'permission__url':'/index.html','action__code':'Edit'},
    {'permission__url':'/index.html','action__code':'DEL'},
    {'permission__url':'/order.html','action__code':'GET'},
    {'permission__url':'/order.html','action__code':'POST'},
    {'permission__url':'/order.html','action__code':'DEL'},
    {'permission__url':'/order.html','action__code':'Edit'},
]

# user_permission_dict = {
#     'index.html': ["GET", "POST", "DEL", "Edit"],
#     'order.html': ["GET", "POST", "DEL", "Edit"]
# }


v={}

for i in msg_dct:
    if i['permission__url'] not in v:
        v[i['permission__url']] = [i['action__code'],]

    elif i['action__code'] not in v[i['permission__url']]:
        v[i['permission__url']].append(i['action__code'])

print(v)

