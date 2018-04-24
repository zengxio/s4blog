#!/usr/bin/env python
#encoding:utf-8
def comment_tree(comment_list):
    """
    :param result: [{id,child:[}]
    :return:
    """
    comment_str="<div class='comment'>"
    for row in comment_list:
        tpl = "<div class='content'>%s</div>" % (row['content'])
        comment_str += tpl
        if row['child']:
            child_str=comment_tree(row['child'])
            comment_str+=child_str

    comment_str +="</div>"
    return comment_str

