from flask import Flask ,render_template,request,session,redirect,send_file
from flask_mail import Mail, Message

import sqlite3
import pyrebase
from werkzeug.utils import secure_filename
import random
import smtplib
import string
import os
app=Flask(__name__)
mail=Mail(app)

app.config['MAIL_SERVER']='smtp.sendgrid.net'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = "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"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

def send_otp(email):
    

    otp=str(random.randint(4567,6785))
    
    
    msg = Message(" Enterschool email verificaton", sender = 'tanya.assistant1916@gmail.com', recipients = [email])
    msg.body = f"otp is {otp}"
    mail.send(msg)
    
    return otp
def send_notification(email,message):
    
    
    msg = Message(" Enterschool Notification", sender = 'tanya.assistant1916@gmail.com', recipients = [email])
    msg.body = message
    mail.send(msg)
    print("send  notify successfully")
    
    




mydb=sqlite3.connect('nitesh.db',check_same_thread=False)
mycursor=mydb.cursor()
config={    "apiKey": "AIzaSyC-x73AHgduv4CTXeYJu4rTjnrwDfj1yls",
    "authDomain": "enterschool-a70f5.firebaseapp.com",
    "databaseURL": "https://enterschool-a70f5.firebaseio.com",
    "projectId": "enterschool-a70f5",
    "storageBucket": "enterschool-a70f5.appspot.com",
    "messagingSenderId": "408802600224",
    "appId": "1:408802600224:web:3fe1983eb48f8cc0c4a345",
    "measurementId": "G-PVJMPYECRW"
    }
firebase=pyrebase.initialize_app(config)
storage=firebase.storage()
def random_generator():
    size=4 
    chars=string.ascii_lowercase
    string1=''.join(random.choice(chars) for x in range(size))
    string2=str(random.randint(1000,9000))
    code=string1+string2
    

    print(f"code is {code}")


    query="select class_code from teachers_list"
    mycursor.execute(query)
    result=mycursor.fetchall()
    if code in result[0]:
        code=random_generator()
        print(code)
    else:
        return code
        
        
        
        

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
    if(request.method=='POST'):
        name=request.form.get('name')
        email=request.form.get('email')
        mobile=request.form.get('mobile_no')
        password=request.form.get('password')
        school=request.form.get('school')
        rep_password=request.form.get('confirm_password')
        session['cr_name']=name
        session['cr_email']=email
        session['cr_mobile']=mobile
        session['cr_password']=password
        session['cr_school']=school
        

        q=(email,mobile)
        query_alreadyExist="""select * from teachers_list where email="{}" and mobile_no="{}" """.format(email,mobile)
        print(query_alreadyExist)
        mycursor.execute(query_alreadyExist)
        emails=mycursor.fetchall()

        if(len(emails)>0):
            return render_template('create_class.html',error="email already exist")

        elif(password==rep_password):
            print(email)
            session['otp']=send_otp(session['cr_email'])
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
        
        
        
        if(session['otp']==otp_value):
            
            
            session['class_code'] = random_generator()
            p=(session['cr_name'],session['cr_email'],session['cr_password'],session['cr_mobile'],session['cr_school'],session['class_code'])
            query="""insert into teachers_list values("{}","{}","{}","{}","{}","{}")""".format(session['cr_name'],session['cr_email'],session['cr_password'],session['cr_mobile'],session['cr_school'],session['class_code'])

            mycursor.execute(query)
            query_create="create table {}(name text,email text,password text,mobile_no integer,roll_no text,class_code text)".format(session['class_code'])
            mycursor.execute(query_create)
            create_student_attendance_table="create table student_attendance_{}(date blob,roll_no text,name text,status text)".format(session['class_code'])
            mycursor.execute(create_student_attendance_table)
            create_notifi_table = 'create table notification_{}(date blob,notification_data text)'.format(session['class_code'])
            mycursor.execute(create_notifi_table)
            create_assignment_table="create table assignment_{}(assign_date blob,subject text,assignment text,date blob,assignment_file text)".format(session['class_code'])
            mycursor.execute(create_assignment_table)
            create_fee_table="create table fees_{}(roll_no text,date blob,month text,rupees text)".format(session['class_code'])
            mycursor.execute(create_fee_table)
            mydb.commit()
            print('executed')
            send_notification(session['cr_email'],"successfully class created.your class code is    {}   .please remember this code for in Future use".format(session['class_code']))
           
            return redirect(url_for("login", message="successfully class created"))
        else:
            return render_template('otp_page.html',message="incorrect otp try again")
@app.route('/join_class_form',methods=['POST'])
def join_class_form():
    

    if request.method=='POST':
        Sname = request.form.get('name')
        Semail = request.form.get('email')
        Smobile = request.form.get('mobile_no')
        Spassword = request.form.get('password')
        Sschool = request.form.get('school')
        Srep_password = request.form.get('confirm_password')
        roll_no=request.form.get('roll_no')
        class_code=request.form.get('class_code')
        session['jo_name']=Sname
        session['jo_email']=Semail
        session['jo_mobile']=Smobile
        session['jo_password']=Spassword
        session['jo_school']=Sschool
        session['jo_roll_no']=roll_no
        session['jo_class_code']=class_code
        q = (Semail, Smobile)
        query_alreadyExist = """select * from {} where email= "{}" and mobile_no="{}" """.format(class_code,Semail,Smobile)
        print(query_alreadyExist,q)
        mycursor.execute(query_alreadyExist)
        emails = mycursor.fetchall()

        if (len(emails) > 0):
            return render_template('join_class.html', error="email already exist")

        elif (Spassword == Srep_password):

            session['otp']=send_otp(session['jo_email'])
            print("otp send")

            return render_template("student_otp_page.html")
        else:
            return render_template('join_class.html', error="password is not match")

@app.route('/student_otp_formdata',methods=['POST'])
def student_otp_formdata():
    if (request.method == 'POST'):
        otp_value = request.form.get('otp')
        
        

        if (session['otp'] == otp_value):

            p = (session['jo_name'],session['jo_email'], session['jo_password'], session['jo_mobile'], session['jo_roll_no'],session['jo_class_code'])
            query = """insert into {} values("{}","{}","{}","{}","{}","{}")""".format(session['jo_class_code'],session['jo_name'],session['jo_email'], session['jo_password'], session['jo_mobile'], session['jo_roll_no'],session['jo_class_code'])
            mycursor.execute(query)
            
            create_marks_table="create table '{}_{}'(exam_name text,max_mark integer,subject text,mark integer)".format(session['jo_roll_no'],session['jo_class_code'])
            mycursor.execute(create_marks_table)
            mydb.commit()

            return render_template("login.html", message="successfully class joined")
        else:
            return render_template('student_otp_page.html', message="incorrect otp try again")


@app.route('/login_formdata', methods=['GET','POST'])
def login_message():
    
    if(request.method=='POST'):
        login_type=request.form.get('login_type')
        login_email=request.form.get('email')
        login_password=request.form.get('password')
        S_class_code=request.form.get('class_code')
        session['lemail']=login_email
        session['class_code']=S_class_code
        session['pass']=login_password
        d=(session['lemail'],session['pass'])
        logincodequery="select * from teachers_list where class_code='{}'".format(session['class_code'])
        mycursor.execute(logincodequery)
        logincode=mycursor.fetchall()
        if len(logincode)>0:
        
            if 'lemail' in session:
                if(login_type=='teacher'):
                    loginquery="""select * from teachers_list where email="{}" and password="{}" """.format(session['lemail'],session['pass'])
                    fetch_name="""select name from teachers_list where email="{}" and password="{}" """.format(session['lemail'],session['pass'])
        
                    mycursor.execute(loginquery)
                    user=mycursor.fetchall()
        
        
                    print(len(user))
                    if len(user)>0:
                      mycursor.execute(fetch_name)
                      Tname = [row[0] for row in mycursor.fetchall()]
                      print(Tname)
                      for value in Tname:
                        session['tname']=value
        
                      return render_template('teacher_main.html', name=session['tname'])
                    else:
                        return render_template('login.html',message='try again password or email is incorrect')
                if(login_type=='student'):
                    
        
                    loginquery = """select * from {} where email="{}" and password="{}" """.format(session['class_code'],session['lemail'],session['pass'])
                    fetch_name = """select name from {} where email="{}" and password="{}" """.format(session['class_code'],session['lemail'],session['pass'])
                    notification_query = "select date,notification_data from notification_{}".format(session['class_code'])
                    print(loginquery,d)
                    mycursor.execute(loginquery)
                    user = mycursor.fetchall()
                    mycursor.execute(notification_query)
                    notifications = mycursor.fetchall()
    
    
                    #return render_template('login.html',message="class code is wrong")
    
    
    
                if len(user) > 0:
                    mycursor.execute(fetch_name)
                    lname = [row[0] for row in mycursor.fetchall()]
                    for name in lname:
                      session['Sname']=name
                       
                    
    
                    return render_template('main.html', name=session['Sname'],notification=notifications)
                else:
                    return render_template('login.html', message='try again password or email is incorrect')
        else:
            return render_template('login.html',message='class code is wrong')
@app.route('/teacher_main')
def teacher_main():
    return render_template('teacher_main.html',name=session['tname'])
@app.route('/main')
def main():
  return render_template('main.html',name=session['Sname'])
@app.route('/attendance')
def attendance():
    roll_no_query = """select roll_no from {} where email="{}" """.format(session['class_code'],session['lemail'])
    mycursor.execute(roll_no_query)
    roll_no = [row[0] for row in mycursor.fetchall()]
    student_roll="select date,status from student_attendance_{} where roll_no='{}'".format(session['class_code'],roll_no[0])
    mycursor.execute(student_roll)
    attendance_status= mycursor.fetchall()
    
    
    query_count="select count(status),status from student_attendance_{} where roll_no='{}' group by status".format(session['class_code'],roll_no[0])
    mycursor.execute(query_count)
    count=mycursor.fetchall()
    try:
        present=int(count[0][0])
        try:
          absent=int(count[1][0])
        except:
          absent=0  
        present_percent=int(present/(present+absent)*100)
        return render_template('attendance.html',attendance_status=attendance_status,name=session['Sname'],percent=present_percent)
    except:
        return render_template("otp_message.html",message="No data Found")
@app.route('/take_attendance')

def take_attendance():
    
    
    fetch_classCode="""select class_code from teachers_list where email="{}" and password="{}" """.format(session['lemail'],session['pass'])
    print(fetch_classCode)
    fetch_classCode_format=(session['lemail'],session['pass'])
    print(fetch_classCode_format)
    mycursor.execute(fetch_classCode)
    code=mycursor.fetchone()
    print(code)
    session['Tclass_code']=code[0]
    print("class")
    
    students_name_query = "select name from {}".format(session['Tclass_code'])
    mycursor.execute(students_name_query)
    students_name =[row[0] for row in mycursor.fetchall()] 
    roll_no_query = "select roll_no from {}".format(session['class_code'])
    mycursor.execute(roll_no_query)
    roll_no =[row[0] for row in mycursor.fetchall()] #don't understand
    print(students_name)


    return render_template('take_attendance.html',name_list=students_name,roll_no_list=roll_no)
@app.route('/take_data_attendance',methods=['post'])
def take_data_attendance():
    if request.method=='POST':
        student_attendance=request.form
        date=request.form.get('date')
        mdate=request.form.get('mdate')
        mroll=request.form.get('mroll_no')
        mstatus=request.form.get('mstatus')
        
        
        
        
        if mdate is None : 
           print(date)   
           for roll_no,status in student_attendance.items():
            
               values=(date,roll_no,'name',status)
               query_update_attendance=""" insert into student_attendance_{} values("{}","{}","{}","{}")""".format(session['Tclass_code'],date,roll_no,'name',status)
               mycursor.execute(query_update_attendance,values)
               mydb.commit()
        if date is None:
          
            
            query_date="""select * from student_attendance_{} where date="{}" """.format(session['Tclass_code'],mdate)
            mycursor.execute(query_date)
            date_result=mycursor.fetchall()
            print(date_result)
            if len(date_result)> 0:
            
                query_reupdate="""update student_attendance_{} set status="{}" where roll_no="{}" and date="{}" """.format(session['Tclass_code'],mstatus,mroll,mdate)       
                re_values=(mstatus,mroll,mdate)
                print(mroll,mdate,mstatus)
                mycursor.execute(query_reupdate)
                mydb.commit()    
                print("succees")
            else :    
              
                return render_template('otp_message.html',message="can't update because you were not taken attendance on this date")   
    return redirect('take_attendance')    
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
        create_notifi_table="insert into notification_{} values(current_date,'{}')".format(session['class_code'],notification)
        print(create_notifi_table)
        mycursor.execute(create_notifi_table)
        mydb.commit()

    return render_template("get_notification_form_data.html",message="successfully ADD")
@app.route('/give_marks')
def give_marks():
    roll_no_query="select roll_no from {}".format(session['class_code'])
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
            insert_mark_query="""insert into {}_{} values("{}","{}","{}","{}")""".format(roll_no,session['class_code'],exam_name,max_mark,x,y)
            insert_format=(exam_name,max_mark,x,y)
            mycursor.execute(insert_mark_query)
        mydb.commit()
        return render_template("Data_give_marks.html",message="success fully updated")
@app.route('/my_marks')
def my_marks():
    roll_no_query = """select roll_no from {} where email="{}" """.format(session['class_code'],session['lemail'])
    mycursor.execute(roll_no_query)
    roll_no = [row[0] for row in mycursor.fetchall()]
    print(roll_no[0])

    query_exam = "select exam_name from {}_{} group by exam_name".format(roll_no[0],session['class_code'],)
    mycursor.execute(query_exam)
    result = [row[0] for row in mycursor.fetchall()]

    return render_template("my_marks.html",exam_type=result,name=session['Sname'])
@app.route('/result_data',methods=['post'])
def result_data():
    if request.method=="POST":
       exam_type=request.form.get('exams')
       roll_no_query = """select roll_no from {} where email="{}" """.format(session['class_code'], login_email)
       mycursor.execute(roll_no_query)
       roll_no = [row[0] for row in mycursor.fetchall()]
       print(roll_no[0])
       query_exam = "select exam_name from {}_{} group by exam_name".format(roll_no[0], session['class_code'])
       mycursor.execute(query_exam)
       Eresult = [row[0] for row in mycursor.fetchall()]

       query_marks = """select * from {}_{} where exam_name="{}" """.format(roll_no[0], session['class_code'],exam_type)
       mycursor.execute(query_marks)
       result = mycursor.fetchall()
       Ename = result[0][0]

       print(query_marks)

       return render_template("my_marks.html", result=result, exam_name=Ename,exam_type=Eresult)
@app.route('/give_assignment')
def give_assignment():
    return render_template("give_assignment.html" ,name=session['tname'])
@app.route('/data_give_asignment' ,methods=['POST'])
def data_give_assignment():
    if request.method=="POST":
        subject=request.form.get('subject_name')
        assignment=request.form.get('assignment')
        last_date=request.form.get('last_date')
        assignment_file=request.files['upload_file']
        assignment_filename=assignment_file.filename.replace(" ","")
        cloud_path='{}_uploads/{}'.format(session['class_code'],assignment_filename)
        storage.child(cloud_path).put(assignment_file)
        print(assignment_filename)
        assignment_query="""insert into assignment_{} values(current_date,"{}","{}","{}","{}")""".format(session['class_code'],subject,assignment,last_date,assignment_filename)
        q_format=(subject,assignment,last_date,assignment_filename)
        mycursor.execute(assignment_query)
        mydb.commit()

        return render_template("data_give_asignment.html",message="successfully Done")
@app.route('/assignments')
def assignment():
    Select_asignments="select * from assignment_{}".format(session['class_code'])
    mycursor.execute(Select_asignments)
    result=mycursor.fetchall()
    print(result)
    return render_template("assignments.html",result=result,name=session['Sname'])
@app.route('/downloads/<file_name>' ,methods=['GET'])
def download_file(file_name):
    attached_filename=file_name
    download_path='{}_uploads/{}'.format(session['class_code'],attached_filename)
    links=storage.child(download_path).get_url(None)
    print(links)
    return f"""<html> <body><a href="{links}" download>Downloads</a></body><html>"""
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
        
        query_insert="""insert into fees_{} values("{}","{}","{}","{}")""".format(session['class_code'],roll_no,date,month,rupees)
        insert_values=(roll_no,date,month,rupees)
        mycursor.execute(query_insert)
        mydb.commit()
        return render_template('set_fee_data.html',message=rupees)
@app.route('/fee_status')
def fee_status():
    roll_no_query = """select roll_no from {} where email="{}" """.format(session['class_code'],session['lemail'])
    mycursor.execute(roll_no_query)
    roll_no = [row[0] for row in mycursor.fetchall()]
    
    select_query="""select * from fees_{} where roll_no="{}" """.format(session['class_code'],roll_no[0])
    mycursor.execute(select_query)
    result=mycursor.fetchall()
      
    
    
    
    return render_template('fee_status.html',result=result,name=session['Sname'])
        





if __name__ == '__main__': 

   app.run(debug=True)

