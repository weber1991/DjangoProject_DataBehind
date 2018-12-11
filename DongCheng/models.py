from django.db import models

# Create your models here.



class rz_service(models.Model):
    '''
    人资的业务类型
    '''
    serial = models.IntegerField(verbose_name='业务编号', primary_key=True)
    serialchar = models.CharField(verbose_name='业务号码', max_length=16,null=True,blank=True)
    typename = models.CharField(verbose_name='业务名称', max_length=512,null=True,blank=True)
    nownumber = models.IntegerField(verbose_name='当前等候人数(实时更新)',null=True,blank=True)

    def __str__(self):
        return self.typename

    class Meta():
        ordering = ['serial']
        verbose_name = '人资的业务类型'
        verbose_name_plural = verbose_name

class rz_queuelist(models.Model):
    id = models.CharField(max_length=255,verbose_name='票号ID', null=True,blank=True)
    serial = models.CharField(max_length=255,verbose_name='业务编号', null=True,blank=True)
    number = models.CharField(verbose_name='票号', null=True,blank=True, max_length=16)
    cometime = models.DateTimeField(verbose_name='取号时间', primary_key=True)
    serveno = models.CharField(max_length=255,verbose_name='工作人员编号', null=True,blank=True)
    servetime = models.DateTimeField(verbose_name='服务时间', null=True,blank=True)
    endtime = models.DateTimeField(verbose_name='结束时间', null=True,blank=True)
    hjcounter = models.CharField(max_length=255,verbose_name='hj数',null=True,blank=True)
    status = models.CharField(max_length=255,verbose_name='票号状态', null=True,blank=True)

    def __str__(self):
        return self.number

    class Meta():
        verbose_name = '当天票号'
        verbose_name_plural = verbose_name
        ordering = ['cometime']

class rz_queuehist(models.Model):
    id = models.CharField(max_length=255,verbose_name='票号ID',null=True,blank=True)
    serial = models.CharField(max_length=255,verbose_name='业务编号',null=True,blank=True)
    number = models.CharField(verbose_name='票号',max_length=16, null=True,blank=True)
    counter = models.CharField(max_length=255,verbose_name='窗口号',null=True,blank=True)
    cometime = models.DateTimeField(verbose_name='取号时间', primary_key=True)
    servetime = models.DateTimeField(verbose_name='叫号时间', null=True,blank=True)
    serveno = models.CharField(max_length=255,verbose_name='工作人员编号', null=True,blank=True)
    endtime = models.DateTimeField(verbose_name='作废时间', null=True,blank=True)
    isHJ = models.CharField(max_length=255,verbose_name='hj标志', null=True,blank=True)
    hjtime = models.DateTimeField(verbose_name='hj时间', null=True,blank=True)
    finished = models.CharField(max_length=255,verbose_name='完成标志', null=True,blank=True)

    def __str__(self):
        return self.number

    class Meta():
        verbose_name = '票号历史'
        verbose_name_plural = verbose_name
        ordering = ['cometime']

class rz_counter(models.Model):
    counterno = models.CharField(max_length=255,verbose_name='窗口编号', primary_key=True)
    serial = models.CharField(max_length=255,verbose_name='业务编号', null=True,blank=True)
    number = models.CharField(verbose_name='当前办理票号',max_length=64, null=True,blank=True) # 需要定时刷新
    state = models.CharField(verbose_name='窗口状态', null=True,blank=True, max_length=16)
    serveno = models.CharField(max_length=255,verbose_name='窗口人员编号', null=True,blank=True)

    def __str__(self):
        return self.counterno

    class Meta():
        verbose_name = '窗口关系表'
        verbose_name_plural = verbose_name
        ordering = ['counterno']

class gs_queuehist(models.Model):
    serial = models.CharField(max_length=255,verbose_name='业务编号')
    number = models.CharField(verbose_name='票号',max_length=64)
    counter = models.CharField(max_length=255,verbose_name='窗口号',null=True,blank=True)
    cometime = models.DateTimeField(verbose_name='取号时间',primary_key=True)
    servetime = models.DateTimeField(verbose_name='叫号时间', null=True,blank=True)
    serveno = models.CharField(max_length=255,verbose_name='工作人员编号',null=True,blank=True)
    endtime = models.DateTimeField(verbose_name='作废时间', null=True,blank=True)
    isdo = models.CharField(max_length=255,verbose_name='是否办理', null=True,blank=True)

    def __str__(self):
        return self.number

    class Meta():
        verbose_name = '票号历史'
        verbose_name_plural = verbose_name
        ordering = ['-cometime']

class gs_servetype(models.Model):
    serial = models.CharField(max_length=255,verbose_name='业务编号', primary_key=True)
    serialchar = models.CharField(verbose_name='业务编码', max_length=16,null=True,blank=True)
    typeno = models.CharField(max_length=255,verbose_name='窗口编号', null=True,blank=True)
    typename = models.CharField(verbose_name='窗口名称', null=True,blank=True, max_length=255)
    apartment = models.CharField(max_length=255,verbose_name='部门编码', null=True,blank=True)
    apartmentname = models.CharField(verbose_name='部门名称', null=True,blank=True, max_length=255)
    nownumber = models.CharField(max_length=255,verbose_name='等候人数',null=True,blank=True)
    starttime = models.CharField(max_length=255,verbose_name='业务开始时间', null=True,blank=True)
    endtime = models.CharField(max_length=255,verbose_name='结束时间', null=True,blank=True)

    def __str__(self):
        return self.serial

    class Meta():
        verbose_name = '业务与窗口关系表'
        verbose_name_plural = verbose_name
        ordering = ['serial']



# # 这个模型的key有点疑惑
# class gs_queue(models.Model):
#     serial = models.IntegerField(verbose_name='业务编号')


class zx_piaohaotongji(models.Model):
    xph = models.CharField(verbose_name='取票号', null=True,blank=True,max_length=64)
    ywmc = models.CharField(verbose_name='业务名称',null=True,blank=True, max_length=256)
    creationtime = models.DateTimeField(verbose_name='取号时间',null=True,blank=True)
    qupiaotongji_id = models.CharField(verbose_name='取票ID',primary_key=True, max_length=255)
    status = models.CharField(max_length=8,verbose_name='状态', null=True,blank=True)
    cardno = models.CharField(max_length=32, verbose_name='身份证', null=True,blank=True)
    peoplename = models.CharField(max_length=32, verbose_name='名称', null=True,blank=True)
    dtbs = models.CharField(max_length=16, verbose_name='办事厅号', null=True,blank=True)
    ywbm = models.CharField(max_length=8, verbose_name='业务编码',null=True,blank=True)

    def __str__(self):
        return self.xph

    class Meta():
        verbose_name = '中心的票号统计表'
        verbose_name_plural = verbose_name
        ordering = ['creationtime']


class zx_pdqk(models.Model):
    no = models.CharField(max_length=255,verbose_name='编号',null=True,blank=True)
    name = models.CharField(max_length=255,verbose_name='名称',primary_key=True)
    last = models.CharField(max_length=255,verbose_name='最后票号',null=True,blank=True)
    ddrs = models.CharField(max_length=255,verbose_name='未知1',null=True,blank=True)
    createtime = models.DateTimeField(verbose_name='创建时间', null=True,blank=True)
    remainder = models.CharField(max_length=255,verbose_name='未知2',null=True,blank=True)
    dtbs = models.CharField(max_length=255,verbose_name='办事厅',null=True,blank=True)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = '中心的业务配置情况'
        verbose_name_plural = verbose_name
        ordering = ['createtime']


class ga_service(models.Model):
    id = models.CharField(max_length=255,primary_key=True,verbose_name='关键ID')
    code = models.CharField(max_length=255, null=True, blank=True, verbose_name='业务编码')
    parent = models.CharField(max_length=255, null=True, blank=True, verbose_name='业务名称')
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name='业务名称')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '公安业务表'
        verbose_name_plural = verbose_name
        ordering = ['id']

class ga_window(models.Model):
    id = models.CharField(max_length=255, verbose_name='关联ID', primary_key=True)
    code = models.CharField(max_length=255, null=True, blank=True, verbose_name='窗口编码')
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name='窗口名称')
    status = models.CharField(max_length=255, null=True, blank=True, verbose_name='窗口状态')
    sort_category = models.CharField(max_length=255, null=True, blank=True, verbose_name='窗口类型')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '窗口类型'
        verbose_name_plural = verbose_name
        ordering = ['id']


class ga_queuehist(models.Model):
    id = models.CharField(max_length=255, primary_key=True, verbose_name='唯一ID')
    code = models.CharField(max_length=255, null=True, blank=True, verbose_name='票号')
    service = models.CharField(max_length=255, null=True, blank=True, verbose_name='业务ID')
    window = models.CharField(max_length=255, null=True, blank=True, verbose_name='窗口ID')
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    id_card = models.CharField(max_length=255, null=True, blank=True, verbose_name='身份证')
    phone = models.CharField(max_length=255, null=True, blank=True, verbose_name='手机号码')
    appointment = models.CharField(max_length=255, null=True, blank=True, verbose_name='预约手机')
    acd = models.DateTimeField(null=True, blank=True, verbose_name='预约时间')
    fcd = models.DateTimeField(null=True, blank=True, verbose_name='取号时间')
    ssd = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    lcd = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')

    def __str__(self):
        return self.ssd

    class Meta:
        verbose_name = '公安票号历史'
        verbose_name_plural = verbose_name
        ordering = ['id']


class base_data(models.Model):
    what = models.CharField(max_length=255, primary_key=True)
    count = models.IntegerField(verbose_name='数量', null=True, blank=True)
    start = models.CharField(max_length=255, null=True, blank=True)
    end = models.CharField(max_length=255, null=True, blank=True)
    changtime = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        self.what

    class Meta:
        verbose_name = '基础数据'
        verbose_name_plural = verbose_name