'''
此部分脚本需要删除数据从新加载
'''
import pymssql
import pymysql
import time, datetime
import os


USER = 'databehind'
PASSWORD = 'weber'
# PASSWORD = 'Dc2019!@#'

def rz_service():
    '''
    获取人资的业务类型，
    :return:
    成功:{state:'1', service_list:[{'s_serial': 1, 's_char': 'A', 's_typename': '就业失业登记 \r\n企业信息修改', 's_nownumber': 51}.....]}
    失败:{state:'0'}
    '''
    import pymssql
    context = {'state':'0'}
    try:
        conn = pymssql.connect(host='19.108.53.63', user='sa', password='sa', database="HRDQUEUE")
        cursor = conn.cursor()
    except:
        return context

    try:
        sql = "select * from dbo.serialset"
        cursor.execute(sql)
        rs = cursor.fetchall()
        service_list = []
        for i in rs:
            service = {}
            service["s_serial"] = i[0]
            service["s_char"] = i[1]
            service["s_typename"] = i[3]
            service["s_nownumber"] = i[7]   # 当前等候人数，这个需要更新
            service_list.append(service)
        context['state'] = "1"
        context["service_list"] = service_list
        return context
    except:
        return context
    finally:
        cursor.close()
        conn.close()

def rz_counter():
    '''
    获取人资的窗口类型，
    :return:
    成功:{state:'1', counter_list:[{'T_counterno': 1, 'T_serial': '关联行，和业务', 'T_number': '当前办理号', 'T_status': 51,'T_serverno',''}.....]}
    失败:{state:'0'}
    '''
    import pymssql
    context = {'state':'0'}
    try:
        conn = pymssql.connect(host='19.108.53.63', user='sa', password='sa', database="HRDQUEUE")
        cursor = conn.cursor()
    except:
        return context

    try:
        sql = "select * from dbo.counterset"
        cursor.execute(sql)
        rs = cursor.fetchall()
        temp_list = []
        for i in rs:
            temp = {}
            temp["T_counterno"] = i[0]
            temp["T_serial"] = i[3]
            temp["T_number"] = i[5] # 当前办理号，可以通过刷新来获取
            temp["T_statue"] = i[6]   # 窗口状态，猜测：W代表正在办理，E代表
            temp["T_serverno"] = i[8] # 窗口业务人员编号
            temp_list.append(temp)
        context['state'] = "1"
        context["counter_list"] = temp_list
        return context
    except:
        return context
    finally:
        cursor.close()
        conn.close()

def rz_queuehist(starttime = None, endtime = None):
    '''
     获取大于start时间，小于end日期的票号历史，日期格式“YYYY-MM-DD”
     :param datetime:
     :return:
     '''
    import pymssql
    import datetime
    try:
        start = datetime.datetime.strptime(starttime, "%Y-%m-%d").strftime('%Y-%m-%d 00:00:00')
    except:
        start = datetime.datetime.today().strftime('%Y-%m-%d 00:00:00')
    finally:
        pass
    try:
        end = datetime.datetime.strptime(endtime, "%Y-%m-%d").strftime('%Y-%m-%d 23:59:59')
    except:
        end = datetime.datetime.today().strftime('%Y-%m-%d 23:59:59')
    finally:
        pass
    context = {'state': '0'}
    try:
        conn = pymssql.connect(host='19.108.53.63', user='sa', password='sa', database="HRDQUEUE")
        cursor = conn.cursor()
    except:
        return context

    try:
        sql = "select * from dbo.QueueHist WHERE H_endtime >=  '" + start + "' AND H_endtime <=  '"+ end +"'"
        cursor.execute(sql)
        rs = cursor.fetchall()
        temp_list = []
        for i in rs:
            temp = {}
            temp["H_id"] = i[0]
            temp["H_Serial"] = i[1]  # 业务编号
            temp["H_number"] = i[2] # 票号
            temp["H_counter"] = i[3] # 窗口号
            temp["H_cometime"] = i[4] # 取号时间
            temp["H_servetime"] = i[5] # 叫号时间
            temp["H_serveno"] = i[6] # 服务人员编号
            temp["H_endtime"] = i[7] # 作废时间
            temp["H_isHJ"] = i[13] # hj标志
            if i[14] is None:
                temp["H_hjtime"] = ''  # hj时间
            else:
                temp["H_hjtime"] = i[14]
            temp["H_finished"] = i[15]  # 完成标志
            temp_list.append(temp)
        context['state'] = "1"
        context["queuehist_list"] = temp_list
        return context
    except:
        return context
    finally:
        cursor.close()
        conn.close()

def insert_rz_service():
    import pymysql

    service = rz_service()
    if service['state'] == '0':
        return 'error'

    try:
        db = pymysql.connect(host='localhost', user=USER, password=PASSWORD, db='databehind', port=3306, charset='utf8')
        cur = db.cursor()
   # sql_update = "update u set username = '%s' where id = %d"
    except:
        return 'error'

    try:
        for i in service["service_list"]:
            sql_insert = "INSERT INTO dongcheng_rz_service(serial,serialchar,typename,nownumber) VALUES(%d,'%s','%s',%d)" \
                         % (i["s_serial"], i["s_char"], i["s_typename"],i["s_nownumber"])
            cur.execute(sql_insert)  # 像sql语句传递参数
            db.commit()  # 提交
    except Exception as e:
        # 错误回滚
        print(e)
        db.rollback()
    finally:
        db.close()

def insert_rz_counter():
    import pymysql

    temp = rz_counter()
    if temp['state'] == '0':
        return 'error'
    try:
        db = pymysql.connect(host='localhost', user=USER, password=PASSWORD, db='databehind', port=3306, charset='utf8')
        cur = db.cursor()
    except:
        return 'error'
    try:
        for i in temp["counter_list"]:
            sql_insert = "INSERT INTO dongcheng_rz_counter(counterno,serial,number,state,serveno) VALUES('%s','%s','%s','%s','%s')" \
                         % (i["T_counterno"], i["T_serial"], i["T_number"],i["T_statue"],i["T_serverno"])
            try:
                cur.execute(sql_insert)  # 像sql语句传递参数
                db.commit()  # 提交
            except Exception as e:
                print(e)
                continue
    except Exception as e:
        # 错误回滚
        print(e)
        db.rollback()
    finally:
        db.close()

def insert_rz_queuehist(start = None, end = None):
    import pymysql
    service = rz_queuehist(start, None)
    if service['state'] == '0':
        return 'error'

    try:
        db = pymysql.connect(host='localhost', user=USER, password=PASSWORD, db='databehind', port=3306, charset='utf8')
        cur = db.cursor()
    # sql_update = "update u set username = '%s' where id = %d"
    except:
        return 'error'

    try:
        for i in service["queuehist_list"]:
            sql_insert = "INSERT INTO dongcheng_rz_queuehist(id,serial,number,counter,cometime,servetime,serveno,endtime,isHJ,hjtime,finished) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                         % (i["H_id"], i["H_Serial"], i["H_number"], i["H_counter"],i["H_cometime"],i["H_servetime"],i["H_serveno"],i["H_endtime"],i["H_isHJ"],i["H_hjtime"],i["H_finished"])
            try:
                cur.execute(sql_insert)  # 像sql语句传递参数
                db.commit()  # 提交
            except:
                continue
        print(datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S') + ' success!(rz_queuehist。)')
    except Exception as e:
        # 错误回滚
        print(e)
        db.rollback()
    finally:
        db.close()

def delete_rz_service():
    try:
        db = pymysql.connect(host='localhost', user=USER, password=PASSWORD, db='databehind', port=3306,
                             charset='utf8')
        cur = db.cursor()
    except:
        return 'error'

    try:
        sql_insert = "DELETE FROM dongcheng_rz_service"
        cur.execute(sql_insert)  # 像sql语句传递参数
        db.commit()  # 提交
    except Exception as e:
        # 错误回滚
        print(e)
        db.rollback()
    finally:
        db.close()

def delete_rz_counter():
    try:
        db = pymysql.connect(host='localhost', user=USER, password=PASSWORD, db='databehind', port=3306, charset='utf8')
        cur = db.cursor()
    except:
        return 'error'

    try:
        sql_insert = "DELETE FROM dongcheng_rz_counter"
        cur.execute(sql_insert)  # 像sql语句传递参数
        db.commit()  # 提交
    except Exception as e:
        # 错误回滚
        print(e)
        db.rollback()
    finally:
        db.close()

while True:
    if rz_service()["state"] == '1':
        delete_rz_service()
        insert_rz_service()
    else:
        print("rz更新业务信息失败。")
    if rz_counter()["state"] == '1':
        delete_rz_counter()
        insert_rz_counter()
    else:
        print("rz更新窗口信息失败。")
    insert_rz_queuehist(None,None)
    time.sleep(100)