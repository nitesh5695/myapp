from flask import Flask ,render_template,request,session
import mysql.connector
import random
import smtplib
global otp
otp=str(1234)
def send_otp(email):
    global otp
    obj=smtplib.SMTP('smtp.gmail.com',587)
    otp=str(random.randint(4567,6785))
    obj.ehlo()
    obj.starttls()
    obj.login("tanya.assistant1916@gmail.com","TANYA 1916")
    obj.sendmail('tanya.assistant1916@gmail.com',email,otp)
    print("send successfully")
    obj.close()



mydb=mysql.connector.connect(host="sql9.freemysqlhosting.net",user="sql9366080",password="q1fjEE9FfW",database="sql9366080")
mycursor=mydb.cursor()
app=Flask(__name__)
app.secret_key="nit1234"
@app.route('/')
def detals():
    return render_template('start_page.html')
@app.route('/create_class')
def create_class():
    return render_template('create_class.html')
@app.route('/join_class')
def join_class():
    return render_template("join_class.html")
@app.route('/login')
def login():
    return render_template("login.html")
@app.route('/form', methods=['GET','POST'])
def form():
    global name
    global email
    global mobile
    global password
    global school



    if(request.method=='POST'):
        name=request.form.get('name')
        email=request.form.get('email')
        mobile=request.form.get('mobile_no')
        password=request.form.get('password')
        school=request.form.get('school')
        rep_password=request.form.get('confirm_password')


        q=(email,mobile)
        query_alreadyExist="select * from teachers_list where email= %s and mobile_no=%s"
        print(query_alreadyExist)
        mycursor.execute(query_alreadyExist,q)
        emails=mycursor.fetchall()

        if(len(emails)>0):
            return render_template('create_class.html',error="email already exist")

        elif(password==rep_password):
            print(email)
            #send_otp(email)
            print("otp send")

            return render_template("otp_page.html")
        else:
            return render_template('create_class.html',error="password is not match")
@app.route('/otp_page')
def otp_page():
    return render_template("otp_page.html")
@app.route('/otp_message',methods=['GET','POST'])
def otp_message():
    print('in otp message')
    if(request.method=='POST'):
        otp_value=request.form.get('otp')
        global otp
        otp=str(1234)
        print(otp,otp_value)
        if(otp==otp_value):
            print('enters in if')
            global code
            code = 'abcd12345'
            p=(name,email,password,mobile,school,code)
            query="insert into teachers_list values(%s,%s,%s,%s,%s,%s)"

            mycursor.execute(query,p)
            query_create="create table {}(name char(50),email varchar(60),password varchar(50),mobile_no char(11),roll_no varchar(10),class_code varchar(10))".format(code)
            mycursor.execute(query_create)
            create_student_attendance_table="create table student_attendance_{}(date date,roll_no varchar(20),name char(30),status varchar(10))".format(code)
            mycursor.execute(create_student_attendance_table)
            create_notifi_table = 'create table notification_{}(date date,notification_data varchar(255))'.format(code)
            mycursor.execute(create_notifi_table)
            create_assignment_table="create table assignment_{}(assign_date date,subject varchar(60),assignment varchar(255),date date)".format(code)
            mycursor.execute(create_assignment_table)
            create_fee_table="create table fees_{}(roll_no varchar(10),date date,month char(10),rupees varchar(6))".format(code)
            mycursor.execute(create_fee_table)
            mydb.commit()
            print('executed')


            return render_template("otp_page.html", message="successfully class created")
        else:
            return render_template('otp_page.html',message="incorrect otp try again")
@app.route('/join_class_form',methods=['POST'])
def join_class_form():
    global Sname,Semail,Smobile,Spassword,Sschool,roll_no,Srep_password,class_code

    if request.method=='POST':
        Sname = request.form.get('name')
        Semail = request.form.get('email')
        Smobile = request.form.get('mobile_no')
        Spassword = request.form.get('password')
        Sschool = request.form.get('school')
        Srep_password = request.form.get('confirm_password')
        roll_no=request.form.get('roll_no')
        class_code=request.form.get('class_code')
        print(class_code)
        q = (Semail, Smobile)
        query_alreadyExist = "select * from {} where email= %s and mobile_no=%s".format(class_code)
        print(query_alreadyExist,q)
        mycursor.execute(query_alreadyExist, q)
        emails = mycursor.fetchall()

        if (len(emails) > 0):
            return render_template('join_class.html', error="email already exist")

        elif (Spassword == Srep_password):

            # send_otp(email)
            print("otp send")

            return render_template("student_otp_page.html")
        else:
            return render_template('join_class.html', error="password is not match")

@app.route('/student_otp_formdata',methods=['POST'])
def student_otp_formdata():
    if (request.method == 'POST'):
        otp_value = request.form.get('otp')
        otp = str(1234)
        print(otp, otp_value)

        if (otp == otp_value):

            p = (Sname, Semail, Spassword, Smobile, roll_no,class_code)
            query = "insert into {} values(%s,%s,%s,%s,%s,%s)".format(class_code)
            mycursor.execute(query, p)
            mydb.commit()
            create_marks_table="create table {}_{}(exam_name varchar(140),max_mark int(4),subject varchar(90),mark int(4))".format(roll_no,class_code)
            mycursor.execute(create_marks_table)


            return render_template("student_otp_page.html", message="successfully class joined")
        else:
            return render_template('student_otp_page.html', message="incorrect otp try again")


@app.route('/login_formdata', methods=['GET','POST'])
def login_message():
    global login_email,login_password,S_class_code
    if(request.method=='POST'):
        login_type=request.form.get('login_type')
        login_email=request.form.get('email')
        login_password=request.form.get('password')
        S_class_code=request.form.get('class_code')
        session['lemail']=login_email
        session['class_code']=S_class_code
        session['pass']=login_password
        d=(session['lemail'],session['pass'])
        if 'lemail' in session:
            if(login_type=='teacher'):
                loginquery="select * from teachers_list where email=%s and password=%s"
                fetch_name="select name from teachers_list where email=%s and password=%s"
    
                mycursor.execute(loginquery,d)
                user=mycursor.fetchall()
    
    
                print(len(user))
                if len(user)>0:
                  mycursor.execute(fetch_name, d)
                  Tname = [row[0] for row in mycursor.fetchone()]
    
                  return render_template('teacher_main.html', name=Tname,)
                else:
                    return render_template('login.html',message='try again password or email is incorrect')
            if(login_type=='student'):
                global Sname
    
                loginquery = "select * from {} where email=%s and password=%s".format(S_class_code)
                fetch_name = "select name from {} where email=%s and password=%s".format(S_class_code)
                notification_query = "select date,notification_data from notification_{}".format(S_class_code)
                print(loginquery,d)
                mycursor.execute(loginquery, d)
                user = mycursor.fetchall()
                mycursor.execute(notification_query)
                notifications = mycursor.fetchall()


                #return render_template('login.html',message="class code is wrong")



            if len(user) > 0:
                mycursor.execute(fetch_name, d)
                lname = [row[0] for row in mycursor.fetchall()]
                for name in lname:
                    Sname = name
                print(Sname)

                return render_template('main.html', name=Sname,notification=notifications)
            else:
                return render_template('login.html', message='try again password or email is incorrect')
@app.route('/teacher_main')
def teacher_main():
    return render_template('teacher_main.html')
@app.route('/main')
def main():
  return render_template('main.html')
@app.route('/attendance')
def attendance():
    roll_no_query = """select roll_no from {} where email="{}" """.format(S_class_code,login_email)
    mycursor.execute(roll_no_query)
    roll_no = [row[0] for row in mycursor.fetchall()]
    student_roll="select date,status from student_attendance_{} where roll_no='{}'".format(S_class_code,roll_no[0])
    mycursor.execute(student_roll)
    attendance_status= mycursor.fetchall()
    
    
    query_count="select count(status),status from student_attendance_{} where roll_no='{}' group by status".format(S_class_code,roll_no[0])
    mycursor.execute(query_count)
    count=mycursor.fetchall()
    present=int(count[0][0])
    absent=int(count[1][0])
    present_percent=present/(present+absent)*100
    
    



    


    return render_template('attendance.html',attendance_status=attendance_status,name=Sname,percent=present_percent)
@app.route('/take_attendance')

def take_attendance():
    global class_code
    fetch_classCode="select class_code from teachers_list where email=%s and password=%s"
    print(fetch_classCode)
    fetch_classCode_format=(login_email,login_password)
    print(fetch_classCode_format)
    mycursor.execute(fetch_classCode,fetch_classCode_format)
    code=mycursor.fetchone()
    print(code)
    class_code=code[0]
    print("class")
    print(class_code)
    students_name_query = "select name from {}".format(class_code)
    mycursor.execute(students_name_query)
    students_name =[row[0] for row in mycursor.fetchall()] 
    roll_no_query = "select roll_no from {}".format(class_code)
    mycursor.execute(roll_no_query)
    roll_no =[row[0] for row in mycursor.fetchall()] #don't understand
    print(students_name)


    return render_template('take_attendance.html',name_list=students_name,roll_no_list=roll_no)
@app.route('/take_data_attendance',methods=['post'])
def take_data_attendance():
    if request.method=='POST':
        student_attendance=request.form
        date=request.form.get('date')
        
        
        
        
            
        for roll_no,status in student_attendance.items():
            
            values=(date,roll_no,'name',status)
            query_update_attendance="insert into student_attendance_{} values(%s,%s,%s,%s)".format(class_code)
            mycursor.execute(query_update_attendance,values)
            mydb.commit()
    return render_template('take_attendance.html')    
@app.route('/otp_page')
def enter_otp():

    return render_template("otp_page.html")
@app.route('/forget_pass')
def forget_pass():
    return render_template('forget_pass.html')
@app.route('/forget_message',methods=['GET','POST'])
def forget_message():
    if(request.method=='POST'):
      global forget_email
      forget_email=request.form.get('forget_email')
      forgetquery="select * from login where email='{}'".format(forget_email)
      mycursor.execute(forgetquery)
      user=mycursor.fetchall()
      print(len(user))
      if len(user)>0:
        #send_otp(forget_email)
        return render_template("enter_otp_forget.html")
      else:
        return render_template("forget_pass.html",message="Email does not Exist")
@app.route('/enter_otp_forget')
def enter_otp_forget():
    return render_template('enter_otp_forget.html')
@app.route('/submit_otp_forget',methods=['GET','POST'])
def submit_otp_forget():
    if(request.method=='POST'):
        forget_otp=request.form.get('forget_otp')
        if(forget_otp==otp):
            password_query="select password from login where email= '{}'".format(forget_email)
            v=forget_email
            mycursor.execute(password_query,v)
            get_password=mycursor.fetchone()
            return render_template('submit_otp_forget.html',password=get_password)
        else:
            return render_template('submit_otp_forget.html',password="somthin wrong")
@app.route('/Edit_notification')
def Edit_notification():
  return render_template("Edit_notification.html")
@app.route('/get_notification_form_data',methods=['POST','GET'])
def get_notificaton_form_data():
    if request.method=='POST':
        notification=request.form.get('textarea')
        print(notification)
        create_notifi_table="insert into notification_{} values(curdate(),'{}')".format(S_class_code,notification)
        print(create_notifi_table)
        mycursor.execute(create_notifi_table)
        mydb.commit()

    return render_template("get_notification_form_data.html",message="successfully ADD")
@app.route('/give_marks')
def give_marks():
    roll_no_query="select roll_no from {}".format(S_class_code)
    mycursor.execute(roll_no_query)
    roll_no=[row[0] for row in mycursor.fetchall()]
    print(roll_no)
    return render_template('give_marks.html',roll_no=roll_no)
@app.route('/Data_give_marks',methods=['GET','POST'] )
def Data_give_marks():
    if request.method=='POST':
        exam_name=request.form.get('exam_name')
        roll_no=request.form.get('student_roll_no')
        max_mark=request.form.get('max_marks')
        subject=request.form.getlist('subject')
        marks=request.form.getlist('marks')

        for (x,y) in zip(subject,marks):
            print(x)
            print(y)
            insert_mark_query="insert into {}_{} values(%s,%s,%s,%s)".format(roll_no,S_class_code)
            insert_format=(exam_name,max_mark,x,y)
            mycursor.execute(insert_mark_query,insert_format)
        mydb.commit()
        return render_template("Data_give_marks.html",message="success fully updated")
@app.route('/my_marks')
def my_marks():
    roll_no_query = """select roll_no from {} where email="{}" """.format(S_class_code,login_email)
    mycursor.execute(roll_no_query)
    roll_no = [row[0] for row in mycursor.fetchall()]
    print(roll_no[0])

    query_exam = "select exam_name from {}_{} group by exam_name".format(roll_no[0],S_class_code,)
    mycursor.execute(query_exam)
    result = [row[0] for row in mycursor.fetchall()]

    return render_template("my_marks.html",exam_type=result)
@app.route('/result_data',methods=['post'])
def result_data():
    if request.method=="POST":
       exam_type=request.form.get('exams')
       roll_no_query = """select roll_no from {} where email="{}" """.format(S_class_code, login_email)
       mycursor.execute(roll_no_query)
       roll_no = [row[0] for row in mycursor.fetchall()]
       print(roll_no[0])
       query_exam = "select exam_name from {}_{} group by exam_name".format(roll_no[0], S_class_code)
       mycursor.execute(query_exam)
       Eresult = [row[0] for row in mycursor.fetchall()]

       query_marks = """select * from {}_{} where exam_name="{}" """.format(roll_no[0], S_class_code,exam_type)
       mycursor.execute(query_marks)
       result = mycursor.fetchall()
       Ename = result[0][0]

       print(query_marks)

       return render_template("my_marks.html", result=result, exam_name=Ename,exam_type=Eresult)
@app.route('/give_assignment')
def give_assignment():
    return render_template("give_assignment.html")
@app.route('/data_give_asignment' ,methods=['POST'])
def data_give_assignment():
    if request.method=="POST":
        subject=request.form.get('subject_name')
        assignment=request.form.get('assignment')
        last_date=request.form.get('last_date')
        assignment_query="insert into assignment_{} values(curdate(),%s,%s,%s)".format(S_class_code)
        q_format=(subject,assignment,last_date)
        mycursor.execute(assignment_query,q_format)
        mydb.commit()

        return render_template("data_give_asignment.html",message="successfully Done")
@app.route('/assignments')
def assignment():
    Select_asignments="select * from assignment_{}".format(S_class_code)
    mycursor.execute(Select_asignments)
    result=mycursor.fetchall()
    print(result)
    return render_template("assignments.html",result=result)
@app.route('/set_fee_status')    
def set_fee():
    return render_template('set_fee_status.html')
@app.route('/set_fee_data', methods=['POST'])
def set_fee_data():
    if request.method=="POST":
        roll_no=request.form.get('roll_no')
        month=request.form.get('month')
        date=request.form.get('date')
        rupees=request.form.get('rupees')
        
        query_insert="insert into fees_{} values(%s,%s,%s,%s)".format(S_class_code)
        insert_values=(roll_no,date,month,rupees)
        mycursor.execute(query_insert,insert_values)
        mydb.commit()
        return render_template('set_fee_data.html',message=rupees)
@app.route('/fee_status')
def fee_status():
    roll_no_query = """select roll_no from {} where email="{}" """.format(S_class_code, login_email)
    mycursor.execute(roll_no_query)
    roll_no = [row[0] for row in mycursor.fetchall()]
    
    select_query="""select * from fees_{} where roll_no="{}" """.format(S_class_code,roll_no[0])
    mycursor.execute(select_query)
    result=mycursor.fetchall()
    print(result[0])
    print(result[0][1])
    
    
    
    return render_template('fee_status.html',result=result)
        





if __name__ == '__main__': 

   app.run(debug=True)

