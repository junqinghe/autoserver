from django.db import models
import datetime

# Create your models here.

class UserProfile(models.Model):
    username=models.CharField(max_length=32)
    email=models.EmailField(max_length=32,null=True,blank=True)

    def __str__(self):
        return self.username

class Department(models.Model):
    name = models.CharField(max_length=64, unique=True)
    manager=models.ForeignKey('UserProfile',related_name='dep')

    def __str__(self):
        return self.name

class BusinessUnit(models.Model):
    '''业务线'''
    name=models.CharField(verbose_name='业务组名',max_length=32,unique=True)
    dep = models.ForeignKey('Department', related_name='business_unit')
    user=models.ForeignKey('UserProfile',verbose_name='管理者',null=True,blank=True)

    class Meta:
        verbose_name_plural = '业务线'
    def __str__(self):
        return self.name

class User2BusinessUnit(models.Model):
    user=models.ForeignKey('UserProfile')
    bu=models.ForeignKey('BusinessUnit')

    def __str__(self):
        return '用户业务线关系表'

class Asset(models.Model):
    device_type_choices = (
        (1, '服务器'),
        (2, '路由器'),
        (3, '安全设备'),
 )
    device_status_choices=(
        (1, '上架'),
        (2, '在线'),
        (3, '离线'),
        (4,'下架'),
    )
    name = models.CharField(max_length=32, unique=True)
    device_type_id=models.IntegerField(choices=device_type_choices,default=1)
    device_status_id=models.IntegerField(choices=device_status_choices,default=1)
    cabinet_num=models.CharField(verbose_name='机柜号',max_length=32,null=True,blank=True)
    cabinet_order= models.CharField(verbose_name='机柜中序号', max_length=32, null=True, blank=True)

    idc=models.ForeignKey('IDC',verbose_name='IDC机房',null=True,blank=True)
    business_unit=models.ForeignKey('BusinessUnit',verbose_name='属于的业务组',null=True,blank=True)

    create_date=models.DateTimeField(blank=True,auto_now_add=True)
    update_date=models.DateTimeField(blank=True,auto_now=True)
    tag=models.ManyToManyField('Tag')

    class Meta:
        verbose_name = '资产总表'
        verbose_name_plural = "资产总表"

    def __str__(self):
        return '<id:%s name:%s>' % (self.id, self.name)




class IDC(models.Model):
    """机房"""

    name = models.CharField(u'机房名称', max_length=64, unique=True)
    floor = models.IntegerField(verbose_name='楼层',default=1)

    class Meta:
        verbose_name_plural='机房表'

    def __str__(self):
        return self.name




class Server(models.Model):
    """服务器设备"""
    asset=models.OneToOneField('Asset')
    sub_assset_type_choices = (
        (0, 'PC服务器'),
        (1, '刀片机'),
        (2, '小型机'),
    )
    sub_asset_type = models.SmallIntegerField(choices=sub_assset_type_choices, verbose_name="服务器类型", default=0)
    hostname=models.CharField(max_length=32,unique=True)
    system=models.CharField(max_length=32,default='Linux')
    version=models.CharField(verbose_name='系统版本',max_length=32)
    create_at=models.DateTimeField(verbose_name='创建时间',auto_now_add=True,null=True,blank=True)
    update_at = models.DateTimeField(verbose_name='上次修改时间',auto_now=True)
    class Meta:
        verbose_name_plural='服务器'

    def __str__(self):
        return '%s id:%s' % (self.asset.name, self.id)

class NetDevice(models.Model):
    '''网络设备'''
    name=models.CharField(max_length=32)
    asset=models.OneToOneField(Asset)
    intranet_ip = models.GenericIPAddressField(verbose_name='内网IP', blank=True, null=True)
    model = models.CharField(verbose_name='型号', max_length=128, null=True, blank=True)
    port_num = models.SmallIntegerField(verbose_name='端口个数', null=True, blank=True)

    def __str__(self):
        return self.name

class Disk(models.Model):
    # slot=models.CharField(max_length=32)
    # capacity=models.FloatField(verbose_name='磁盘容量(G)')
    # model=models.CharField(max_length=32,verbose_name='磁盘型号',null=True,blank=True)
    #
    # disk_iface_choice=(
    #     ('SATA', 'SATA'),
    #     ('SAS', 'SAS'),
    #     ('SCSI', 'SCSI'),
    #     ('SSD', 'SSD'),
    # )
    # iface_type = models.CharField(verbose_name='接口类型', max_length=64, choices=disk_iface_choice, default='SAS')
    # sv=models.ForeignKey('Server',related_name='disk')
    #
    # def __str__(self):
    #     return 'sv:%s ;slot:%s ;capacity:%s'%(self.sv,self.slot,self.capacity)
    slot=models.CharField('槽位',max_length=8)
    model=models.CharField('磁盘型号',max_length=32)
    capacity=models.CharField('容量',max_length=32)
    pd_type=models.CharField('磁盘类型',max_length=32)
    server_obj=models.ForeignKey('Server',related_name="disk")

    class Meta:
        verbose_name_plural = "硬盘"

class Cpu(models.Model):
    '''cpu组件'''
    sv=models.ForeignKey('Server',related_name='cpu')
    cpu_count=models.SmallIntegerField(verbose_name='核数')
    cpu_physical_count=models.SmallIntegerField(verbose_name='物理个数')
    cpu_model = models.CharField(verbose_name='CPU型号', max_length=128, blank=True)

    def __str__(self):
        return self.cpu_model

class Nic(models.Model):
    """网卡组件"""
    # sv = models.ForeignKey('Server', related_name='nic')
    # name = models.CharField(verbose_name='网卡名', max_length=64, blank=True, null=True)
    # sn = models.CharField(verbose_name='SN号', max_length=128, blank=True, null=True)
    # model = models.CharField(verbose_name='网卡型号', max_length=128, blank=True, null=True)
    # macaddress = models.CharField(verbose_name='MAC', max_length=64, unique=True)
    # def __str__(self):
    #     return '服务器：%s ;网卡：%s'%(self.sv,self.name)
    name=models.CharField('网卡名称',max_length=128)
    hwaddr=models.CharField('网卡MAC地址',max_length=64)
    netmask=models.CharField(max_length=64)
    ipaddrs=models.CharField('ip地址',max_length=256)
    up=models.BooleanField(default=False)
    server_obj=models.ForeignKey('Server',related_name='nic')

    class Meta:
        verbose_name_plural="网卡表"


class Tag(models.Model):
    '''资产标签'''
    name=models.CharField(verbose_name='标签',max_length=32,unique=True)

    def __str__(self):
        return self.name

class Manufactory(models.Model):
    """厂商"""

    manufactory = models.CharField(u'厂商名称', max_length=64, unique=True)


    def __str__(self):
        return self.manufactory

    class Meta:
        verbose_name = '厂商'
        verbose_name_plural = "厂商"

class Memory(models.Model):
    sv=models.ForeignKey('Server')
    manufacturer=models.ForeignKey('Manufactory',null=True,blank=True)
    capacity=models.FloatField(verbose_name='内存容量',null=True,blank=True)
    slot=models.CharField(verbose_name='接口',max_length=24)
    sn = models.CharField(verbose_name='主板sn', max_length=64)
    speed=models.CharField(verbose_name='运行速度',max_length=38,null=True,blank=True)
    model=models.CharField(verbose_name='内存型号',max_length=38,null=True,blank=True)
    def __str__(self):
        return '服务器：%s 内存'%(self.sv.hostname)

class AssetRecord(models.Model):
    """资产事件"""
    asset_obj=models.ForeignKey('Asset',related_name='ar')
    content=models.TextField(null=True)
    creator=models.ForeignKey('UserProfile',null=True,blank=True)
    create_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "资产变更"
    # name = models.CharField(u'事件名称', max_length=48,null=True,blank=True)
    # event_type_choices = (
    #     (1, u'硬件变更'),
    #     (2, u'新增配件'),
    #     (3, u'设备下线'),
    #     (4, u'设备上线'),
    #     (5, u'定期维护'),
    #     (6, u'业务上线\更新\变更'),
    #     (7, u'其它'),
    # )
    # event_type = models.SmallIntegerField(u'事件类型', choices=event_type_choices)
    # asset_obj = models.ForeignKey('Asset',null=True,blank=True)
    # detail = models.TextField(u'事件详情')
    # date = models.DateTimeField(u'事件时间', auto_now_add=True)
    # user = models.ForeignKey('UserProfile', verbose_name=u'事件源')
    # create_date = models.DateField(auto_now_add=True)
    #
    # def __str__(self):
    #     return self.name
    #
    # class Meta:
    #     verbose_name = '事件纪录'
    #     verbose_name_plural = "事件纪录"
    #
    # def colored_event_type(self):
    #     if self.event_type == 1:
    #         cell_html = '<span style="background: orange;">%s</span>'
    #     elif self.event_type == 2:
    #         cell_html = '<span style="background: yellowgreen;">%s</span>'
    #     else:
    #         cell_html = '<span >%s</span>'
    #     return cell_html % self.get_event_type_display()
    #
    # colored_event_type.allow_tags = True
    # colored_event_type.short_description = u'事件类型'

class ErrorLog(models.Model):
    '''错误日志，如：agent采集数据错误或运行错误'''
    asset=models.ForeignKey('Asset',null=True,blank=True)
    title=models.CharField(max_length=16)
    content=models.TextField()
    create_date=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural='错误日志表'

    def __str__(self):
        return self.title


