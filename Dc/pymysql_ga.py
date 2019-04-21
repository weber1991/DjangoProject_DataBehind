import pymysql
import datetime,time


USER = 'databehind'
PASSWORD = 'weber'
# PASSWORD = 'Dc2019!@#'

def ga_service():
    '''
     获取公安业务数据，
     :return:
     '''
    context = {'state': '0'}
    try:
        conn = pymysql.connect(host='120.76.201.146', user='dev', password='dev1231234', db="padc", port=3306, charset='utf8')
        cursor = conn.cursor()
    except:
        return context

    try:
        sql = "select * from service"
        cursor.execute(sql)
        rs = cursor.fetchall()
        temp_list = []
        for i in rs:
            temp = {}
            temp["id"] = i[0]   # id
            temp["code"] = i[2] # 票号开头编码
            temp["parent"] = i[3]  # 业务名称1
            temp["name"] = i[4]  # 业务名称2
            temp_list.append(temp)
        context['state'] = "1"
        context["service_list"] = temp_list
        return context
    except Exception as e:
        print(e)
        return context
    finally:
        cursor.close()
        conn.close()

def ga_window():
    '''
     获取公安窗口数据，
     :return:
     '''
    context = {'state': '0'}
    try:
        conn = pymysql.connect(host='120.76.201.146', user='dev', password='dev1231234', db="padc", port=3306, charset='utf8')
        cursor = conn.cursor()
    except:
        return context

    try:
        sql = "select * from window"
        cursor.execute(sql)
        rs = cursor.fetchall()
        temp_list = []
        for i in rs:
            temp = {}
            temp["id"] = i[0]   # id
            temp["code"] = i[2] # 窗口编码
            temp["name"] = i[3]  # 窗口名称
            temp["status"] = i[4]  # 状态
            temp["sort_category"] = i[5]    # 待参考
            temp_list.append(temp)
        context['state'] = "1"
        context["window_list"] = temp_list
        return context
    except Exception as e:
        print(e)
        return context
    finally:
        cursor.close()
        conn.close()

def ga_queuehist(start):
    '''
      获取公安业务数据，
      :return:
      '''
    import datetime
    try:
        starttime = datetime.datetime.strptime(start, "%Y-%m-%d").strftime('%Y-%m-%d 00:00:00')
    except:
        starttime = datetime.datetime.today().strftime('%Y-%m-%d 00:00:00')
    finally:
        pass
    context = {'state': '0'}
    try:
        conn = pymysql.connect(host='120.76.201.146', user='dev', password='dev1231234', db="padc", port=3306,
                               charset='utf8')
        cursor = conn.cursor()
    except:
        return context

    try:
        sql = "select * from queue_history where ssd > '" + starttime +"'"
        cursor.execute(sql)
        rs = cursor.fetchall()
        temp_list = []
        for i in rs:
            temp = {}
            temp["id"] = i[0]  # 唯一id
            temp["code"] = i[1]  # 票号
            temp["service"] = i[2]  # 业务号
            temp["window"] = i[6]  # 窗口号
            temp["name"] = i[10]  # 预约人姓名
            temp["id_card"] = i[11]  # 身份证
            temp["phone"] = i[12]  # 预约联系电话
            temp["appointment"] = i[19]  # 预约
            if i[20] is None:
                temp["acd"] = '1984-12-25 23:59:59'
            else:
                temp["acd"] = i[20]  # 预约时间
            temp["fcd"] = i[21]     # 取号时间
            temp["ssd"] = i[23]     # 结束时间
            temp["lcd"] = i[24]     # 结束时间
            temp_list.append(temp)
        context['state'] = "1"
        context["queuehist_list"] = temp_list
        return context
    except Exception as e:
        print(e)
        return context
    finally:
        cursor.close()
        conn.close()

def insert_ga_service():
    temp = ga_service()
    if temp['state'] == '0':
        return 'error'

    try:
        db = pymysql.connect(host='localhost', user=USER, password=PASSWORD, db='databehind', port=3306, charset='utf8')
        cur = db.cursor()
    # sql_update = "update u set username = '%s' where id = %d"
    except:
        return 'error'

    try:
        for i in temp["service_list"]:
            sql_insert = "INSERT INTO dongcheng_ga_service(id, code, parent, name ) VALUES('%s','%s','%s','%s')" \
                         % (i["id"], i["code"], i["parent"], i["name"])
            print(sql_insert)
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

def insert_ga_window():
    temp = ga_window()
    if temp['state'] == '0':
        return 'error'

    try:
        db = pymysql.connect(host='localhost', user=USER, password=PASSWORD, db='databehind', port=3306,
                             charset='utf8')
        cur = db.cursor()
    except:
        return 'error'

    try:
        for i in temp["window_list"]:
            sql_insert = "INSERT INTO dongcheng_ga_window(id, code, name, status, sort_category ) VALUES('%s','%s','%s','%s','%s')" \
                         % (i["id"], i["code"], i["name"], i["status"], i["sort_category"])
            try:
                cur.execute(sql_insert)  # 像sql语句传递参数
                db.commit()  # 提交
            except Exception as e:
                # print(e)
                continue
        print(datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S') + ' success!(insert_ga_window。)')
    except Exception as e:
        # 错误回滚
        print(e)
        db.rollback()
    finally:
        db.close()

def insert_ga_queuehist(start = None):
    temp = ga_queuehist(start)
    if temp['state'] == '0':
        return 'error'
    try:
        db = pymysql.connect(host='localhost', user=USER, password=PASSWORD, db='databehind', port=3306,
                             charset='utf8')
        cur = db.cursor()
    except:
        return 'error'

    try:
        for i in temp["queuehist_list"]:
            sql_insert = "INSERT INTO dongcheng_ga_queuehist(id, code, service, window, name, id_card, phone, appointment, acd, fcd, ssd, lcd ) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                         % (i["id"], i["code"], i["service"], i["window"], i["name"], i["id_card"], i["phone"], i["appointment"], i["acd"], i["fcd"], i["ssd"],i["lcd"])
            try:
                cur.execute(sql_insert)  # 像sql语句传递参数
                db.commit()  # 提交
            except Exception as e:
                print(e)
                continue
        print(datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S') + ' success!(insert_ga_queuehist。)')
    except Exception as e:
        # 错误回滚
        print(e)
        db.rollback()
    finally:
        db.close()

def del_ga_window():
    try:
        db = pymysql.connect(host='localhost', user=USER, password=PASSWORD, db='databehind', port=3306,
                             charset='utf8')
        cur = db.cursor()
    except:
        return 'error'

    sql_insert = "DELETE FROM dongcheng_ga_window"
    try:
        cur.execute(sql_insert)  # 像sql语句传递参数
        db.commit()  # 提交
        print(datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S') + ' success!(delete_ga_window。)')
    except Exception as e:
        # 错误回滚
        print(e)
        db.rollback()
    finally:
        db.close()

def del_ga_service():
    try:
        db = pymysql.connect(host='localhost', user=USER, password=PASSWORD, db='databehind', port=3306,
                             charset='utf8')
        cur = db.cursor()
    except:
        return 'error'
    sql_insert = "DELETE FROM dongcheng_ga_service"
    try:
        cur.execute(sql_insert)  # 像sql语句传递参数
        db.commit()  # 提交
        print(datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S') + ' success!(delete_ga_service。)')
    except Exception as e:
        # 错误回滚
        print(e)
        db.rollback()
    finally:
        db.close()


while True:
    if ga_service()["state"] == "1":
        del_ga_window()
        insert_ga_window()
    else:
        print("更新公安业务失败")

    if ga_window()["state"] == "1":
        del_ga_service()
        insert_ga_service()
    else:
        print("更新公安窗口失败")
    insert_ga_queuehist(None)
    time.sleep(100)
