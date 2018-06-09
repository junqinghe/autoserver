from django.shortcuts import render
from django.shortcuts import HttpResponse,redirect
from repository import models
# Create your views here.
import json

from datetime import datetime,date
class JsonCustomEncoder(json.JSONEncoder):
    def default(self,field):
        if isinstance(field,datetime):
            return field.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(field,date):
            return field.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self,field)

def curd(request):
    return render(request,'curd.html')

def curd_html(request):
    if request.method=='GET':
        table_config=[
            {'q': None, 'title': '选择', 'display': True,
             'text': {
                 'tpl': '<input type="checkbox" value="{k3}" />',
                 'kwargs': {'k3': '@id'}},
             'attrs': {'k3': '@id',
                       }
             },
            {'q':'id','title':'ID','display':True,'text':
                {'tpl':'{N1}',
                 'kwargs':{'N1':'@id'}
                },
             'attrs': {'editable':'true',
                       }
             },
            {'q': 'hostname', 'title': '主机名','display':True,'text':
                {'tpl':'{hostname}',
                 'kwargs':{'hostname':'@hostname'}
                },
             'attrs': {'editable': 'true',
                       }
             },
            {'q': 'create_at', 'title': '创建时间','display':True,'text':
                {'tpl':'想改就改{create_at}',
                 'kwargs':{'create_at':'@create_at'}
                },
             'attrs': {'editable': 'true',
                       }
             },
            # {'q': 'asset__name', 'title': '资产名','text':
            #     {'tpl':'{asset__name}',
            #      'kwargs':{'asset__name':'@asset__name'}
            #     }},
            {'q': 'asset__cabinet_num', 'title': '机柜号','display':False,'text':
                {'tpl':'{asset__cabinet_num}',
                 'kwargs':{'asset__cabinet_num':'@asset__cabinet_num'}
                },
             'attrs': {'editable': 'true', }
             },
            {'q': None, 'title':'操作','display':True,'text':
                {'tpl':'<a href="/backend/del?nid={nid}">删除</a>|<a<a href="/backend/add?nid={nid}>添加</a>',
                 'kwargs':{'nid':'@id'}
                }},
        ]

        value_list=[]
        for row in table_config:
            if row['q']:
                value_list.append(row['q'])
        print(value_list)
        server_list=models.Server.objects.values(*value_list)
        ret={
            'server_list':list(server_list),
            'table_config':table_config,

        }


        return HttpResponse(json.dumps(ret,cls=JsonCustomEncoder))

def asset(request):
    return render(request,'asset.html')

def asset_html(request):
    if request.method=='PUT':
        row_list=json.loads(str(request.body,encoding='utf-8'))
        for row in row_list:
            if row:
                id=row.pop('id')
                # print(id,row)
                models.Asset.objects.filter(id=id).update(**row)
        return HttpResponse('...')
    elif request.method == 'DELETE':
        idlist=request.body
        delist=json.loads(str(idlist,encoding='utf-8'))
        models.Asset.objects.filter(idc__in=delist)

        return HttpResponse('...')
    elif request.method=='GET':
        table_config=[
            {'q': None, 'title': '选择', 'display': True,
             'text': {
                 'tpl': '<input type="checkbox" value="{k3}" />',
                 'kwargs': {'k3': '@id'}},
             'attrs': { 'k3': '@id',}
             },
            {'q':'id','title':'ID','display':True,
             'text':{
                 'tpl':'{N1}',
                 'kwargs':{'N1':'@id'}},
             'attrs':{'k2':'@id',}
             },

            {'q':'device_type_id', 'title': '资产类型','display':True,
             'text':{'tpl':'{n1}',
                     'kwargs':{'n1':'@@device_type_choices'}},
             'attrs': {'origin': '@device_type_id', 'editable':'true','name':'device_type_id','edit_type':'select','global_key': 'device_type_choices'}
             },
            {'q': 'create_date', 'title': '创建时间','display':True,
             'text':
                {'tpl':'想{n1}',
                 'kwargs':{'n1':'@create_date'},},
             'attrs': {'origin': '@create_date','editable':'true','name':'create_date'}
             },
            {'q': 'idc_id', 'title': '机房', 'display': None,
             'text': { },
             'attrs': { },
             },
            {'q': 'idc__name', 'title': '机房', 'display': True,
             'text': {'tpl':'{n1}',
                 'kwargs':{'n1':'@idc__name'},},
             'attrs': {'origin':'@idc_id','editable':'true','edit_type':'select','global_key':'idc_choice','name':'idc_id'},
             },
            {'q': 'device_status_id', 'title': '资产状态','display':True,
             'text': {'tpl':'{n1}','kwargs':{'n1':'@@device_status_choices'}},
             'attrs': { 'origin':'@device_status_id', 'editable':'true','edit_type':'select','global_key':'device_status_choices', 'name':'device_status_id'}
             },
            {'q': None, 'title':'操作','display':True,'text':
                {'tpl':'<a href="/backend/del?nid={nid}">删除</a>|<a<a href="/backend/add?nid={nid}>添加</a>',
                 'kwargs':{'nid':'@id'}
                }},
        ]


        value_list=[]
        for row in table_config:
            if row['q']:
                value_list.append(row['q'])
        print(value_list)
        server_list=models.Asset.objects.values(*value_list)
        ret={
            'server_list':list(server_list),
            'table_config':table_config,
            'global_dict':{
                'device_type_choices': models.Asset.device_type_choices,
                'device_status_choices': models.Asset.device_status_choices,
                'idc_choice':list(models.IDC.objects.values_list('id','name')),
            }
        }


        return HttpResponse(json.dumps(ret,cls=JsonCustomEncoder))


def charts(request):
    return render(request,'charts.html')

def shishi(request):
    return render(request,'shishi.html')