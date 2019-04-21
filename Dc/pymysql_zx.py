import os
import time,datetime
import pymysql


HOST = '10.145.192.68:1521/DALANG2016W'
USER = 'databehind'
PASSWORD = 'weber'
# PASSWORD = 'Dc2019!@#'

def zx_qupiaotongji(date = None):
    '''
    获取中心的取票信息
    :return:
    '''
    import cx_Oracle
    import os,datetime,time
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
    try:
        day = datetime.datetime.strptime(date, "%Y-%m-%d %H:00:00").strftime('%Y-%m-%d %H:00:00')
    except:
        day = time.strftime('%Y-%m-%d')
    finally:
        pass
    context = {'state':'0'}
    try:
        conn = cx_Oracle.connect('dc2017', 'ucap22119520', HOST)
        curs = conn.cursor()
    except:
        return context

    try:
        sql = "SELECT * FROM EX_GDBS_QUPIAOTONGJI WHERE creationtime > '" + day + "'" # sql语句

        curs.execute(sql)
        row = curs.fetchall()

        temp_list = []
        for i in row:
            temp = {}
            temp["xph"] = i[0]
            temp["ywmc"] = i[1]
            temp["creationtime"] = i[2]
            temp["qupiaotongji_id"] = i[3]
            temp["status"] = i[4]
            temp['cardno'] = i[5]
            temp["peoplename"] = i[6]
            temp["dtbs"] = i[8]
            temp["ywbm"] = i[9]
            temp_list.append(temp)
        context["state"] = '1'
        context["qupiaotongji_list"] = temp_list
        return context
    except Exception as e:
        print(e)
        return context
    finally:
        curs.close()
        conn.close()

def insert_zx_qupiaotongji(date = None):
    import pymysql,datetime
    qupiao_list = zx_qupiaotongji(date)
    if qupiao_list['state'] == '0':
        return 'error'

    try:
        db = pymysql.connect(host='localhost', user=USER, password=PASSWORD, db='databehind', port=3306, charset='utf8')
        cur = db.cursor()
    # sql_update = "update u set username = '%s' where id = %d"
    except:
        return 'error'

    try:
        for i in qupiao_list["qupiaotongji_list"]:
            # print(i)
            sql_insert = "INSERT INTO dongcheng_zx_piaohaotongji(xph,ywmc,creationtime,qupiaotongji_id, status, cardno, peoplename, dtbs, ywbm) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                         % (i["xph"], i["ywmc"], i["creationtime"], i["qupiaotongji_id"],i["status"],i["cardno"],i["peoplename"],i["dtbs"],i["ywbm"])
            try:
                cur.execute(sql_insert)  # 像sql语句传递参数
                db.commit()  # 提交
            except Exception as e:
                #print(e)
                continue
        print(datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')+' success.(zx_quhaotongji)')
    except Exception as e:
        # 错误回滚
        print(e)
        db.rollback()
    finally:
        db.close()

def select_zx_qupiaotongji_time(starttime):
    import pymysql
    import datetime

    db = pymysql.connect(host='localhost', user=USER, password=PASSWORD, db='databehind', port=3306, charset='utf8')
    cur = db.cursor()
    # sql_update = "update u set username = '%s' where id = %d"
    try:
        day = datetime.datetime.strptime(starttime, "%Y-%m-%d").strftime('%Y-%m-%d')
    except:
        day = datetime.datetime.today().strftime('%Y-%m-%d')
    finally:
        pass
    try:
        sql_insert = "SELECT * FROM dongcheng_zx_piaohaotongji WHERE creationtime > '" + day +"'"
        print(sql_insert)
        cur.execute(sql_insert)  # 像sql语句传递参数
        db.commit()  # 提交
        qupiaotongji_list = cur.fetchall()
        return qupiaotongji_list
    except Exception as e:
        # 错误回滚
        print(e)
        db.rollback()
        return 'error'
    finally:
        db.close()

def zx_ck():
    '''
    获取中心的取票信息
    :return:
    '''
    import cx_Oracle
    import os,datetime,time
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
    context = {'state':'0'}
    try:
        conn = cx_Oracle.connect('dc2017', 'ucap22119520', HOST)
        curs = conn.cursor()
    except:
        return context

    try:
        sql = "SELECT * FROM CK_PDQK"  # sql语句

        curs.execute(sql)
        row = curs.fetchall()

        temp_list = []
        for i in row:
            temp = {}
            temp["no"] = i[0]
            temp["name"] = i[1]
            temp["last"] = i[2]
            temp["ddrs"] = i[3]
            temp["createtime"] = i[4]
            temp['remainder'] = i[5]
            temp["dtbs"] = i[6]
            temp_list.append(temp)
        context["state"] = '1'
        context["ck_list"] = temp_list
        return context
    except Exception as e:
        print(e)
        return context
    finally:
        curs.close()
        conn.close()

def insert_zx_ck():
    import pymysql,datetime
    ck_list = zx_ck()
    if ck_list['state'] == '0':
        return 'error'

    try:
        db = pymysql.connect(host='localhost', user=USER, password=PASSWORD, db='databehind', port=3306, charset='utf8')
        cur = db.cursor()
    except:
        return 'error'

    # sql_update = "update u set username = '%s' where id = %d"

    try:
        print(len(ck_list["ck_list"]))
        qq = 1
        for i in ck_list["ck_list"]:

            qq += 1
            sql_insert = "INSERT INTO dongcheng_zx_pdqk(no,name,last,ddrs, createtime, remainder, dtbs) VALUES('%s','%s','%s','%s','%s','%s','%s')" \
                         % (i["no"], i["name"], i["last"], i["ddrs"],i["createtime"],i["remainder"],i["dtbs"])
            try:
                cur.execute(sql_insert)  # 像sql语句传递参数
                db.commit()  # 提交
            except Exception as e:
                print(qq)
                #print(e)
                continue
        print(datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')+' success.(zx_pdqk)')
    except Exception as e:
        # 错误回滚
        print(e)
        db.rollback()
    finally:
        db.close()

def delete_zx_ck():
    try:
        db = pymysql.connect(host='localhost', user=USER, password=PASSWORD, db='databehind', port=3306,
                             charset='utf8')
        cur = db.cursor()
    except:
        return 'error'

    sql_insert = "DELETE FROM dongcheng_zx_pdqk"
    try:
        cur.execute(sql_insert)  # 像sql语句传递参数
        db.commit()  # 提交
        print(datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S') + ' success.(zx_pdqk)')
    except Exception as e:
        # 错误回滚
        print(e)
        db.rollback()
    finally:
        db.close()


while True:
    delete_zx_ck()
    insert_zx_ck()
    insert_zx_qupiaotongji(None)
    # print(zx_ck())
    time.sleep(100)