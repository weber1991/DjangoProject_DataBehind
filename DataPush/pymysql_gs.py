import pymssql
import pymysql
import time, datetime

#PASSWORD = 'weber'
PASSWORD = 'dc2018'

def gs_queuehist(starttime = None, endtime = None):
    '''
    东城工商分局的票号历史表
     获取大于start时间，小于end日期的票号历史，日期格式“YYYY-MM-DD”
     :param datetime:
     :return:
     '''
    try:
        start = datetime.datetime.strptime(starttime, "%Y-%m-%d").strftime('%Y-%m-%d %H:00:00')
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
        conn = pymssql.connect(host='19.104.172.204', user='sa', password='', database="QUEUE")
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
            temp["H_Serial"] = i[0]  # 业务编号
            temp["H_number"] = i[1] # 票号
            temp["H_counter"] = i[2] # 窗口号
            temp["H_cometime"] = i[3] # 取号时间
            temp["H_servetime"] = i[4] # 叫号时间
            temp["H_serveno"] = i[5] # 服务人员编号
            temp["H_endtime"] = i[6] # 作废时间
            temp["H_isdo"] = i[7] # hj标志
            temp_list.append(temp)
        context['state'] = "1"
        context["queuehist_list"] = temp_list
        return context
    except:
        return context
    finally:
        cursor.close()
        conn.close()

def gs_servertype():
    '''
    东城工商分局的业务，窗口关系表
    :return:
    '''
    import pymssql
    import datetime
    context = {'state': '0'}
    try:
        conn = pymssql.connect(host='19.104.172.204', user='sa', password='', database="QUEUE")
        cursor = conn.cursor()
    except:
        return context

    try:
        sql = "select * from dbo.servetype"

        cursor.execute(sql)
        rs = cursor.fetchall()
        temp_list = []
        for i in rs:
            temp = {}
            temp["S_Serial"] = i[0]  # 业务编号
            temp["S_char"] = i[1] # 业务编码，就是票号开头文字
            temp["S_typeno"] = i[2] # 窗口编号
            temp["S_typename"] = i[3] # 窗口名称
            temp["S_apartment"] = i[4] # 部门编号
            temp["S_apartmentname"] = i[5] # 部门名称
            temp["S_nownumber"] = i[7] # 等候人数
            temp["S_starttime"] = i[8]  # 业务开始时间
            temp["S_endtime"] = i[9]  # 业务结束时间
            temp_list.append(temp)
        context['state'] = "1"
        context["servetype_list"] = temp_list
        return context
    except:
        return context
    finally:
        cursor.close()
        conn.close()

def insert_gs_queuehist(start = None):

    service = gs_queuehist(start,None)
    if service['state'] == '0':
        return 'error'

    try:
        db = pymysql.connect(host='172.16.41.165', user='root', password=PASSWORD, db='databehind', port=3306, charset='utf8')
        cur = db.cursor()
    except:
        return 'error'

    try:
        for i in service["queuehist_list"]:
            sql_insert = "INSERT INTO dongcheng_gs_queuehist(serial,number,counter,cometime,servetime,serveno,endtime,isdo) VALUES('%s','%s','%s','%s','%s','%s','%s','%s')" \
                         % (i["H_Serial"], i["H_number"], i["H_counter"],i["H_cometime"],i["H_servetime"],i["H_serveno"],i["H_endtime"],i["H_isdo"])
            try:
                cur.execute(sql_insert)  # 像sql语句传递参数
                db.commit()  # 提交
            except:
                continue
        print("insert gs queuehist success!!")
    except Exception as e:
        # 错误回滚
        print(e)
        db.rollback()
    finally:
        db.close()

def insert_gs_servertype():
    service = gs_servertype()
    if service['state'] == '0':
        return 'error'

    try:
        db = pymysql.connect(host='172.16.41.165', user='root', password=PASSWORD, db='databehind', port=3306, charset='utf8')
        cur = db.cursor()
    except:
        return 'error'

    try:
        for i in service["servetype_list"]:
            sql_insert = "INSERT INTO dongcheng_gs_servetype(serial,serialchar,typeno,typename,apartment,apartmentname,nownumber,starttime,endtime) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                         % (i["S_Serial"], i["S_char"], i["S_typeno"],i["S_typename"],i["S_apartment"],i["S_apartmentname"],i["S_nownumber"],i["S_starttime"],i["S_endtime"])
            try:
                cur.execute(sql_insert)  # 像sql语句传递参数
                db.commit()  # 提交
            except:
                continue
        print("insert gs servertype success!!")
    except Exception as e:
        # 错误回滚
        print(e)
        db.rollback()
    finally:
        db.close()

def delete_gs_servertype():
    try:
        db = pymysql.connect(host='172.16.41.165', user='root', password=PASSWORD, db='databehind', port=3306, charset='utf8')
        cur = db.cursor()
    except:
        return 'error'

    try:
        sql_insert = "DELETE FROM dongcheng_gs_servetype"
        cur.execute(sql_insert)  # 像sql语句传递参数
        db.commit()  # 提交
        print('delete gs_servetype success!')
    except Exception as e:
        # 错误回滚
        print(e)
        db.rollback()
    finally:
        db.close()


def get_gs_count(starttime=None, endtime=None):
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
        db = pymysql.connect(host='172.16.41.165', user='root', password=PASSWORD, db='databehind', port=3306, charset='utf8')
        cur = db.cursor()
    except:
        return 'error'
    try:
        sql = "select * from dongcheng_gs_queuehist WHERE endtime >=  '" + start + "' AND endtime <=  '"+ end +"'"

        cur.execute(sql)
        rs = cur.fetchall()
        print(len(rs))

    except Exception as e:
        # 错误回滚
        print(e)
        db.rollback()
    finally:
        db.close()


while True:
    if gs_servertype()["state"] == '1':
        delete_gs_servertype()
        insert_gs_servertype()
    insert_gs_queuehist(None)

    # 服务器使用延迟
    time.sleep(5*60)

    # 个人单机使用延迟
    #time.sleep(100)