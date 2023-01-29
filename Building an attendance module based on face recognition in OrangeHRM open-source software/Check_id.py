import pymysql
import datetime

def check_id(id_user):
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="htloc")
    cursor = connection.cursor()
    retrive = "Select * from ohrm_attendance_record WHERE employee_id = '" + str(id_user) + "' ;"
    cursor.execute(retrive)
    rows = cursor.fetchall()
    dt2 = datetime.datetime.now()
    if len(rows)==0:
        check_in(id_user)
        connection.commit()
        connection.close()
        return "Check in"
    max=rows[0][0]
    pos=0
    for i in range(0,len(rows)):
        if rows[i][0]>max:
            max=rows[i][0]
            pos=i
    if rows[pos][10]=="PUNCHED OUT" :
        if (dt2.timestamp()-rows[pos][9].timestamp())<300.0:
            connection.commit()
            connection.close()
            return "Check in lai sau 5 phut"
        check_in(id_user)
        connection.commit()
        connection.close()
        return "Check in"
    if rows[pos][10]=="PUNCHED IN" :
        if (dt2.timestamp() - rows[pos][5].timestamp()) < 300.0:
            connection.commit()
            connection.close()
            return "Check out lai sau 5 phut"
        check_out(max)
        connection.commit()
        connection.close()
        return "Check out"
    connection.commit()
    connection.close()
    return " "

def check_out(id_c):
    muigio = 7
    name_muigio = "Asia/Saigon"
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="htloc")
    cursor = connection.cursor()
    dt2 = datetime.datetime.now()
    dt1 = datetime.datetime.fromtimestamp(dt2.timestamp() - muigio * 60 * 60)
    updateSql = "UPDATE  ohrm_attendance_record SET punch_out_utc_time= '"+str(dt1)+"', " \
               "punch_out_time_offset= '"+str(muigio)+"' ," \
               "punch_out_user_time= '"+str(dt2)+"'," \
               "state= 'PUNCHED OUT'," \
               "punch_out_timezone_name= '"+name_muigio+"'  WHERE ID = '"+str(id_c)+"' ;"
    cursor.execute(updateSql)
    connection.commit()
    connection.close()

def check_in(id_user):
    muigio = 7
    name_muigio = "Asia/Saigon"
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="htloc")
    cursor = connection.cursor()
    dt2 = datetime.datetime.now()
    dt1 = datetime.datetime.fromtimestamp(dt2.timestamp() - muigio * 60 * 60)
    insert = "INSERT INTO ohrm_attendance_record(employee_id, punch_in_utc_time, punch_in_time_offset," \
             " punch_in_user_time, state, punch_in_timezone_name) " \
             "VALUES('"+str(id_user)+"', '"+str(dt1)+"','"+str(muigio)+"','"+str(dt2)+"','PUNCHED IN','"+name_muigio+"' );"
    cursor.execute(insert)
    connection.commit()
    connection.close()
