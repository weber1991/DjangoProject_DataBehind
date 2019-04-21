import pymssql
import pymysql
import time, datetime


USER = 'databehind'
PASSWORD = 'weber'
# PASSWORD = 'Dc2019!@#'


def get_gs_count(starttime=None, endtime=None):
    context = {'state': '0'}

    try:
        start = datetime.datetime.strptime(starttime, "%Y-%m-%d").strftime('%Y-%m-%d %H:00:00')
    except:
        start = datetime.datetime.today().strftime('%Y-%m-%d')
    finally:
        pass
    try:
        end = datetime.datetime.strptime(endtime, "%Y-%m-%d").strftime('%Y-%m-%d 23:59:59')
    except:
        end = datetime.datetime.today().strftime('%Y-%m-%d')
    finally:
        pass

    try:
        db = pymysql.connect(host='localhost', user=USER, password=PASSWORD, db='databehind', port=3306, charset='utf8')
        cur = db.cursor()
    except:
        return context
    try:
        sql = "select * from dongcheng_gs_queuehist WHERE endtime >=  '" + start + "' AND endtime <=  '"+ end +"'"

        cur.execute(sql)
        rs = cur.fetchall()
        context["state"] = '1'
        context["count"] = len(rs)

        return context

    except Exception as e:
        # 错误回滚
        print(e)
        db.rollback()
        return context
    finally:
        db.close()

def get_ga_count(starttime=None, endtime=None):
    context = {'state': '0'}

    try:
        start = datetime.datetime.strptime(starttime, "%Y-%m-%d").strftime('%Y-%m-%d %H:00:00')
    except:
        start = datetime.datetime.today().strftime('%Y-%m-%d')
    finally:
        pass
    try:
        end = datetime.datetime.strptime(endtime, "%Y-%m-%d").strftime('%Y-%m-%d 23:59:59')
    except:
        end = datetime.datetime.today().strftime('%Y-%m-%d')
    finally:
        pass

    try:
        db = pymysql.connect(host='localhost', user=USER, password=PASSWORD, db='databehind', port=3306, charset='utf8')
        cur = db.cursor()
    except:
        return context
    try:
        sql = "select * from dongcheng_ga_queuehist WHERE ssd >=  '" + start + "' AND ssd <=  '"+ end +"'"

        cur.execute(sql)
        rs = cur.fetchall()
        context["state"] = '1'
        context["count"] = len(rs)

        return context

    except Exception as e:
        # 错误回滚
        print(e)
        db.rollback()
        return context
    finally:
        db.close()

def get_zx_count(starttime=None, endtime=None):
    context = {'state': '0'}

    try:
        start = datetime.datetime.strptime(starttime, "%Y-%m-%d").strftime('%Y-%m-%d %H:00:00')
    except:
        start = datetime.datetime.today().strftime('%Y-%m-%d')
    finally:
        pass
    try:
        end = datetime.datetime.strptime(endtime, "%Y-%m-%d").strftime('%Y-%m-%d 23:59:59')
    except:
        end = datetime.datetime.today().strftime('%Y-%m-%d')
    finally:
        pass

    try:
        db = pymysql.connect(host='localhost', user=USER, password=PASSWORD, db='databehind', port=3306, charset='utf8')
        cur = db.cursor()
    except:
        return context
    try:
        sql = "select * from dongcheng_zx_piaohaotongji WHERE creationtime >=  '" + start + "' AND creationtime <=  '"+ end +"'"

        cur.execute(sql)
        rs = cur.fetchall()
        context["state"] = '1'
        context["count"] = len(rs)

        return context

    except Exception as e:
        # 错误回滚
        print(e)
        db.rollback()
        return context
    finally:
        db.close()

def get_rz_count(starttime=None, endtime=None):
    context = {'state': '0'}

    try:
        start = datetime.datetime.strptime(starttime, "%Y-%m-%d").strftime('%Y-%m-%d %H:00:00')
    except:
        start = datetime.datetime.today().strftime('%Y-%m-%d')
    finally:
        pass
    try:
        end = datetime.datetime.strptime(endtime, "%Y-%m-%d").strftime('%Y-%m-%d 23:59:59')
    except:
        end = datetime.datetime.today().strftime('%Y-%m-%d')
    finally:
        pass

    try:
        db = pymysql.connect(host='localhost', user=USER, password=PASSWORD, db='databehind', port=3306, charset='utf8')
        cur = db.cursor()
    except:
        return context
    try:
        sql = "select * from dongcheng_rz_queuehist WHERE endtime >=  '" + start + "' AND endtime <=  '"+ end +"'"

        cur.execute(sql)
        rs = cur.fetchall()
        context["state"] = '1'
        context["count"] = len(rs)

        return context

    except Exception as e:
        # 错误回滚
        print(e)
        db.rollback()
        return context
    finally:
        db.close()


def insert_base_data(what='', count=0, start='', end=''):
    now = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    try:
        db = pymysql.connect(host='localhost', user='root', password=PASSWORD, db='databehind', port=3306,
                             charset='utf8')
        cur = db.cursor()
    except:
        return 'error'
    try:
        sql = "INSERT INTO dongcheng_base_data(what,count,start,end,changtime) VALUES('%s',%d,'%s','%s','%s')" \
                         % (what, count, start,end, now)

        cur.execute(sql)
        db.commit()  # 提交
        print(sql)
        return 'success'
    except Exception as e:
        # 错误回滚
        print(e)
        db.rollback()
        return 'error'
    finally:
        db.close()

def clean_base_data():
    try:
        db = pymysql.connect(host='localhost', user='root', password=PASSWORD, db='databehind', port=3306,
                             charset='utf8')
        cur = db.cursor()
    except:
        return 'error'
    try:
        sql = "DELETE FROM dongcheng_base_data"
        cur.execute(sql)
        db.commit()  # 提交
        return 'success'
    except Exception as e:
        # 错误回滚
        print(e)
        db.rollback()
        return 'error'
    finally:
        db.close()


# insert_base_data('test', 10, '2018-1-1', '2018-1-2')
# clean_base_data()
while True:
    # 构造时间序列

    today = datetime.datetime.strptime(time.strftime("%Y-%m-%d"), '%Y-%m-%d')
    day_1 = today - datetime.timedelta(days = 1)
    day_7 = today - datetime.timedelta(days = 7)
    day_31 = today - datetime.timedelta(days = 31)
    day_365 = today - datetime.timedelta(days = 365)
    print(day_1.strftime('"%Y-%m-%d"'))

    gs_count_7 = get_gs_count(day_7.strftime("%Y-%m-%d"), day_1.strftime("%Y-%m-%d"))
    gs_count_31 = get_gs_count(day_31.strftime("%Y-%m-%d"), day_1.strftime("%Y-%m-%d"))
    gs_count_365 = get_gs_count(day_365.strftime("%Y-%m-%d"), day_1.strftime("%Y-%m-%d"))

    ga_count_7 = get_ga_count(day_7.strftime("%Y-%m-%d"), day_1.strftime("%Y-%m-%d"))
    ga_count_31 = get_ga_count(day_31.strftime("%Y-%m-%d"), day_1.strftime("%Y-%m-%d"))
    ga_count_365 = get_ga_count(day_365.strftime("%Y-%m-%d"), day_1.strftime("%Y-%m-%d"))

    zx_count_7 = get_zx_count(day_7.strftime("%Y-%m-%d"), day_1.strftime("%Y-%m-%d"))
    zx_count_31 = get_zx_count(day_31.strftime("%Y-%m-%d"), day_1.strftime("%Y-%m-%d"))
    zx_count_365 = get_zx_count(day_365.strftime("%Y-%m-%d"), day_1.strftime("%Y-%m-%d"))

    rz_count_7 = get_rz_count(day_7.strftime("%Y-%m-%d"), day_1.strftime("%Y-%m-%d"))
    rz_count_31 = get_rz_count(day_31.strftime("%Y-%m-%d"), day_1.strftime("%Y-%m-%d"))
    rz_count_365 = get_rz_count(day_365.strftime("%Y-%m-%d"), day_1.strftime("%Y-%m-%d"))

    if (gs_count_7["state"] == '1') and (gs_count_31["state"] == '1') and (gs_count_365["state"] == '1') and (ga_count_7["state"] == '1') and (ga_count_31["state"] == '1') and (ga_count_365["state"] == '1') and (rz_count_7["state"] == '1') and (rz_count_31["state"] == '1') and (rz_count_365["state"] == '1') and (zx_count_7["state"] == '1') and (zx_count_31["state"] == '1') and (zx_count_365["state"] == '1'):
        print("clean data")
        clean_base_data()

    insert_base_data('gs_count_7',gs_count_7["count"],day_7.strftime("%Y-%m-%d"), day_1.strftime("%Y-%m-%d"))
    insert_base_data('gs_count_31', gs_count_31["count"], day_31.strftime("%Y-%m-%d"), day_31.strftime("%Y-%m-%d"))
    insert_base_data('gs_count_365', gs_count_365["count"], day_365.strftime("%Y-%m-%d"), day_365.strftime("%Y-%m-%d"))

    insert_base_data('ga_count_7',ga_count_7["count"],day_7.strftime("%Y-%m-%d"), day_1.strftime("%Y-%m-%d"))
    insert_base_data('ga_count_31', ga_count_31["count"], day_31.strftime("%Y-%m-%d"), day_31.strftime("%Y-%m-%d"))
    insert_base_data('ga_count_365', ga_count_365["count"], day_365.strftime("%Y-%m-%d"), day_365.strftime("%Y-%m-%d"))

    insert_base_data('zx_count_7',zx_count_7["count"],day_7.strftime("%Y-%m-%d"), day_1.strftime("%Y-%m-%d"))
    insert_base_data('zx_count_31', zx_count_31["count"], day_31.strftime("%Y-%m-%d"), day_31.strftime("%Y-%m-%d"))
    insert_base_data('zx_count_365', zx_count_365["count"], day_365.strftime("%Y-%m-%d"), day_365.strftime("%Y-%m-%d"))

    insert_base_data('rz_count_7',rz_count_7["count"],day_7.strftime("%Y-%m-%d"), day_1.strftime("%Y-%m-%d"))
    insert_base_data('rz_count_31', rz_count_31["count"], day_31.strftime("%Y-%m-%d"), day_31.strftime("%Y-%m-%d"))
    insert_base_data('rz_count_365', rz_count_365["count"], day_365.strftime("%Y-%m-%d"), day_365.strftime("%Y-%m-%d"))



    time.sleep(60*60)

