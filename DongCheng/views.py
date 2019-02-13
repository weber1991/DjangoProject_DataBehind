from __future__ import unicode_literals
import math
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from pyecharts import Line3D, Bar, Pie, Kline, Line
from DongCheng.models import *
import datetime, time
from datetime import timedelta


REMOTE_HOST = "https://pyecharts.github.io/assets/js"


def get_date(year, month = 1, day = 1):
    try:
        date = datetime.datetime(int(year),int(month),int(day),0,0)
        return date
    except:
        return False

# 官方demo
def index_dc(req):
    print(time.time())
    today = datetime.datetime.strptime(time.strftime("%Y-%m-%d"), '%Y-%m-%d')
    day_7 = today - datetime.timedelta(days = 7)
    day_31 = today - datetime.timedelta(days = 31)
    day_365 = today - datetime.timedelta(days = 365)


    zx_count_today = zx_piaohaotongji.objects.filter(creationtime__gte=today).count()
    rz_count_today = rz_queuehist.objects.filter(endtime__gte=today).count()
    gs_count_today = gs_queuehist.objects.filter(endtime__gte=today).count()
    ga_count_today = ga_queuehist.objects.filter(ssd__gte=today).count()

    # print("************",time.time())
    # print(len(zx_piaohaotongji.objects.filter(creationtime__gte=day_365)))
    # print("************",time.time())
    # print(zx_piaohaotongji.objects.filter(creationtime__gte=day_365).count())
    # print("************",time.time())

    # 周时间不计算七天，而是计算每周第一天和最后一天
    # zx_count_7 = base_data.objects.get(what='zx_count_7').count
    # rz_count_7 = base_data.objects.get(what='rz_count_7').count
    # gs_count_7 = base_data.objects.get(what='gs_count_7').count
    # ga_count_7 = base_data.objects.get(what='ga_count_7').count

    # 月时间不计算31天，而是计算每个月开始
    # zx_count_31 = base_data.objects.get(what='zx_count_31').count
    # rz_count_31 = base_data.objects.get(what='rz_count_31').count
    # gs_count_31 = base_data.objects.get(what='gs_count_31').count
    # ga_count_31 = base_data.objects.get(what='ga_count_31').count

    # 年份不用365天，而是使用大于今年1月1日
    # zx_count_365 = base_data.objects.get(what='zx_count_365').count
    # rz_count_365 = base_data.objects.get(what='rz_count_365').count
    # gs_count_365 = base_data.objects.get(what='gs_count_365').count
    # ga_count_365 = base_data.objects.get(what='ga_count_365').count

    # 构造今年1月1号
    now = datetime.datetime.now()
    now_year = get_date(now.year)
    now_month = get_date(now_year,now_month)
    now_week_start_date = now - timedelta(days=now.weekday())
    now_week_start = get_date(now.year, now.month, now_week_start_date.day)

    zx_count_7 = zx_piaohaotongji.objects.filter(creationtime__gte=now_week_start).count()
    rz_count_7 = rz_queuehist.objects.filter(endtime__gte=now_week_start).count()
    gs_count_7 = gs_queuehist.objects.filter(endtime__gte=now_week_start).count()
    ga_count_7 = ga_queuehist.objects.filter(ssd__gte=now_week_start).count()
    
    zx_count_31 = zx_piaohaotongji.objects.filter(creationtime__gte=now_month).count()
    rz_count_31 = rz_queuehist.objects.filter(endtime__gte=now_month).count()
    gs_count_31 = gs_queuehist.objects.filter(endtime__gte=now_month).count()
    ga_count_31 = ga_queuehist.objects.filter(ssd__gte=now_month).count()

    zx_count_365 = zx_piaohaotongji.objects.filter(creationtime__gte=now_year).count()
    rz_count_365 = rz_queuehist.objects.filter(endtime__gte=now_year).count()
    gs_count_365 = gs_queuehist.objects.filter(endtime__gte=now_year).count()
    ga_count_365 = ga_queuehist.objects.filter(ssd__gte=now_year).count()

    print(time.time())
    context = dict(
        zx_count_today = zx_count_today,
        rz_count_today = rz_count_today,
        gs_count_today = gs_count_today,
        ga_count_today = ga_count_today,
        count_today = rz_count_today + gs_count_today + zx_count_today + ga_count_today,
        count_7 = rz_count_7 + gs_count_7 + zx_count_7 + ga_count_7,
        count_31 = rz_count_31 + gs_count_31 + zx_count_31 + ga_count_31,
        count_365 = rz_count_365 + gs_count_365 + zx_count_365 + ga_count_365,
    )
    return render(req, 'DongCheng/index_dc.html', context)

def bumen_data_show(req):
    if req.method == 'GET':
        return render(req, 'DongCheng/bumen_data_show.html', {})
    else:
        bumen = req.POST.get("bumen", '')
        start = req.POST.get("start", None)
        end = req.POST.get("end", None)
        if start == '':
            start = time.strftime('%Y-%m-%d')
        if end == '':
            end = time.strftime('%Y-%m-%d')

        print(start,end)
        if bumen == 'rz':
            rz_bar = rz_serial_bar(start, end)
            rz_pie = rz_count_pie(start, end)
            rz_line = rz_day_line(start, end)
            context = dict(
                host=REMOTE_HOST,  # 获取所有JS文件的地址
                bar_demo=rz_bar.render_embed(),
                bar_script_list=rz_bar.get_js_dependencies(),
                pie_demo = rz_pie.render_embed(),
                pie_script_list = rz_pie.get_js_dependencies(),
                line_demo = rz_line.render_embed(),
                line_script_list = rz_line.get_js_dependencies(),
            )
        if bumen == 'zx':
            zx_bar = zx_service_bar(start, end)
            zx_line = zx_day_line(start, end)
            context = dict(
                host=REMOTE_HOST,  # 获取所有JS文件的地址
                bar_demo=zx_bar.render_embed(),
                bar_script_list=zx_bar.get_js_dependencies(),
                line_demo = zx_line.render_embed(),
                line_script_list = zx_line.get_js_dependencies(),
            )
        if bumen == 'gs':
            temp_bar = gs_service_bar(start, end)
            temp_pie = gs_window_pie(start, end)
            temp_line = gs_day_line(start, end)
            context = dict(
                host=REMOTE_HOST,  # 获取所有JS文件的地址
                bar_demo=temp_bar.render_embed(),
                bar_script_list=temp_bar.get_js_dependencies(),
                pie_demo=temp_pie.render_embed(),
                pie_script_list=temp_pie.get_js_dependencies(),
                line_demo=temp_line.render_embed(),
                line_script_list=temp_line.get_js_dependencies(),
            )
        if bumen == 'ga':
            temp_bar = ga_service_bar(start, end)
            temp_pie = ga_window_pie(start, end)
            temp_line = ga_day_line(start, end)
            context = dict(
                host=REMOTE_HOST,  # 获取所有JS文件的地址
                bar_demo=temp_bar.render_embed(),
                bar_script_list=temp_bar.get_js_dependencies(),
                pie_demo = temp_pie.render_embed(),
                pie_script_list = temp_pie.get_js_dependencies(),
                line_demo = temp_line.render_embed(),
                line_script_list = temp_line.get_js_dependencies(),
            )
        if bumen == 'all':
            temp_bar = all_bumen_bar(start, end)
            temp_line = all_day_line(start, end)
            context = dict(
                host=REMOTE_HOST,  # 获取所有JS文件的地址
                bar_demo=temp_bar.render_embed(),
                bar_script_list=temp_bar.get_js_dependencies(),
                line_demo = temp_line.render_embed(),
                line_script_list = temp_line.get_js_dependencies(),
            )
        context["bumen"] = bumen
        return render(req, 'DongCheng/bumen_data_show.html', context)

def all_bumen_bar(start = None, end = None):
    print(time.time())
    try:
        starttime = datetime.datetime.strptime(start, '%Y-%m-%d')
    except:
        starttime = time.strftime("%Y-%m-%d 00:00:00")
        starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d 00:00:00')
    try:
        endtime = datetime.datetime.strptime(end, '%Y-%m-%d')+ datetime.timedelta(days=1)
    except:
        endtime = time.strftime("%Y-%m-%d 23:59:59")
        endtime = datetime.datetime.strptime(endtime, '%Y-%m-%d 23:59:59')


    print(starttime,endtime)
    zx_piaohao_list = zx_piaohaotongji.objects.filter(creationtime__gte=starttime, creationtime__lte=endtime)
    rz_queue_list = rz_queuehist.objects.filter(hjtime__gte=starttime, hjtime__lte=endtime)
    ga_queue_list = ga_queuehist.objects.filter(ssd__gte=starttime, ssd__lte=endtime)
    gs_queue_list = gs_queuehist.objects.filter(endtime__gte=starttime, endtime__lte=endtime)

    print(zx_piaohao_list)
    bumen_name_list = []
    bumen_count_list = []

    bumen_name_list.append('综合服务中心')
    bumen_count_list.append(zx_piaohao_list.count())
    bumen_name_list.append('人力资源局')
    bumen_count_list.append(rz_queue_list.count())
    bumen_name_list.append('公安分局')
    bumen_count_list.append(ga_queue_list.count())
    bumen_name_list.append('工商分局')
    bumen_count_list.append(gs_queue_list.count())

    bumen_count_all = zx_piaohao_list.count() + rz_queue_list.count() + gs_queue_list.count() + ga_queue_list.count()

    title = "东城街道行政办事" + start + "至" + end + "受理情况"
    bar = Bar(title,subtitle="总业务量为"+ str(bumen_count_all),subtitle_color='#F00',subtitle_text_size=16, height=600, width=1920, title_pos="center", )
    bar.add("业务量",
            bumen_name_list,
            bumen_count_list,
            is_label_show=True,
            legend_pos="left",
            xaxis_interval=0,  # 设置为0，强制显示所有标签
            xaxis_rotate=0,  # 倾斜角度：90~-90
            )
    print(bumen_name_list)
    print(bumen_count_list)
    print(time.time())
    return bar

def all_day_line(start = None, end = None):
    try:
        starttime = datetime.datetime.strptime(start, '%Y-%m-%d')
    except:
        starttime = time.strftime("%Y-%m-%d 00:00:00")
        starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d 00:00:00')
    try:
        endtime = datetime.datetime.strptime(end, '%Y-%m-%d')+ datetime.timedelta(days=1)
    except:
        endtime = time.strftime("%Y-%m-%d 23:59:59")
        endtime = datetime.datetime.strptime(endtime, '%Y-%m-%d 23:59:59')

    day_count = (endtime-starttime).days

    print(day_count)
    # delta = datetime.timedelta(days=1)
    day_list = []
    day_count_list_zx = []
    day_count_list_rz = []
    day_count_list_ga = []
    day_count_list_gs = []
    all_count = 0
    for i in range(0,day_count):
        temp_time1 = starttime + datetime.timedelta(days=i)
        temp_time2 = starttime + datetime.timedelta(days=i + 1)
        temp_count_zx = zx_piaohaotongji.objects.filter(creationtime__gte=temp_time1, creationtime__lte=temp_time2).count()
        temp_count_rz = rz_queuehist.objects.filter(hjtime__gte=temp_time1, hjtime__lte=temp_time2).count()
        temp_count_ga = ga_queuehist.objects.filter(ssd__gte=temp_time1, ssd__lte=temp_time2).count()
        temp_count_gs = gs_queuehist.objects.filter(endtime__gte=temp_time1, endtime__lte=temp_time2).count()
        day_count_list_gs.append(temp_count_gs)
        day_count_list_ga.append(temp_count_ga)
        day_count_list_zx.append(temp_count_zx)
        day_count_list_rz.append(temp_count_rz)
        day_list.append(temp_time1.strftime('%Y-%m-%d'))
        all_count += temp_count_zx + temp_count_rz + temp_count_ga +temp_count_gs

    print(day_list)

    title = "东城街道行政办事" + start + "至" + end + "总受理情况"
    line = Line(title,subtitle='总受理量为'+ str(all_count),subtitle_color='#F00',subtitle_text_size=16, height=600, width=1920, title_pos="center",)
    line.add('工商分局',
             day_list,
             day_count_list_gs,
             is_stack=True,
             is_label_show=True,
             #xaxis_interval=0,
             is_datazoom_show=True,
             legend_orient="vertical",
             legend_pos="right",
             legend_top="%10",
             )
    line.add('综合服务中心',
             day_list,
             day_count_list_zx,
             is_stack=True,
             is_label_show=True,
             is_datazoom_show=True,
             legend_orient="vertical",
             legend_pos="right",
             legend_top="%10",
             )
    line.add('公安分局',
             day_list,
             day_count_list_ga,
             is_stack=True,
             is_label_show=True,
             is_datazoom_show=True,
             legend_orient="vertical",
             legend_pos="right",
             legend_top="%10",
             )
    line.add('人力资源',
             day_list,
             day_count_list_rz,
             is_stack=True,
             is_label_show=True,
             is_datazoom_show=True,
             legend_orient="vertical",
             legend_pos="right",
             legend_top="%10",
             )
    return line


def zx_service_bar(start = None, end = None):
    try:
        starttime = datetime.datetime.strptime(start, '%Y-%m-%d')
    except:
        starttime = time.strftime("%Y-%m-%d 00:00:00")
    try:
        endtime = datetime.datetime.strptime(end, '%Y-%m-%d')+ datetime.timedelta(days=1)
    except:
        endtime = time.strftime("%Y-%m-%d 23:59:59")
    zx_piaohao_list = zx_piaohaotongji.objects.filter(creationtime__gte=starttime, creationtime__lte=endtime)
    zx_service_list = zx_pdqk.objects.exclude(name__contains='all')
    zx_piaohao_yewu_list = dict(
        serivce_list=[],
        count_list=[]
    )
    for i in zx_service_list:
        zx_piaohao_yewu_list["serivce_list"].append(i.name)
    all_count = 0
    temp_list = zx_piaohao_list
    for i in zx_piaohao_yewu_list["serivce_list"]:
        count = zx_piaohao_list.filter(ywmc=i).count()
        temp_list = temp_list.exclude(ywmc=i)
        zx_piaohao_yewu_list["count_list"].append(count)
        all_count += count
    for temp in temp_list:
        print(temp.ywmc)
    print(temp_list.count())
    title = "东城综合服务中心" + start + "至" + end + "受理情况"
    bar = Bar(title, subtitle='总受理量为'+ str(all_count),subtitle_color='#F00',subtitle_text_size=16, height=600, width=1920, title_pos="center", )
    bar.add("业务量",
            zx_piaohao_yewu_list["serivce_list"],
            zx_piaohao_yewu_list["count_list"],
            is_label_show=True,
            is_datazoom_show=True,
            legend_pos="left",
            xaxis_margin = 4,
        datazoom_type="slider",
        # datazoom_range=[10, 55],
             # xaxis_margin=0,  # 标签与轴线之间的距离
            xaxis_interval=0,  # 设置为0，强制显示所有标签
            xaxis_rotate=10,  # 倾斜角度：90~-90
            xaxis_label_textsize = 10,
            # xaxis_label_textsize = 1, # X轴标签字体大小
            )
    return bar

def zx_day_line(start = None, end=None):
    try:
        starttime = datetime.datetime.strptime(start, '%Y-%m-%d')
    except:
        starttime = time.strftime("%Y-%m-%d 00:00:00")
        starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d 00:00:00')
    try:
        endtime = datetime.datetime.strptime(end, '%Y-%m-%d')+ datetime.timedelta(days=1)
    except:
        endtime = time.strftime("%Y-%m-%d 23:59:59")
        endtime = datetime.datetime.strptime(endtime, '%Y-%m-%d 23:59:59')

    day_count = (endtime-starttime).days

    # print(day_count)
    # delta = datetime.timedelta(days=1)
    day_list = []
    day_count_list = []
    all_count = 0
    for i in range(0,day_count):
        temp_time1 = starttime + datetime.timedelta(days=i)
        temp_time2 = starttime + datetime.timedelta(days=i + 1)
        temp_count = zx_piaohaotongji.objects.filter(creationtime__gte=temp_time1, creationtime__lte=temp_time2).count()
        day_list.append(temp_time1.strftime('%Y-%m-%d'))
        day_count_list.append(temp_count)
        all_count += temp_count

    # print(day_list)
    # print(day_count_list)
    title = "东城综合服务中心" + start + "至" + end + "总受理情况"
    line = Line(title,subtitle='总受理量为'+ str(all_count),subtitle_color='#F00',subtitle_text_size=16, height=600, width=1920, title_pos="center",)
    line.add('',
             day_list,
             day_count_list,
             is_stack=True,
             is_label_show=True,
             #xaxis_interval=0,
             is_datazoom_show=True)

    return line

def rz_serial_bar(start = None, end = None):
    try:
        starttime = datetime.datetime.strptime(start, '%Y-%m-%d')
    except:
        starttime = time.strftime("%Y-%m-%d 00:00:00")
    try:
        endtime = datetime.datetime.strptime(end, '%Y-%m-%d') + datetime.timedelta(days=1)
    except:
        endtime = time.strftime("%Y-%m-%d 23:59:59")


    rz_serial_list = rz_service.objects.all()
    rz_queue_list = rz_queuehist.objects.filter(hjtime__gte=starttime, hjtime__lte=endtime)
    rz_serial_count_list = []
    rz_serial_name_list = []
    all_count = 0
    for i in rz_serial_list:
        count = rz_queue_list.filter(serial=i.serial).count()
        rz_serial_count_list.append(count)
        rz_serial_name_list.append(i.typename)
        all_count += count

    print(rz_serial_count_list)
    print(rz_serial_name_list)
    title = "东城人力资源局" + start + "至" + end + "业务受理情况"
    bar = Bar(title, subtitle='总受理量为'+ str(all_count),subtitle_color='#F00',subtitle_text_size=16, height=600, width=1920, title_pos="center", )
    bar.add("业务量",
            rz_serial_name_list,
            rz_serial_count_list,
            is_label_show=True,
            legend_pos="left",
            xaxis_margin=10,  # 标签与轴线之间的距离
            xaxis_interval=0,  # 设置为0，强制显示所有标签
            xaxis_rotate=25,
            xaxis_name_gap = 50,
            )
    print(time.time())
    return bar

def rz_count_pie(start = None, end=None):
    try:
        starttime = datetime.datetime.strptime(start, '%Y-%m-%d')
    except:
        starttime = time.strftime("%Y-%m-%d 00:00:00")
    try:
        endtime = datetime.datetime.strptime(end, '%Y-%m-%d') + datetime.timedelta(days=1)
    except:
        endtime = time.strftime("%Y-%m-%d 23:59:59")
    rz_counter_list = rz_counter.objects.all()
    rz_queue_list = rz_queuehist.objects.filter(hjtime__gte=starttime, hjtime__lte=endtime)
    rz_counter_count_list = []
    rz_counter_name_list = []
    all_count = 0
    for i in rz_counter_list:
        count = rz_queue_list.filter(counter=i.counterno).count()
        rz_counter_count_list.append(count)
        rz_counter_name_list.append(i.counterno + '号窗口')
        all_count += count

    title = "东城人力资源局" + start + "至" + end + "窗口受理情况"
    pie = Pie(title,subtitle='总受理量为'+ str(all_count),subtitle_color='#F00',subtitle_text_size=16,title_pos='center',width=1920,height=600,)
    pie.add('',
            rz_counter_name_list,
            rz_counter_count_list,
            label_text_color=None,
            is_label_show=True,
            legend_orient="vertical",
            legend_pos="left",)
    return pie

def rz_day_line(start = None, end=None):
    try:
        starttime = datetime.datetime.strptime(start, '%Y-%m-%d')
    except:
        starttime = time.strftime("%Y-%m-%d 00:00:00")
        starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d 00:00:00')
    try:
        endtime = datetime.datetime.strptime(end, '%Y-%m-%d')+ datetime.timedelta(days=1)
    except:
        endtime = time.strftime("%Y-%m-%d 23:59:59")
        endtime = datetime.datetime.strptime(endtime, '%Y-%m-%d 23:59:59')

    day_count = (endtime-starttime).days

    print(day_count)
    # delta = datetime.timedelta(days=1)
    day_list = []
    day_count_list = []
    all_count = 0
    for i in range(0,day_count):
        temp_time1 = starttime + datetime.timedelta(days=i)
        temp_time2 = starttime + datetime.timedelta(days=i + 1)
        temp_count = rz_queuehist.objects.filter(hjtime__gte=temp_time1, hjtime__lte=temp_time2).count()
        day_list.append(temp_time1.strftime('%Y-%m-%d'))
        day_count_list.append(temp_count)
        all_count += temp_count

    print(day_list)
    print(day_count_list)
    title = "东城人力资源局" + start + "至" + end + "总受理情况"
    line = Line(title,subtitle='总受理量为'+ str(all_count),subtitle_color='#F00',subtitle_text_size=16, height=600, width=1920, title_pos="center",)
    line.add('',
             day_list,
             day_count_list,
             is_stack=True,
             is_label_show=True,
             legend_pos="left",
             #xaxis_interval=0,
             is_datazoom_show=True)

    return line

def ga_service_bar(start = None, end = None):
    print(time.time())
    try:
        starttime = datetime.datetime.strptime(start, '%Y-%m-%d')
    except:
        starttime = time.strftime("%Y-%m-%d 00:00:00")
    try:
        endtime = datetime.datetime.strptime(end, '%Y-%m-%d') + datetime.timedelta(days=1)
    except:
        endtime = time.strftime("%Y-%m-%d 23:59:59")


    ga_service_list = ga_service.objects.all()
    ga_queue_list = ga_queuehist.objects.filter(ssd__gte=starttime, ssd__lte=endtime)
    ga_service_count_list = []
    ga_service_name_list = []
    all_count = 0
    for i in ga_service_list:
        count = ga_queue_list.filter(service=i.id).count()
        ga_service_count_list.append(count)
        ga_service_name_list.append(i.name)
        all_count += count

    title = "东城公安分局" + start + "至" + end + "业务受理情况"
    bar = Bar(title,subtitle='总受理量为'+ str(all_count),subtitle_color='#F00',subtitle_text_size=16, height=600, width=1920, title_pos="center", )
    bar.add("业务量",
            ga_service_name_list,
            ga_service_count_list,
            legend_pos="left",
            is_label_show=True,
            xaxis_margin=10,  # 标签与轴线之间的距离
            xaxis_interval=0,  # 设置为0，强制显示所有标签
            xaxis_rotate=25,
            xaxis_name_gap = 50,
            )
    print(time.time())
    return bar

def ga_window_pie(start = None, end=None):
    try:
        starttime = datetime.datetime.strptime(start, '%Y-%m-%d')
    except:
        starttime = time.strftime("%Y-%m-%d 00:00:00")
    try:
        endtime = datetime.datetime.strptime(end, '%Y-%m-%d') + datetime.timedelta(days=1)
    except:
        endtime = time.strftime("%Y-%m-%d 23:59:59")
    ga_window_list = ga_window.objects.all()
    ga_queue_list = ga_queuehist.objects.filter(ssd__gte=starttime, ssd__lte=endtime)
    ga_window_count_list = []
    ga_window_name_list = []
    all_count = 0
    for i in ga_window_list:
        count = ga_queue_list.filter(window=i.id).count()
        ga_window_count_list.append(count)
        ga_window_name_list.append(i.name + '号窗口')
        all_count += count

    title = "东城公安分局" + start + "至" + end + "窗口受理情况"
    pie = Pie(title,subtitle='总受理量为'+ str(all_count),subtitle_color='#F00',subtitle_text_size=16,height=600, width=1920, title_pos="center",)
    pie.add('',
            ga_window_name_list,
            ga_window_count_list,
            label_text_color=None,
            is_label_show=True,
            legend_orient="vertical",
            legend_pos="left",)
    return pie

def ga_day_line(start = None, end=None):
    try:
        starttime = datetime.datetime.strptime(start, '%Y-%m-%d')
    except:
        starttime = time.strftime("%Y-%m-%d 00:00:00")
        starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d 00:00:00')
    try:
        endtime = datetime.datetime.strptime(end, '%Y-%m-%d')+ datetime.timedelta(days=1)
    except:
        endtime = time.strftime("%Y-%m-%d 23:59:59")
        endtime = datetime.datetime.strptime(endtime, '%Y-%m-%d 23:59:59')

    day_count = (endtime-starttime).days

    print(day_count)
    # delta = datetime.timedelta(days=1)
    day_list = []
    day_count_list = []
    all_count = 0
    for i in range(0,day_count):
        temp_time1 = starttime + datetime.timedelta(days=i)
        temp_time2 = starttime + datetime.timedelta(days=i + 1)
        temp_count = ga_queuehist.objects.filter(ssd__gte=temp_time1, ssd__lte=temp_time2).count()
        day_list.append(temp_time1.strftime('%Y-%m-%d'))
        day_count_list.append(temp_count)
        all_count += temp_count

    print(day_list)
    print(day_count_list)
    title = "东城公安分局" + start + "至" + end + "总受理情况"
    line = Line(title, subtitle='总受理量为'+ str(all_count),subtitle_color='#F00',subtitle_text_size=16,height=600, width=1920, title_pos="center",)
    line.add('',
             day_list,
             day_count_list,
             is_stack=True,
             is_label_show=True,
             #xaxis_interval=0,
             is_datazoom_show=True)
    return line


def gs_service_bar(start = None, end = None):
    print(time.time())
    try:
        starttime = datetime.datetime.strptime(start, '%Y-%m-%d')
    except:
        starttime = time.strftime("%Y-%m-%d 00:00:00")
    try:
        endtime = datetime.datetime.strptime(end, '%Y-%m-%d') + datetime.timedelta(days=1)
    except:
        endtime = time.strftime("%Y-%m-%d 23:59:59")

    gs_service_list = gs_servetype.objects.all()
    gs_queue_list = gs_queuehist.objects.filter(endtime__gte=starttime, endtime__lte=endtime)
    gs_service_count_list = []
    gs_service_name_list = []
    all_count = 0
    for i in gs_service_list:
        count = gs_queue_list.filter(serial=i.serial).count()
        gs_service_count_list.append(count)
        gs_service_name_list.append(i.serialchar + '号业务')
        all_count += count

    title = "东城工商分局" + start + "至" + end + "业务受理情况"
    bar = Bar(title,subtitle='总受理量为'+ str(all_count),subtitle_color='#F00',subtitle_text_size=16, height=600, width=1920, title_pos="center", )
    bar.add("业务量",
            gs_service_name_list,
            gs_service_count_list,
            is_label_show=True,
            legend_pos="left",
            xaxis_margin=10,  # 标签与轴线之间的距离
            xaxis_interval=0,  # 设置为0，强制显示所有标签
            xaxis_rotate=25,
            xaxis_name_gap = 50,
            )
    print(time.time())
    return bar

def gs_window_pie(start = None, end=None):
    try:
        starttime = datetime.datetime.strptime(start, '%Y-%m-%d')
    except:
        starttime = time.strftime("%Y-%m-%d 00:00:00")
    try:
        endtime = datetime.datetime.strptime(end, '%Y-%m-%d') + datetime.timedelta(days=1)
    except:
        endtime = time.strftime("%Y-%m-%d 23:59:59")
    gs_window_list = gs_servetype.objects.all()
    gs_queue_list = gs_queuehist.objects.filter(endtime__gte=starttime, endtime__lte=endtime)
    gs_window_count_list = []
    gs_window_name_list = []
    all_count = 0
    for i in gs_window_list:
        count = gs_queue_list.filter(serial=i.serial).count()
        gs_window_count_list.append(count)
        gs_window_name_list.append(i.typename)
        all_count += count

    title = "东城工商分局" + start + "至" + end + "窗口受理情况"
    pie = Pie(title,subtitle='总受理量为'+ str(all_count),subtitle_color='#F00',subtitle_text_size=16,height=600, width=1920, title_pos="center",)
    pie.add('',
            gs_window_name_list,
            gs_window_count_list,
            label_text_color=None,
            is_label_show=True,
            legend_orient="vertical",
            legend_pos="left",)
    return pie

# 如果出现这个业务量突然多了，是因为业务配置中有改动，包含一些旧的配置
def gs_day_line(start = None, end=None):
    try:
        starttime = datetime.datetime.strptime(start, '%Y-%m-%d')
    except:
        starttime = time.strftime("%Y-%m-%d 00:00:00")
        starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d 00:00:00')
    try:
        endtime = datetime.datetime.strptime(end, '%Y-%m-%d')+ datetime.timedelta(days=1)
    except:
        endtime = time.strftime("%Y-%m-%d 23:59:59")
        endtime = datetime.datetime.strptime(endtime, '%Y-%m-%d 23:59:59')

    day_count = (endtime-starttime).days

    print(day_count)
    # delta = datetime.timedelta(days=1)
    day_list = []
    day_count_list = []
    gs_queuehist_list = gs_queuehist.objects.filter(endtime__gte=starttime,endtime__lte=endtime)
    all_count = 0
    for i in range(0,day_count):
        temp_time1 = starttime + datetime.timedelta(days=i)
        temp_time2 = starttime + datetime.timedelta(days=i + 1)
        temp_count = gs_queuehist_list.filter(endtime__gte=temp_time1, endtime__lte=temp_time2).count()
        day_list.append(temp_time1.strftime('%Y-%m-%d'))
        day_count_list.append(temp_count)
        all_count += temp_count

    print(day_list)
    print(day_count_list)
    title = "东城工商分局" + start + "至" + end + "总受理情况"
    line = Line(title,subtitle='总受理量为'+ str(all_count),subtitle_color='#F00',subtitle_text_size=16, height=600, width=1920, title_pos="center",)
    line.add('',
             day_list,
             day_count_list,
             is_stack=True,
             is_label_show=True,
             #xaxis_interval=0,
             is_datazoom_show=True)

    return line













def line3d_demo():
    _data = []
    for t in range(0, 25000):
        _t = t / 1000
        x = (1 + 0.25 * math.cos(75 * _t)) * math.cos(_t)
        y = (1 + 0.25 * math.cos(75 * _t)) * math.sin(_t)
        z = _t + 2.0 * math.sin(75 * _t)
        _data.append([x, y, z])
    range_color = [
        '#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
        '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
    line3d = Line3D("3D line plot demo", width=1200, height=600)
    line3d.add("", _data, is_visualmap=True,
               visual_range_color=range_color, visual_range=[0, 30],
               is_grid3D_rotate=True, grid3D_rotate_speed=180)
    return line3d

def bar_demo():
    bar = Bar("柱状图demo", "这里是副标题")
    bar.add("服装",
            ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"],
            [5, 20, 36, 10, 75, 90],
            is_label_show=True,
            )
    return bar

def pie_demo():
    attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    v1 = [11, 12, 13, 10, 10, 10]
    pie = Pie("饼图demo")
    pie.add("", attr, v1, is_label_show=True)
    return pie

def k_demo():
    v1 = [[2320.26, 2320.26, 2287.3, 2362.94], [2300, 2291.3, 2288.26, 2308.38],
          [2295.35, 2346.5, 2295.35, 2345.92], [2347.22, 2358.98, 2337.35, 2363.8],
          [2360.75, 2382.48, 2347.89, 2383.76], [2383.43, 2385.42, 2371.23, 2391.82],
          [2377.41, 2419.02, 2369.57, 2421.15], [2425.92, 2428.15, 2417.58, 2440.38],
          [2411, 2433.13, 2403.3, 2437.42], [2432.68, 2334.48, 2427.7, 2441.73],
          [2430.69, 2418.53, 2394.22, 2433.89], [2416.62, 2432.4, 2414.4, 2443.03],
          [2441.91, 2421.56, 2418.43, 2444.8], [2420.26, 2382.91, 2373.53, 2427.07],
          [2383.49, 2397.18, 2370.61, 2397.94], [2378.82, 2325.95, 2309.17, 2378.82],
          [2322.94, 2314.16, 2308.76, 2330.88], [2320.62, 2325.82, 2315.01, 2338.78],
          [2313.74, 2293.34, 2289.89, 2340.71], [2297.77, 2313.22, 2292.03, 2324.63],
          [2322.32, 2365.59, 2308.92, 2366.16], [2364.54, 2359.51, 2330.86, 2369.65],
          [2332.08, 2273.4, 2259.25, 2333.54], [2274.81, 2326.31, 2270.1, 2328.14],
          [2333.61, 2347.18, 2321.6, 2351.44], [2340.44, 2324.29, 2304.27, 2352.02],
          [2326.42, 2318.61, 2314.59, 2333.67], [2314.68, 2310.59, 2296.58, 2320.96],
          [2309.16, 2286.6, 2264.83, 2333.29], [2282.17, 2263.97, 2253.25, 2286.33],
          [2255.77, 2270.28, 2253.31, 2276.22]]
    kline = Kline("K 线图示例")
    kline.add("日K",
              ["2017/7/{}".format(i + 1) for i in range(31)],
              v1,
              is_datazoom_show=True,)
    return kline

