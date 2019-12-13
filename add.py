import matplotlib.pyplot as plt
import matplotlib as mpl

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
import model
from sqlalchemy import and_
from queue import Queue,LifoQueue,PriorityQueue
import os

def add_stu(id,name,grade,sclass):
    if id == ""or name == "" or grade == "" or sclass == "":
        return "有空的项，请检查输入"
    stu = model.student()
    stu.sId = id
    stu.sname = name
    stu.grade = grade
    stu.sclass = sclass
    try:
        model.db.session.add(stu)
        model.db.session.commit()
        return "学生添加成功!"
    except Exception as e:
        model.db.session.rollback()
        return "学生已存在"

def add_tea(id,name,identity):
    if id == ""or name == ""or identity == "":
        return "有空的项，请检查输入"
    if identity != "a" and identity != "t":
        return "请正确输入老师的级别，管理员请输入'a',普通老师请输入't'"
    tea = model.teacher()
    tea.tId = id
    tea.tname = name
    tea.identity = identity
    try:
        model.db.session.add(tea)
        model.db.session.commit()
        return "学生添加成功!"
    except Exception as e:
        model.db.session.rollback()
        return "老师已存在"

def add_classroom(academicbuilding,classroomId,type,capacity,computer):
    if academicbuilding == ""or classroomId == ""or type== ""or capacity == "" or computer == "":
        return "有空的项，请检查输入"
    if type >= 4 or type <= 0 :
        return "请正确选择教室类型，1-4"
    if computer != 1 and computer != 0:
        return "请正确输入是否需要机房，是输入1，否输入0"
    try:
        cla = model.classroom()
        cla.classroomId = classroomId
        cla.academicbuilding = academicbuilding
        cla.capacity = capacity
        cla.type = type
        cla.computer = computer
        model.db.session.add(cla)
        model.db.session.commit()
        return "教室插入成功"
    except Exception as e:
        model.db.session.rollback()
        return "请检查自己的输入"

def add_course(id,name,teacher,iscomputer):
    if id == "" or teacher == "" or name == "" or iscomputer == "":
        return "有空的项，请检查输入"
    if iscomputer != 1 and iscomputer != 0:
        return "请正确输入是否需要机房，是输入1，否输入0"
    try:
       cou = model.course()
       cou.iscomputer =iscomputer
       cou.course_code = id
       cou.course_name = name
       cou.teachingteacher = teacher
       model.db.session.add(cou)
       model.db.session.commit()
       return "课程添加成功!"
    except Exception as e:
        model.db.session.rollback()
        return "请检查自己的输入"

if __name__ == '__main__':
     add_course("0000","wewrw","t","1")
  
