import mysql.connector
#Step1:call connect() method and create object of connect()
x=mysql.connector.connect(host='localhost',
                        username='root',
                        password='Sudeept@777',
                        database='qrcode_db')
if x:
    print("Connection established sucessfully")
else:
    print("Please try again")

#Step2: create cursor object
y=x.cursor()

#Step3: execute sql query for creating a table
def create_table():
    y.execute("create table if not exists qrinfo(Person_name text,mobile_number text,address text,course_name text,course_date Date)")
def add_record(a,b,c,d,e):
    y.execute("insert into qrinfo(Person_name,mobile_number,address,course_name,course_date) values(%s,%s,%s,%s,%s)",(a,b,c,d,e))
#Step4: Commit()
    x.commit()
def view_all_records():
    y.execute("select * from qrinfo")
    data=y.fetchall()
    return data
def view_update():
    y.execute("select distinct person_name from qrinfo")
    data=y.fetchall()
    return data
def get_person(x):
    y.execute('select * from qrinfo where person_name="{}"'.format(x))
    data=y.fetchall()
    return data
def update(a,b,z,n):
    y.execute('update qrinfo set mobile_number=%s,course_name=%s,course_date=%s where person_name=%s'
                ,(a,b,z,n))
    x.commit()
    data=y.fetchall()
    return data
def delete(person):
    y.execute('delete from qrinfo where person_name="{}"'.format(person))
    x.commit()


    

