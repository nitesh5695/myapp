import mysql.connector
mydb=mysql.connector.connect(host="sql9.freemysqlhosting.net",user="sql9366080",password="q1fjEE9FfW",database="sql9366080")
mycursor=mydb.cursor()
query_marks = """select * from 18mca02_abcd123456 where exam_name="final exam end" """
mycursor.execute(query_marks)
result = mycursor.fetchall()
Ename = result
print(Ename)