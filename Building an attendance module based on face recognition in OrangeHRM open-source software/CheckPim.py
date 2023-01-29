import pymysql
import pickle
import shutil
import os
import cv2

def write_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)

def _load_pickle(file_path):
  with open(file_path, 'rb') as f:
    obj = pickle.load(f)
  return obj

def _save_pickle(obj, file_path):
  with open(file_path, 'wb') as f:
    pickle.dump(obj, f)
def sosanh(a,b):
    if (len(a)>len(b)):
        tb=0
        while tb<len(b):
            ta=0
            while ta<len(a):
                if b[tb]==a[ta]:
                    b.pop(tb)
                    a.pop(ta)
                    ta=len(a)
                    tb=tb-1
                ta=ta+1
            tb=tb+1
        return a
    if (len(a)<len(b)):
        ta=0
        while ta<len(a):
            tb=0
            while tb<len(b):
                if b[tb]==a[ta]:
                    b.pop(tb)
                    a.pop(ta)
                    tb=len(b)
                    ta=ta-1
                tb=tb+1
            ta=ta+1
        return b
    return []


def kt():
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="htloc")
    cursor = connection.cursor()
    retrive = "Select * from hs_hr_emp_attachment;"
    cursor.execute(retrive)
    rows = cursor.fetchall()
    a=[]
    t=0
    for row in rows:
      a.append(row[0])
    y=_load_pickle("Data/ds.pkl")

    # print(y,a)
    if (len(a)!=len(y)) :
        t=1
        import main
        a1 = []
        y1 = []
        for t1 in a:
            a1.append(t1)
        for t1 in y:
            y1.append(t1)
        cds=sosanh(a1,y1)
        for cd in cds:
            # print(cd)
            retrive = "Select * from hs_hr_emp_attachment WHERE emp_number = '" + str(cd) + "' ;"
            cursor.execute(retrive)
            row2 = cursor.fetchall()
            main.remove_u(str(cd))
            path="Dataset/"+str(cd)
            try:
                shutil.rmtree(path)
            except:
                osss = 0
            if len(row2)>0:
                os.mkdir(path)
                q=0
                for t1 in row2:
                    image = t1[5]
                    q=q+1
                    write_file(image,path+"/"+"image"+str(q)+".jpg")
                    main.add_u(str(cd), cv2.imread(path+"/"+"image"+str(q)+".jpg"))


        retrive = "Select * from hs_hr_employee;"
        cursor.execute(retrive)
        row2 = cursor.fetchall()
        b = []
        for t1 in row2:
            b.append([t1[0], t1[2] + " " + t1[4] + " " + t1[3]])
        _save_pickle(b, "Data/name_id.pkl")
        _save_pickle(a,"Data/ds.pkl")
    # print(y,a)
    connection.commit()
    connection.close()
    return t