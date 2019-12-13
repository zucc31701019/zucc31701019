import threading
import time

from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import  login
import model
import drawtest
from flask_mail import Mail, Message
import pymysql, random, xlrd
pymysql.install_as_MySQLdb()
import arrange
# import tkinter as tk
from tkinter import filedialog
from mttkinter import mtTkinter as tk


ccheck = ''

# app = Flask(__name__)

# @app.route('/')
# def signin():
#     return render_template('index3.html')

model.app.config['MAIL_SERVER'] = 'smtp.qq.com'
model.app.config['MAIL_PORT'] = 465
model.app.config['MAIL_USE_SSL'] = True
model.app.config['MAIL_USE_TLS'] = False
model.app.config['MAIL_USERNAME'] = '1330172898@qq.com'
model.app.config['MAIL_PASSWORD'] = 'wnuxpwmftumbifjg'
mail = Mail(model.app)

# @model.app.route('/sign up/')
# def signup():
#     return render_template('sign-up3.html')
#
# @model.app.route('/forgot/')
# def forgot():
#     return render_template('forgot3.html')
#
# @model.app.route('/student/')
# def stu():
#     return render_template('student_main.html')




# @app.route('/',methods=['GET','POST'])
# def login():
#     if request.method == "POST":
#       username = request.form.get('username')
#       password = request.form.get('password')
#       print(username)
#       print(password)
#       data = model.student.query.filter(model.student.saccount == username).first()
#       pwd = data.spwd
#       if data == None:
#          return  'hhhhh'
#       else:
#           if pwd == password:
#               return render_template('student_main.html')
#
#     return render_template('index3.html')

# @model.app.route('/', methods=['GET', 'POST'])
# def signin():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         data = model.student.query.filter(model.student.saccount == username).first()
#         if(data == None ):
#             print('wrong1')
#         else:
#             if(password != data.spwd):
#                 print('wrong2')
#             else:
#                 return render_template('student_main.html')
#     return render_template('index3.html')

# @model.app.route('/', methods=['GET', 'POST'])
# def signin():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         data1 = model.admin.query.filter(model.admin.aaccount == username).first()
#         data2 = model.teacher.query.filter(model.teacher.taccount == username).first()
#         data3 = model.student.query.filter(model.student.saccount == username).first()
#         if data3 != None:
#             data = data3
#             if password != data.spwd:
#                 flash('账户或密码错误')
#             else:
#                 return redirect(url_for('student_main', Id=username))
#         elif data2 != None:
#             data = data2
#             if password != data.tpwd:
#                 flash('账户或密码错误')
#             else:
#                 return redirect(url_for('student_main', Id=username))
#         elif data1 != None:
#             data = data1
#             if password != data.apwd:
#                 flash('账户或密码错误')
#             else:
#                 return redirect(url_for('student_main', Id=username))
#         else:
#             flash('账户或密码错误')
#     return render_template('index3.html')

@model.app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        data1 = model.teacher.query.filter(model.teacher.tId == username).first()
        data2 = model.student.query.filter(model.student.sId == username).first()
        if data1 != None:
            if password != data1.tpwd:
                flash('账户或密码错误')
            else:
                if data1.identity == 'a':
                    return redirect(url_for('Admin', Id=username))
                elif data1.identity == 't':
                    return redirect(url_for('Teacher', Id=username))
        elif data2 != None:
            if password != data2.spwd:
                flash('账户或密码错误')
            else:
                return redirect(url_for('Student', Id=username))
        else:
            flash('账户或密码错误')
    return render_template('index3.html')

@model.app.route('/sign up/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        id = request.form.get('id')
        email = request.form.get('email')
        password = request.form.get('password')
        repassword = request.form.get('re-password')
        data1 = model.teacher.query.filter(model.teacher.tId == id).first()
        data2 = model.student.query.filter(model.student.sId == id).first()
        if data1 != None:
            if data1.tpwd != None:
                flash('已进行注册')
            else:
                if not all([email, password, repassword]):
                    flash('信息不完整')
                elif password != repassword:
                    flash('密码不一致')
                else:
                    flash("注册成功，请登录")
                    data1.temail = email
                    data1.tpwd = password
                    data1.tcheck = 0
                    model.db.session.add(data1)
                    model.db.session.commit()
                    return redirect('/#signin')
        elif data2 != None:
            if data2.spwd != None:
                flash('已进行注册')
            else:
                if not all([email, password, repassword]):
                    flash('信息不完整')
                elif password != repassword:
                    flash('密码不一致')
                else:
                    flash("注册成功，请登录")
                    data2.semail = email
                    data2.spwd = password
                    data2.scheck = 0
                    model.db.session.add(data2)
                    model.db.session.commit()
                    # flash("注册成功，即将跳转登录界面")
                    time.sleep(3)
                    return redirect('/#signin')
        else:
            flash('该ID不存在')
    return render_template('sign-up3.html')

@model.app.route('/forgot3/', methods=['GET', 'POST'])
def forgot3():
    if request.method =='POST':
        id = request.form.get('Id')
        data1 = model.teacher.query.filter(model.teacher.tId == id).first()
        data2 = model.student.query.filter(model.student.sId == id).first()
        code = ''
        for i in range(0,6):
            code = code + str(random.randint(0,9))
            global ccheck
            ccheck = code
        if data1 != None:
            identity = 't'
            email = data1.temail
            msg = Message('', sender='1330172898@qq.com', recipients=[email])
            msg.body = '验证码:' + code
            with model.app.app_context():
                mail.send(msg)
            return redirect(url_for('forgot4', code = code, identity = identity, id = id))
        elif data2 != None:
            identity = 's'
            email = data2.semail
            msg = Message('', sender='1330172898@qq.com', recipients=[email])
            msg.body = '验证码:'+code
            with model.app.app_context():
                mail.send(msg)
            return redirect(url_for('forgot4',identity = identity, id = id))
        else:
            flash('Id输入错误')
    return render_template('forgot3.html')

@model.app.route('/forgot4/?<string:identity>?<string:id>', methods=['GET', 'POST'])
def forgot4(identity, id):
    if request.method == 'POST':
        global ccheck
        VerificationCode = request.form.get('VerificationCode')
        newpwd = request.form.get('newpwd')
        if VerificationCode == ccheck:
            if newpwd !=None:
                if identity == 't':
                    tea =model.teacher.query.filter(model.teacher.tId == id).first()
                    tea.tpwd = newpwd
                    model.db.session.add(tea)
                    model.db.session.commit()
                    return redirect(url_for('signin'))
                else:
                    stu = model.student.query.filter(model.student.sId == id).first()
                    stu.spwd = newpwd
                    model.db.session.add(stu)
                    model.db.session.commit()
                    return redirect(url_for('signin'))
            else:
                flash('密码不能为空')
        else:
            flash('验证码错误')
    return render_template('forgot4.html', identity = identity, id = id)

@model.app.route('/Admin/<string:Id>', methods=['GET', 'POST'])
def Admin(Id):
    return render_template('Admin2.html', Id = Id)

@model.app.route('/Adminexam/<string:Id>', methods=['GET', 'POST'])
def Adminexam(Id):
    num = model.exam.query.count()
    data = model.exam.query.all()
    list = []
    my_list = []
    my_list.append('课程编号')
    my_list.append('课程名称')
    my_list.append('教学楼')
    my_list.append('教室')
    my_list.append('考试时间')
    for i in range(0,num):
        course_code = data[i].course_code
        academicbuilding = data[i].academicbuilding
        classroomId = data[i].classroomId
        course_name = data[i].course_name
        time = data[i].time
        my_list = []
        my_list.append(course_code)
        my_list.append(course_name)
        my_list.append(academicbuilding)
        my_list.append(classroomId)
        my_list.append(time)
        list.append(my_list)
    return render_template('Adminexam.html', Id = Id, list = list)

@model.app.route('/Admintest/<string:Id>', methods=['GET', 'POST'])
def Admintest(Id):
    num = model.test.query.count()
    data = model.test.query.all()
    list = []
    my_list = []
    my_list.append('课程编号')
    my_list.append('课程名称')
    my_list.append('姓名')
    my_list.append('考试时间')
    my_list.append('教学楼')
    my_list.append('教室')
    my_list.append('座位号')
    list.append(my_list)
    for i in range(0, num):
        course_code = data[i].course_code
        course_name = data[i].course_name
        name = data[i].sname
        time = data[i].time
        academicbuilding = data[i].academicbuilding
        classroomId = data[i].classroomId
        seat = data[i].seat
        my_list = []
        my_list.append(course_code)
        my_list.append(course_name)
        my_list.append(name)
        my_list.append(time)
        my_list.append(academicbuilding)
        my_list.append(classroomId)
        my_list.append(seat)
        list.append(my_list)
    return render_template('Admintest.html', Id = Id, list = list)

@model.app.route('/Admininvigilate/<string:Id>', methods=['GET', 'POST'])
def Admininvigilate(Id):
    num = model.invigilate.query.count()
    data = model.invigilate.query.all()
    list = []
    my_list = []
    my_list.append('课程编号')
    my_list.append('课程名称')
    my_list.append('姓名')
    my_list.append('监考时间')
    my_list.append('教学楼')
    my_list.append('教室')
    my_list.append('监考/巡考')
    list.append(my_list)
    for i in range(0, num):
        course_code = data[i].course_code
        course_name = data[i].course_name
        name = data[i].tname
        time = data[i].time
        academicbuilding = data[i].academicbuilding
        classroomId = data[i].classroomId
        if data[i].isstop == 0:
            type = "巡考"
        else:
            type = "监考"
        my_list = []
        my_list.append(course_code)
        my_list.append(course_name)
        my_list.append(name)
        my_list.append(time)
        my_list.append(academicbuilding)
        my_list.append(classroomId)
        my_list.append(type)
        list.append(my_list)
    return render_template('Admininvigilate.html', Id = Id, list = list)

@model.app.route('/Admina/<string:Id>', methods=['GET', 'POST'])
def Admina(Id):
    num = model.teacher.query.filter(model.teacher.tcheck == 0).count()
    data = model.teacher.query.filter(model.teacher.tcheck == 0).all()
    num2 = model.student.query.filter(model.student.scheck == 0).count()
    data2 = model.student.query.filter(model.student.scheck == 0).all()
    list = []
    my_list = []
    my_list.append('教师编号')
    my_list.append('姓名')
    my_list.append('是否查看')
    list.append(my_list)
    list2 =[]
    my_list2 = []
    my_list2.append('学生编号')
    my_list2.append('姓名')
    my_list2.append('是否查看')
    list2.append(my_list2)
    for i in range(0, num):
        tId = data[i].tId
        name = data[i].tname
        my_list = []
        my_list.append(tId)
        my_list.append(name)
        my_list.append('否')
        list.append(my_list)
    for i in range(0,num2):
        sId = data2[i].sId
        name2 = data2[i].sname
        my_list2 = []
        my_list2.append(sId)
        my_list2.append(name2)
        my_list2.append('否')
        list2.append(my_list2)
    if request.method == 'POST':
        for i in range(0,num):
            email = data[i].temail
            msg = Message('', sender='1330172898@qq.com', recipients=[email])
            msg.body = '请尽快登录教务管理系统查看监考巡考信息'
            with model.app.app_context():
                mail.send(msg)
        for i in range(0,num2):
            email = data[2].semail
            msg = Message('', sender='1330172898@qq.com', recipients=[email])
            msg.body = '请尽快登录教务管理系统查看考试信息'
            with model.app.app_context():
                mail.send(msg)
    return render_template('Admina.html', Id = Id, list = list, list2 = list2)

@model.app.route('/admchangePwd/?<string:Id>', methods=['GET', 'POST'])
def admchangePwd(Id):
    if request.method == 'POST':
        oldpwd = request.form.get('oldpwd')
        newpwd1 = request.form.get('newpwd1')
        newpwd2 = request.form.get('newpwd2')
        if not all([oldpwd, newpwd1, newpwd2]):
            flash('信息不完整')
        else:
            data = model.teacher.query.filter(model.teacher.tId == Id).first()
            pwd = data.tpwd
            if pwd == oldpwd:
                if newpwd1 != newpwd2:
                    flash('密码输入不一致')
                else:
                    data.tpwd = newpwd1
                    model.db.session.add(data)
                    model.db.session.commit()
                    flash('密码修改成功')
            else:
                flash('原密码输入错误')
    return render_template('admchangePwd.html', Id=Id)


@model.app.route('/stuchangePwd/?<string:Id>', methods=['GET', 'POST'])
def stuchangePwd(Id):
    if request.method == 'POST':
        oldpwd = request.form.get('oldpwd')
        newpwd1 = request.form.get('newpwd1')
        newpwd2 = request.form.get('newpwd2')
        if not all([oldpwd, newpwd1, newpwd2]):
            flash('信息不完整')
        else:
            data = model.student.query.filter(model.student.sId == Id).first()
            pwd = data.spwd
            if pwd == oldpwd:
                if newpwd1 != newpwd2:
                    flash('密码输入不一致')
                else:
                    data.spwd = newpwd1
                    model.db.session.add(data)
                    model.db.session.commit()
                    flash('密码修改成功')
            else:
                flash('原密码输入错误')
    return render_template('stuchangePwd.html', Id = Id)

@model.app.route('/teachangePwd/?<string:Id>', methods=['GET', 'POST'])
def teachangePwd(Id):
    if request.method == 'POST':
        oldpwd = request.form.get('oldpwd')
        newpwd1 = request.form.get('newpwd1')
        newpwd2 = request.form.get('newpwd2')
        if not all([oldpwd, newpwd1, newpwd2]):
            flash('信息不完整')
        else:
            data = model.teacher.query.filter(model.teacher.tId == Id).first()
            pwd = data.tpwd
            if pwd == oldpwd:
                if newpwd1 != newpwd2:
                    flash('密码输入不一致')
                else:
                    data.tpwd = newpwd1
                    model.db.session.add(data)
                    model.db.session.commit()
                    flash('密码修改成功')
            else:
                flash('原密码输入错误')
    return render_template('teachangePwd.html', Id=Id)

@model.app.route('/Student/<string:Id>', methods=['GET', 'POST'])
def Student(Id):
    num = model.test.query.filter(model.test.sId == Id).count()
    data = model.test.query.filter(model.test.sId == Id).all()
    stu = model.student.query.filter(model.student.sId == Id).first()
    stu.scheck = 1
    model.db.session.add(stu)
    model.db.session.commit()
    list = []
    my_list=[]
    my_list.append('课程编号')
    my_list.append('课程名称')
    my_list.append('姓名')
    my_list.append('考试时间')
    my_list.append('教学楼')
    my_list.append('教室')
    my_list.append('座位号')
    list.append(my_list)
    for i in range(0, num):
        course_code = data[i].course_code
        course_name = data[i].course_name
        name = data[i].sname
        time = data[i].time
        academicbuilding = data[i].academicbuilding
        classroomId = data[i].classroomId
        seat = data[i].seat
        my_list = []
        my_list.append(course_code)
        my_list.append(course_name)
        my_list.append(name)
        my_list.append(time)
        my_list.append(academicbuilding)
        my_list.append(classroomId)
        my_list.append(seat)
        list.append(my_list)
    return render_template('Student.html', list = list, Id = Id)

@model.app.route('/Teacher/<string:Id>', methods=['GET', 'POST'])
def Teacher(Id):
    num = model.invigilate.query.filter(model.invigilate.tId == Id).count()
    data = model.invigilate.query.filter(model.invigilate.tId == Id).all()
    tea = model.teacher.query.filter(model.teacher.tId == Id).first()
    tea.tcheck = 1
    model.db.session.add(tea)
    model.db.session.commit()
    list = []
    my_list = []
    my_list.append('课程编号')
    my_list.append('课程名称')
    my_list.append('姓名')
    my_list.append('监考时间')
    my_list.append('教学楼')
    my_list.append('教室')
    my_list.append('监考/巡考')
    list.append(my_list)
    for i in range(0, num):
        course_code = data[i].course_code
        course_name = data[i].course_name
        name = data[i].tname
        time = data[i].time
        academicbuilding = data[i].academicbuilding
        classroomId = data[i].classroomId
        if data[i].isstop == 0:
            type = "巡考"
        else:
            type = "监考"
        my_list = []
        my_list.append(course_code)
        my_list.append(course_name)
        my_list.append(name)
        my_list.append(time)
        my_list.append(academicbuilding)
        my_list.append(classroomId)
        my_list.append(type)
        list.append(my_list)
    return render_template('Teacher.html', list=list, Id = Id)



# @model.app.route('/student_main/?<string:Id>', methods=['GET', 'POST'])
# def student_main(Id):
#     if request.method == 'POST':
#         num = model.test.query.filter(model.test.sId == Id).count()
#         data = model.test.query.filter(model.test.sId == Id).all()
#         stu = model.student.query.filter(model.student.sId == Id).first()
#         # print(stu.scheck)
#         stu.scheck = True
#         model.db.session.add(stu)
#         model.db.session.commit()
#         list = []
#         for i in range(0, num):
#             course_code = data[i].course_code
#             course_name = data[i].course_name
#             sname = data[i].sname
#             time = data[i].time
#             academicbuilding = data[i].academicbuilding
#             classroomId = data[i].classroomId
#             seat = data[i].seat
#             my_list = []
#             my_list.append(course_code)
#             my_list.append(course_name)
#             my_list.append(sname)
#             my_list.append(time)
#             my_list.append(academicbuilding)
#             my_list.append(classroomId)
#             my_list.append(seat)
#             list.append(my_list)
#         return render_template('student_index.html', list = list)
#     return render_template('student_index.html')
#
#
# @model.app.route('/admin_main?<string:Id>', methods=['GET', 'POST'])
# def admin_main(Id):
#     if request.method == 'POST':
#         num = model.exam.query.count()
#         data = model.exam.query.all()
#         list = []
#         for i in range(0, num):
#             course_code = data[i].course_code
#             course_name = data[i].course_name
#             time = data[i].time
#             academicbuilding = data[i].academicbuilding
#             classroomId = data[i].classroomId
#             my_list = []
#             my_list.append(course_code)
#             my_list.append(course_name)
#             my_list.append(time)
#             my_list.append(academicbuilding)
#             my_list.append(classroomId)
#             list.append(my_list)
#         return render_template('student_index.html', list = list)
#     return render_template('student_index.html')

@model.app.route('/Input1/?<string:Id>', methods=['GET', 'POST'])
def Input1(Id):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    book = xlrd.open_workbook(file_path)
    list = book.sheets()
    print(list)
    sheet_names = book.sheet_names()
    print(sheet_names)
    print(len(sheet_names[1]))
    try:
        conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='',
        db='arrangement',
        port=3306,
        charset='utf8'
        )
        cur = conn.cursor()
        query = 'insert into student(sId,sname,sclass,grade) values(%s, %s, %s, %s);'
        for i in sheet_names:
            sheet_i = book.sheet_by_name(i)
            for r in range(1, sheet_i.nrows):
                a1 = sheet_i.cell(r, 0).value
                a2 = sheet_i.cell(r, 1).value
                a3 = sheet_i.cell(r, 2).value
                a4 = sheet_i.cell(r, 3).value
                values = (a1, a2, a3, a4)
                cur.execute(query, values)
            cur.close()
            conn.commit()
            conn.close()
            flash("导入成功")
    except Exception as e:
        flash(e)
    root.mainloop()
    return render_template('Input1.html', Id=Id)



@model.app.route('/Input2/?<string:Id>')
def Input2(Id):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    book = xlrd.open_workbook(file_path)
    list = book.sheets()
    print(list)
    sheet_names = book.sheet_names()
    print(sheet_names)
    print(len(sheet_names[0]))
    try:
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            passwd='',
            db='arrangement',
            port=3306,
            charset='utf8'
        )
        cur = conn.cursor()
        query = 'insert into teacher(tId,tname,identity) values(%s, %s, %s);'
        for i in sheet_names:
            sheet_i = book.sheet_by_name(i)
            for r in range(1, sheet_i.nrows):
                a1 = sheet_i.cell(r, 0).value
                a2 = sheet_i.cell(r, 1).value
                a3 = sheet_i.cell(r, 2).value
                values = (a1, a2, a3)
                cur.execute(query, values)
        cur.close()
        conn.commit()
        conn.close()

    except Exception as e:
        flash(e)
    flash("导入成功")
    root.mainloop()
    return render_template('Input2.html', Id=Id)

@model.app.route('/Input3/?<string:Id>')
def Input3(Id):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    book = xlrd.open_workbook(file_path)
    list = book.sheets()
    print(list)
    sheet_names = book.sheet_names()
    print(sheet_names)
    print(len(sheet_names[0]))
    try:
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            passwd='',
            db='arrangement',
            port=3306,
            charset='utf8'
        )
        cur = conn.cursor()
        query = 'insert into course(course_code,course_name,teachingteacher,istest,iscomputer,year,month,day,time,teacher_id,str_time) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
        for i in sheet_names:
            sheet_i = book.sheet_by_name(i)
            for r in range(1, sheet_i.nrows):
                a1 = sheet_i.cell(r, 0).value
                a2 = sheet_i.cell(r, 1).value
                a3 = sheet_i.cell(r, 2).value
                a4 = int(sheet_i.cell(r, 3).value)
                a5 = int(sheet_i.cell(r, 4).value)
                a6 = int(sheet_i.cell(r, 5).value)
                a7 = int(sheet_i.cell(r, 6).value)
                a8 = int(sheet_i.cell(r, 7).value)
                a9 = int(sheet_i.cell(r, 8).value)
                a10 = sheet_i.cell(r, 9).value
                t = '8: 10 - 10: 10'
                if int(a9) == 1:
                    t='8: 10 - 10: 10'
                elif int(a9) == 2:
                    t='10: 40 - 12: 40'
                elif int(a9) == 3:
                    t='14: 00 - 16: 00'
                a11 = str(a6)+'年'+str(a7)+'月'+str(a8)+'日 '+t
                values = (a1, a2, a3, int(a4), int(a5), int(a6), int(a7), int(a8), int(a9), a10, a11)
                cur.execute(query, values)
        cur.close()
        conn.commit()
        conn.close()
    except Exception as e:
        flash(e)
    flash("导入成功")
    root.mainloop()
    return render_template('Input3.html', Id = Id)

@model.app.route('/Input4/?<string:Id>')
def Input4(Id):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    book = xlrd.open_workbook(file_path)
    list = book.sheets()
    print(list)
    sheet_names = book.sheet_names()
    print(sheet_names)
    print(len(sheet_names[0]))
    try:
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            passwd='',
            db='arrangement',
            port=3306,
            charset='utf8'
        )
        cur = conn.cursor()
        query = 'insert into study(sId,course_code,sname,grade,sclass,course_name) values(%s, %s, %s, %s, %s, %s);'
        for i in sheet_names:
            sheet_i = book.sheet_by_name(i)
            for r in range(1, sheet_i.nrows):
                a1 = sheet_i.cell(r, 0).value
                a2 = sheet_i.cell(r, 1).value
                a3 = sheet_i.cell(r, 2).value
                a4 = sheet_i.cell(r, 3).value
                a5 = sheet_i.cell(r, 4).value
                a6 = sheet_i.cell(r, 5).value
                values = (a1, a2, a3, a4, a5, a6)
                cur.execute(query, values)
        cur.close()
        conn.commit()
        conn.close()
    except Exception as e:
        flash(e)
    flash("导入成功")
    root.mainloop()
    return render_template('Input4.html', Id = Id)

@model.app.route('/Input5/?<string:Id>')
def Input5(Id):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    book = xlrd.open_workbook(file_path)
    list = book.sheets()
    print(list)
    sheet_names = book.sheet_names()
    # print(sheet_names)
    # print(len(sheet_names[0]))
    try:
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            passwd='',
            db='arrangement',
            port=3306,
            charset='utf8'
        )
        cur = conn.cursor()
        query = 'insert into classroom(academicbuilding,classroomId,type,capacity,computer) values(%s, %s, %s, %s, %s);'
        for i in sheet_names:
            sheet_i = book.sheet_by_name(i)
            for r in range(1, sheet_i.nrows):
                a1 = sheet_i.cell(r, 0).value
                a2 = sheet_i.cell(r, 1).value
                a3 = sheet_i.cell(r, 2).value
                a4 = sheet_i.cell(r, 3).value
                a5 = sheet_i.cell(r, 4).value
                values = (a1, a2, a3, a4, a5)
                cur.execute(query, values)
        cur.close()
        conn.commit()
        conn.close()
        flash("导入成功")
    except Exception as e:
        flash(e)
    root.mainloop()
    return render_template('Input5.html', Id = Id)


@model.app.route('/aaa?<string:Id>', methods=['GET', 'POST'] )
def yjsc(Id):
    if request.method == 'POST':
        try:
           arrange.arrangment()
           flash("生成成功")
        except Exception as e:
            flash("生成失败，请检查输入")
    return render_template('yjsc.html', Id = Id)

@model.app.route('/sign?<string:Id>', methods=['GET', 'POST'] )
def sign(Id):
    if request.method == 'POST':
        data = model.exam.query.all()
        num = model.exam.query.count()
        path = r"C:\Users\17283\Desktop\考场座位视图"
        drawtest.mkdir(path)
        for i in range(0,num):
            type = data[i].type
            time = data[i].time
            course_code = data[i].course_code
            academicbuilding = data[i].academicbuilding
            classroomId = data[i].classroomId
            course_name = data[i].course_name
            drawtest.draw(type,time,course_code,academicbuilding,classroomId,course_name)
    return render_template('Sign.html', Id = Id)
@model.app.route('/add_stu?<string:Id>', methods=['GET', 'POST'] )
def add_stu(Id):
    if request.method == 'POST':
        id = request.form.get('Id')
        name = request.form.get('name')
        grade = request.form.get('grade')
        sclass = request.form.get('sclass')
        if not all([Id, name, grade, sclass]):
            flash('信息不完整')
        else:
            stu = model.student()
            stu.sId = id
            stu.sname = name
            stu.grade = grade
            stu.sclass = sclass
            try:
                model.db.session.add(stu)
                model.db.session.commit()
                flash('学生添加成功')
            except Exception as e:
                model.db.session.rollback()
                flash('学生已存在')
    return render_template('add_stu.html', Id = Id)

@model.app.route('/delete_stu?<string:Id>', methods=['GET', 'POST'] )
def delete_stu(Id):
    if request.method == 'POST':
        id = request.form.get('Id')
        if not all([Id]):
            flash('信息不完整')
        else:
            try:
                stu = model.student.query.filter(model.student.sId == id).first()
                model.db.session.delete(stu)
                model.db.session.commit()
                flash('学生删除成功')
            except Exception as e:
                model.db.session.rollback()
                flash('学生不存在或无法删除')
    return render_template('delete_stu.html', Id = Id)

@model.app.route('/search_stu?<string:Id>', methods=['GET', 'POST'] )
def search_stu(Id):
    num = model.student.query.count()
    data = model.student.query.all()
    list = []
    my_list = []
    my_list.append('学生Id')
    my_list.append('姓名')
    my_list.append('年级')
    my_list.append('班级')
    my_list.append('密码')
    my_list.append('邮箱')
    list.append(my_list)
    for i in range(0, num):
        sId = data[i].sId
        sname = data[i].sname
        grade = data[i].grade
        sclass = data[i].sclass
        spwd = data[i].spwd
        semail = data[i].semail
        my_list = []
        my_list.append(sId)
        my_list.append(sname)
        my_list.append(grade)
        my_list.append(sclass)
        my_list.append(spwd)
        my_list.append(semail)
        list.append(my_list)
    return render_template('search_stu.html', Id = Id, list = list)

@model.app.route('/add_tea?<string:Id>', methods=['GET', 'POST'] )
def add_tea(Id):
    if request.method == 'POST':
        id = request.form.get('Id')
        name = request.form.get('name')
        identity = request.form.get('identity')
        if not all([Id, name, identity]):
            flash('信息不完整')
        elif identity != 't' & identity != 'a':
            flash('填写正确的教师身份')
        else:
            tea = model.teacher()
            tea.tId = id
            tea.tname = name
            tea.identity = identity
            try:
                model.db.session.add(tea)
                model.db.session.commit()
                flash('教师添加成功')
            except Exception as e:
                model.db.session.rollback()
                flash('教师已存在')
    return render_template('add_tea.html', Id = Id)

@model.app.route('/delete_tea?<string:Id>', methods=['GET', 'POST'] )
def delete_tea(Id):
    if request.method == 'POST':
        id = request.form.get('Id')
        if not all([Id]):
            flash('信息不完整')
        else:
            try:
                tea = model.teacher.query.filter(model.teacher.tId == id).first()
                model.db.session.delete(tea)
                model.db.session.commit()
                flash('教师删除成功')
            except Exception as e:
                model.db.session.rollback()
                flash('教师不存在或无法删除')
    return render_template('delete_tea.html', Id = Id)

@model.app.route('/search_tea?<string:Id>', methods=['GET', 'POST'] )
def search_tea(Id):
    num = model.teacher.query.count()
    data = model.teacher.query.all()
    list = []
    my_list = []
    my_list.append('教师Id')
    my_list.append('姓名')
    my_list.append('密码')
    my_list.append('邮箱')
    my_list.append('身份')
    list.append(my_list)
    for i in range(0, num):
        tId = data[i].tId
        tname = data[i].tname
        tpwd = data[i].tpwd
        temail = data[i].temail
        if data[i].identity == 'a':
            identity = 'admin'
        elif data[i].identity == 't':
            identity = 'teacher'
        my_list = []
        my_list.append(tId)
        my_list.append(tname)
        my_list.append(tpwd)
        my_list.append(temail)
        my_list.append(identity)
        list.append(my_list)
    return render_template('search_tea.html', Id = Id, list = list)

@model.app.route('/add_course?<string:Id>', methods=['GET', 'POST'] )
def add_course(Id):
    if request.method == 'POST':
        id = request.form.get('code')
        name = request.form.get('name')
        teacher = request.form.get('teacher')
        istest = request.form.get('istest')
        iscomputer = request.form.get('iscomputer')
        if not all([id, name, teacher, istest, iscomputer]):
            flash('信息不完整')
        else :
            istest =  int(istest)
            iscomputer = int(iscomputer)
            if istest != 1 & istest != 0:
                flash('请正确输入是否需要考试, 是输入1, 否输入0')
            elif iscomputer != 1 & iscomputer != 0:
                flash('请正确输入是否需要机房, 是输入1, 否输入0')
            else:
                try:
                    cou = model.course()
                    cou.istest = int(istest)
                    cou.iscomputer = int(iscomputer)
                    cou.course_code = id
                    cou.course_name = name
                    cou.teachingteacher = teacher
                    model.db.session.add(cou)
                    model.db.session.commit()
                    flash('课程添加成功')
                except Exception as e:
                    model.db.session.rollback()
                    flash('请检查输入')
    return render_template('add_course.html', Id = Id)

@model.app.route('/delete_course?<string:Id>', methods=['GET', 'POST'] )
def delete_course(Id):
    if request.method == 'POST':
        id = request.form.get('Id')
        if not all([Id]):
            flash('信息不完整')
        else:
            try:
                cou = model.course.query.filter(model.course.course_code == id).first()
                model.db.session.delete(cou)
                model.db.session.commit()
                flash('课程删除成功')
            except Exception as e:
                model.db.session.rollback()
                flash('课程不存在或无法删除')
    return render_template('delete_course.html', Id = Id)

@model.app.route('/search_course?<string:Id>', methods=['GET', 'POST'] )
def search_course(Id):
    num = model.course.query.count()
    data = model.course.query.all()
    list = []
    my_list = []
    my_list.append('课程Id')
    my_list.append('课程名称')
    my_list.append('授课教师')
    my_list.append('是否考试')
    my_list.append('是否需要机房')
    my_list.append('考试时间')
    list.append(my_list)
    for i in range(0, num):
        course_code = data[i].course_code
        course_name = data[i].course_name
        teachingteacher = data[i].teachingteacher
        str_time = data[i].str_time
        if data[i].istest == 1:
            istest = '是'
        elif data[i].istest == 0:
            istest = '否'
        if data[i].iscomputer == 1:
            iscomputer = '是'
        elif data[i].iscomputer == 0:
            iscomputer = '否'
        my_list = []
        my_list.append(course_code)
        my_list.append(course_name)
        my_list.append(teachingteacher)
        my_list.append(istest)
        my_list.append(iscomputer)
        my_list.append(str_time)
        list.append(my_list)
    return render_template('search_course.html', Id = Id, list = list)


@model.app.route('/add_classroom?<string:Id>', methods=['GET', 'POST'] )
def add_classroom(Id):
    if request.method == 'POST':
        academicbuilding = request.form.get('academicbuilding')
        classroomId = request.form.get('classroomId')
        type = request.form.get('type')
        capacity = int(request.form.get('capacity'))
        computer = int(request.form.get('computer'))
        if not all([academicbuilding, classroomId, type, capacity, computer]):
            flash('信息不完整')
        elif capacity <= 0:
            flash('请正确输入教室容量')
        elif computer != 1 & computer != 0:
            flash('请正确输入是否为机房, 是输入1, 否输入0')
        else:
            try:
                cla = model.classroom()
                cla.academicbuilding = academicbuilding
                cla.classroomId = classroomId
                cla.type = type
                cla.capacity = capacity
                cla.computer = computer
                model.db.session.add(cla)
                model.db.session.commit()
                flash('教室插入成功')
            except Exception as e:
                model.db.session.rollback()
                flash('请检查输入')
    return render_template('add_classroom.html', Id = Id)

@model.app.route('/delete_classroom?<string:Id>', methods=['GET', 'POST'] )
def delete_classroom(Id):
    if request.method == 'POST':
        academicbuilding = request.form.get('academicbuilding')
        classroomId = request.form.get('classroomId')
        if not all([academicbuilding, classroomId]):
            flash('信息不完整')
        else:
            try:
                cla = model.classroom.query.filter(model.classroom.academicbuilding == academicbuilding, model.classroom.classroomId == classroomId).first()
                model.db.session.delete(cla)
                model.db.session.commit()
                flash('教室删除成功')
            except Exception as e:
                model.db.session.rollback()
                flash('教室不存在或无法删除')
    return render_template('delete_classroom.html', Id = Id)

@model.app.route('/search_classroom?<string:Id>', methods=['GET', 'POST'] )
def search_classroom(Id):
    num = model.classroom.query.count()
    data = model.classroom.query.all()
    list = []
    my_list = []
    my_list.append('教学楼')
    my_list.append('教室')
    my_list.append('类型')
    my_list.append('容量')
    my_list.append('是否为机房')
    list.append(my_list)
    for i in range(0, num):
        academicbuilding = data[i].academicbuilding
        classroomId = data[i].classroomId
        type = data[i].type
        capacity = data[i].capacity
        computer = data[i].computer
        my_list = []
        my_list.append(academicbuilding)
        my_list.append(classroomId)
        my_list.append(type)
        my_list.append(capacity)
        my_list.append(computer)
        list.append(my_list)
    return render_template('search_classroom.html', Id = Id, list = list)

@model.app.route('/search_study?<string:Id>', methods=['GET', 'POST'] )
def search_study(Id):
    num = model.study.query.count()
    data = model.study.query.all()
    list = []
    my_list = []
    my_list.append('课程Id')
    my_list.append('课程名称')
    my_list.append('学生Id')
    my_list.append('学生姓名')
    my_list.append('年级')
    my_list.append('班级')
    list.append(my_list)
    for i in range(0, num):
        course_code = data[i].course_code
        course_name = data[i].course_name
        sId = data[i].sId
        sname = data[i].sname
        grade = data[i].grade
        sclass = data[i].sclass
        my_list = []
        my_list.append(course_code)
        my_list.append(course_name)
        my_list.append(sId)
        my_list.append(sname)
        my_list.append(grade)
        my_list.append(sclass)
        list.append(my_list)
    return render_template('search_study.html', Id = Id, list = list)

@model.app.route('/add_study?<string:Id>', methods=['GET', 'POST'] )
def add_study(Id):
    if request.method == 'POST':
        sid = request.form.get('sId')
        cid = request.form.get('cId')
        if not all([sid, cid]):
            flash('信息不完整')
        else:
            data1 = model.student.query.filter(model.student.sId == sid).first()
            data2 = model.course.query.filter(model.course.course_code == cid).first()
            if data1 == None:
                flash('学生不存在')
            elif data2 == None:
                flash('课程不存在')
            else:
                try:
                    stu = model.study()
                    stu.sId = sid
                    stu.course_code = cid
                    stu.sname = data1.sname
                    stu.grade = data1.grade
                    stu.sclass = data1.sclass
                    stu.semail = data1.semail
                    stu.course_name = data2.course_name
                    model.db.session.add(stu)
                    model.db.session.commit()
                    flash('选课信息添加成功')
                except Exception as e:
                    model.db.session.rollback()
                    flash('请检查输入')
    return render_template('add_study.html', Id = Id)

@model.app.route('/delete_study?<string:Id>', methods=['GET', 'POST'] )
def delete_study(Id):
    if request.method == 'POST':
        sid = request.form.get('sId')
        cid = request.form.get('cId')
        if not all([sid, cid]):
            flash('信息不完整')
        else:
            data1 = model.student.query.filter(model.student.sId == sid).first()
            data2 = model.course.query.filter(model.course.course_code == cid).first()
            if data1 == None:
                flash('学生不存在')
            elif data2 == None:
                flash('课程不存在')
            else:
                try:
                    stu = model.study.query.filter(model.study.sId == sid, model.study.course_code == cid).first()
                    model.db.session.delete(stu)
                    model.db.session.commit()
                    flash('选课信息删除成功')
                except Exception as e:
                    model.db.session.rollback()
                    flash('请检查输入')
    return render_template('delete_study.html', Id=Id)


if __name__ == '__main__':
    # arrange.arrangment()
    model.app.run(debug=True ,use_reloader=False)