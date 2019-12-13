from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/arrangement'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY']='123'
db = SQLAlchemy(app)


class admin(db.Model):
    __tablename__ = 'admin'
    aId = db.Column(db.String(255), primary_key=True)
    aname = db.Column(db.String(255))
    aemail = db.Column(db.String(255))
    aaccount = db.Column(db.String(255))
    apwd = db.Column(db.String(255))

class classroom(db.Model):
    __tablename__ = 'classroom'
    academicbuilding = db.Column(db.String(255), primary_key=True)
    classroomId = db.Column(db.String(255), primary_key=True)
    type = db.Column(db.String(255))
    capacity = db.Column(db.Integer)
    computer = db.Column(db.Boolean)

class course(db.Model):
    __tablename__ = 'course'
    course_code = db.Column(db.String(255), primary_key=True)
    course_name = db.Column(db.String(255))
    teachingteacher = db.Column(db.String(255))
    istest = db.Column(db.Integer)
    iscomputer = db.Column(db.Integer)
    time = db.Column(db.Integer)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    teacher_id = db.Column(db.String(255))
    str_time = db.Column(db.String(255))

class exam(db.Model):
    __tablename__ = 'exam'
    course_code = db.Column(db.String(255), primary_key=True)
    academicbuilding = db.Column(db.String(255), primary_key=True)
    classroomId = db.Column(db.String(255), primary_key=True)
    time = db.Column(db.String(255))
    course_name = db.Column(db.String(255))
    type = db.Column(db.Integer)

class invigilate(db.Model):
    __tablename__ = 'invigilate'
    tId = db.Column(db.String(255), primary_key=True)
    academicbuilding = db.Column(db.String(255), primary_key=True)
    classroomId = db.Column(db.String(255), primary_key=True)
    time = db.Column(db.String(255))
    tname = db.Column(db.String(255))
    course_name = db.Column(db.String(255))
    course_code = db.Column(db.String(255))
    isstop = db.Column(db.Integer)

class student(db.Model):
    __tablename__ = 'student'
    sId = db.Column(db.String(255), primary_key=True)
    sname = db.Column(db.String(255))
    sclass = db.Column(db.String(255))
    grade = db.Column(db.String(255))
    saccount = db.Column(db.String(255))
    spwd = db.Column(db.String(255))
    scheck = db.Column(db.Integer)
    semail = db.Column(db.String(255))


class study(db.Model):
    __tablename__ = 'study'
    sId = db.Column(db.String(255), primary_key=True)
    course_code = db.Column(db.String(255), primary_key=True)
    sname = db.Column(db.String(255))
    semail = db.Column(db.String(255))
    grade = db.Column(db.String(255))
    sclass = db.Column(db.String(255))
    course_name = db.Column(db.String(255))

class teach(db.Model):
    __tablename__ = 'teach'
    tId = db.Column(db.String(255), primary_key=True)
    course_code = db.Column(db.String(255), primary_key=True)
    tname = db.Column(db.String(255))
    temail = db.Column(db.String(255))
    course_name = db.Column(db.String(255))

class teacher(db.Model):
    __tablename__ = 'teacher'
    tId = db.Column(db.String(255), primary_key=True)
    tname = db.Column(db.String(255))
    temail = db.Column(db.String(255))
    taccount = db.Column(db.String(255))
    tpwd = db.Column(db.String(255))
    tcheck = db.Column(db.Integer)
    identity = db.Column(db.String(255))


class test(db.Model):
    __tablename__ = 'test'
    sId = db.Column(db.String(255), primary_key=True)
    academicbuilding = db.Column(db.String(255), primary_key=True)
    classroomId = db.Column(db.String(255), primary_key=True)
    time = db.Column(db.String(255))
    seat = db.Column(db.Integer)
    sname = db.Column(db.String(255))
    course_name = db.Column(db.String(255))
    course_code = db.Column(db.String(255),primary_key=True)



