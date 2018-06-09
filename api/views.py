from django.shortcuts import render,HttpResponse
import json
from django.conf import settings
from repository import models
import hashlib
import time
from Crypto.Cipher import AES

def decrypt(msg):          #发送过来的是字节类型
    '''对发过来的数据解密'''
    key=b'asdasfasdasdf242'
    cipher=AES.new(key,AES.MODE_CBC,key)   #创建对象
    result=cipher.decrypt(msg)
    num=result[-1]
    data=result[0:-num]
    print(str(data,encoding='utf-8'))
    return str(data,encoding='utf-8')

def Api_AUTH(request):
    api_key_record = {
        'dasdsfsfsafasfasfsaf': 1241435252.23214,
    }  ####这个可以放在redis/memchache里面
    client_md5_time_key = request.META.get('Openkey')
    client_md5_key, client_ctime = client_md5_time_key.split('|')

    client_time = float(client_ctime)
    server_time = time.time()

    if server_time - client_time > 10:  ####第一关
        return HttpResponse('超时了')

    ############第二关
    temp = "%s|%s" % (settings, client_ctime)  ##按照用户端一样的生成md5值，然后验证
    m = hashlib.md5()
    m.update(bytes(temp, encoding='utf-8'))
    server_md5_key = m.hexdigest()
    if server_md5_key != client_md5_key:
        return HttpResponse('认证失败')
    for k in list(api_key_record.keys()):
        v = api_key_record[k]
        if server_time > v:
            del api_key_record[k]

    ########第三关：
    if client_md5_key in api_key_record:
        return ('已经来过')
    else:
        api_key_record[client_md5_time_key] = client_time + 10  ###这个可以结合redis/memchache，，因为是练习，就这样吧

        func(request)
def API_auth(func):
    '''装饰器验证'''
    def wrapper(request):
        api_key_record = {
            'dasdsfsfsafasfasfsaf': 1241435252.23214,
        }  ####这个可以放在redis/memchache里面
        client_md5_time_key = request.META.get('Openkey')
        client_md5_key, client_ctime = client_md5_time_key.split('|')

        client_time = float(client_ctime)
        server_time = time.time()

        if server_time - client_time > 10:  ####第一关
            return HttpResponse('超时了')

        ############第二关
        temp = "%s|%s" % (settings, client_ctime)  ##按照用户端一样的生成md5值，然后验证
        m = hashlib.md5()
        m.update(bytes(temp, encoding='utf-8'))
        server_md5_key = m.hexdigest()
        if server_md5_key != client_md5_key:
            return HttpResponse('认证失败')
        for k in list(api_key_record.keys()):
            v = api_key_record[k]
            if server_time > v:
                del api_key_record[k]

        ########第三关：
        if client_md5_key in api_key_record:
            return ('已经来过')
        else:
            api_key_record[client_md5_time_key] = client_time + 10  ###这个可以结合redis/memchache，，因为是练习，就这样吧
        func(request)
    return wrapper


@API_auth
def asset(request):
    '''
    对client端 ssh和socktet请求来的东西进行数据入库
    :param request:
    :return:
    '''
    # Api_AUTH(request)   #也可以通过装饰器
    if request.method =="GET":
        '''做个api验证'''
        return HttpResponse('给你数据接着')

    elif request.method=='POST':
        server_info=decrypt(request.body)
        server_info=json.loads(server_info)
        hostname=server_info['basic']['data']['hostname']
        server_obj=models.Server.objects.filter(hostname=hostname)
        if not server_obj:
            return HttpResponse('当前主机未录入')
        asset_obj=server_info.asset

        ##资产以前的资产信息
        disk_list=server_info.disk.all()
        # '''ps,以其中一条
        # sever_info[1]={'data':{
        #                  "5":{"slot":'5','caoactity':""384.239,"pd_type":'SATA','model':'SIAXNSDAS  Sumsung sf '}
        #                 "1":{"slot":'5','caoactity':""384.239,"pd_type":'SATA','model':'SIAXNSDAS  Sumsung sf '}
        #
        # }}
        # '''
        # ####处理：
        # '''比如比较硬盘
        # 1.根据新资产和原资产进行比较：新数据["5","1"]  老数据 ["4","5","6"]
        # 2.增加 ["1"],更新["5"],删除["4","6"]
        # 3.增加：
        #     sever_info中根据["1"]找到详细，然后入库
        #   删除：
        #     数据库中找到当前服务器的硬盘[4,6]
        #
        #
        # log_list=[]
        # dict_info={"slot":'5','capacity':""384.239,"pd_type":'SATA','model':'SIAXNSDAS  Sumsung sf ',}
        # obj
        #     if obj.capacity !=dict_info['capacity']
        #         log_list.append("硬盘容量由%s变更为%s"%s(obj.capacity,dict_info['capacity']))
        #         obh.capacity=dict_info['capacity']
        #     obj.save()
        #     models.log.object.create("".join(log_list))
        #
        # '''

        # for k,v in server_info.items():

        ###########################################ps 处理硬盘信息####################
        if not server_info['disk']['status']:
            models.ErrorLog.objects.create(content=server_info['disk']['data'],asset=server_obj.asset,title="%s采集错误信息"%hostname)
        #####################交集  创建   删除
        new_disk_dict=server_info['disk']['data']
        new_slot_list=list(new_disk_dict.keys())
        old_disk_list=models.Disk.objects.filter(server_obj=server_obj)
        old_slot_list=[]
        for item in old_disk_list:
            old_slot_list.append(item.slot)
        ##交集 :更新
        update_list=set(new_slot_list).intersection(old_slot_list)


        ##差集 ：创建
        create_list=set(new_slot_list).difference(old_slot_list)



        ##差集 ：
        del_list=set(old_slot_list).difference(new_slot_list)

        #删除
        if del_list:
            models.Disk.objects.filter(server_ob=server_obj,slot__in=del_list).delete()  #删掉
            models.AssetRecord.objects.create(asset_obj=server_obj.asset,content="移除硬盘：%s"%(".".join(del_list)))               ##写入日志

        #增加
        record_list = []
        for slot in create_list:
            disk_dict = new_disk_dict[slot]
            models.Disk.objects.create(**disk_dict)  ##增加
            temp = "新增硬盘：位置{slot},容量{capacity},型号{model},类型{pd_type}".format(**disk_dict)
            record_list.append(temp)
        if record_list:
            content = ":".join(record_list)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=content)

        #更新
        record_list=[]
        row_map={'capacity':'容量','pd_type':'类型','model':'型号'}
        for slot in update_list:
            new_disk_row=new_disk_dict[slot]
            old_disk_row=models.Disk.objects.filter(slot=slot,server_obj=server_obj).first()
            for k,v in new_disk_row.items():
                value=getattr(old_disk_row,k)
                if v !=value:
                    record_list.append("槽位%s，%s由%s变更为%s"%(slot,row_map[k],value,v))
                    setattr(old_disk_row,k,v)
            old_disk_row.save()
        if record_list:
            content = ":".join(record_list)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=content)

        ###########其他的查询结果都是同样的操作


    return HttpResponse('......')