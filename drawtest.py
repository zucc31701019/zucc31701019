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

mpl.rcParams["font.sans-serif"]=["SimHei"]
mpl.rcParams["axes.unicode_minus"]=False

def del_dir(dir_path):
    import shutil
    shutil.rmtree(dir_path)

def mkdir(path):
    # del_dir(path)
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if isExists:
        del_dir(path)
    os.makedirs(path)



def draw(type, time, course_id, ac , class_id,course_name):
    if type == 1:
        plt.figure(figsize=(40, 30))
        plt.suptitle(time + " " + ac + class_id + " " + course_name, ha="center")
        plt.subplot2grid((40, 4), (1, 0), colspan=4)
        plt.text(0.5, 0.5, "讲台", ha="center", fontsize=15)
        cnt = 1
        plt.subplot2grid((40, 4), (17, 0), colspan=4,rowspan=2)
        plt.text(0.5, 0.5, "走廊", ha="center", fontsize=15)
        for col in range(0, 4):
            for row in range(0, 24):
                all_test = model.test.query.filter(
                    and_(model.test.course_code == course_id, class_id == model.test.classroomId,
                         ac == model.test.academicbuilding, model.test.seat == cnt)).all()
                if int(row % 24) <= 13:

                    if len(all_test) == 0:
                       plt.subplot2grid((40, 4), (row + 2, col))
                       plt.text(0.5, 0.5, str(cnt), ha="center", fontsize=15)
                    else:
                        plt.subplot2grid((40, 4), (row + 2, col),fc = 'yellow')
                        plt.text(0.5, 0.5, str(str(cnt) +" "+all_test[0].sname), ha="center", fontsize=15)
                    cnt = cnt + 1
                elif int(row % 24) >= 14:

                    if len(all_test) == 0:
                        plt.subplot2grid((40, 4), (row + 5, col))
                        plt.text(0.5, 0.5, str(cnt), ha="center", fontsize=15)
                    else:
                        plt.subplot2grid((40, 4), (row + 5, col),fc = 'yellow')
                        plt.text(0.5, 0.5, str(str(cnt) + " " + all_test[0].sname), ha="center", fontsize=15)
                    cnt = cnt + 1
        plt.subplot2grid((40, 4), (17, 0), colspan=4, rowspan=2)
        plt.text(0.5, 0.5, "走廊", ha="center", fontsize=15)
        tt = ac + class_id + " " + course_name
        path = 'C:\\Users\\17283\\Desktop\\考场座位视图\\' + tt + '.png'
        plt.savefig(path)
        # plt.show()

    if type == 2:
        plt.figure(figsize=(40, 30))
        plt.suptitle(time + " " + ac + class_id + " " + course_name, ha="center")
        plt.subplot2grid((40, 30), (1, 0), colspan=16)
        plt.text(0.5, 0.5, "讲台", ha="center", fontsize=15)
        cnt = 1

        for col in range(0, 12):
            for row in range(0, 7):
                all_test = model.test.query.filter(
                    and_(model.test.course_code == course_id, class_id == model.test.classroomId,
                         ac == model.test.academicbuilding, model.test.seat == cnt)).all()

                if col < 3:

                    if len(all_test) == 0:
                        plt.subplot2grid((40, 30), (row + 2, col))
                        plt.text(0.5, 0.5, str(cnt), ha="center", fontsize=15)
                    else:
                        plt.subplot2grid((40, 30), (row + 2, col),fc = 'yellow')
                        plt.text(0.5, 0.5, str(str(cnt) + " " + all_test[0].sname), ha="center", fontsize=15)
                    cnt = cnt + 1

                elif col >= 3 and col < 9:

                    if len(all_test) == 0:
                        plt.subplot2grid((40, 30), (row + 2, col + 2))
                        plt.text(0.5, 0.5, str(cnt), ha="center", fontsize=15)
                    else:
                        plt.subplot2grid((40, 30), (row + 2, col + 2),fc = 'yellow')
                        plt.text(0.5, 0.5, str(str(cnt) + " " + all_test[0].sname), ha="center", fontsize=15)
                    cnt = cnt + 1
                else:

                    if len(all_test) == 0:
                        plt.subplot2grid((40, 30), (row + 2, col + 4))
                        plt.text(0.5, 0.5, str(cnt), ha="center", fontsize=15)
                    else:
                        plt.subplot2grid((40, 30), (row + 2, col + 4),fc ='yellow')
                        plt.text(0.5, 0.5, str(str(cnt) + " " + all_test[0].sname), ha="center", fontsize=15)
                    cnt = cnt + 1

        plt.subplot2grid((40, 30), (2, 3) , colspan=2, rowspan=7)
        plt.text(0.5, 0.5, "走廊", ha="center", fontsize=15)
        plt.subplot2grid((40, 30), (2, 11), colspan=2, rowspan=7)
        plt.text(0.5, 0.5, "走廊", ha="center", fontsize=15)
        tt =   ac + class_id + " " + course_name
        path = 'C:\\Users\\17283\\Desktop\\考场座位视图\\' + tt + '.png'
        plt.savefig(path)
        # plt.show()

    if type == 3:
        plt.figure(figsize=(40, 30))

        plt.suptitle(time + " " + ac + class_id + " " + course_name, ha="center")
        plt.subplot2grid((40, 30), (1, 0), colspan=15)
        plt.text(0.5, 0.5, "讲台", ha="center", fontsize=15)
        cnt = 1

        for col in range(0, 11):
            for row in range(0, 12):
                all_test = model.test.query.filter(
                    and_(model.test.course_code == course_id, class_id == model.test.classroomId,
                         ac == model.test.academicbuilding, model.test.seat == cnt)).all()

                if col < 3:
                    if row < 6:
                        if len(all_test) == 0:
                            plt.subplot2grid((40, 30), (row + 2, col))
                            plt.text(0.5, 0.5, str(cnt), ha="center", fontsize=15)
                        else:
                            plt.subplot2grid((40, 30), (row + 2, col), fc='yellow')
                            plt.text(0.5, 0.5, str(str(cnt) + " " + all_test[0].sname), ha="center", fontsize=15)
                        cnt = cnt + 1
                    else:
                        if len(all_test) == 0:
                            plt.subplot2grid((40, 30), (row + 3, col))
                            plt.text(0.5, 0.5, str(cnt), ha="center", fontsize=15)
                        else:
                            plt.subplot2grid((40, 30), (row + 3, col), fc='yellow')
                            plt.text(0.5, 0.5, str(str(cnt) + " " + all_test[0].sname), ha="center", fontsize=15)
                        cnt = cnt + 1

                elif col >= 3 and col < 8:
                    if row < 6:
                        if len(all_test) == 0:
                            plt.subplot2grid((40, 30), (row + 2, col + 2))
                            plt.text(0.5, 0.5, str(cnt), ha="center", fontsize=15)
                        else:
                            plt.subplot2grid((40, 30), (row + 2, col + 2), fc ='yellow')
                            plt.text(0.5, 0.5, str(str(cnt) + " " + all_test[0].sname), ha="center", fontsize=15)
                        cnt = cnt + 1
                    else:
                        if len(all_test) == 0:
                            plt.subplot2grid((40, 30), (row + 3, col + 2))
                            plt.text(0.5, 0.5, str(cnt), ha="center", fontsize=15)
                        else:
                            plt.subplot2grid((40, 30), (row + 3, col + 2), fc='yellow')
                            plt.text(0.5, 0.5, str(str(cnt) + " " + all_test[0].sname), ha="center", fontsize=15)
                        cnt = cnt + 1

                elif col >=8 and col <10:
                    if row < 6:
                        if len(all_test) == 0:
                            plt.subplot2grid((40, 30), (row + 2, col + 4))
                            plt.text(0.5, 0.5, str(cnt), ha="center", fontsize=15)
                        else:
                            plt.subplot2grid((40, 30), (row + 2, col + 4), fc ='yellow')
                            plt.text(0.5, 0.5, str(str(cnt) + " " + all_test[0].sname), ha="center", fontsize=15)
                        cnt = cnt + 1
                    else:
                        if len(all_test) == 0:
                            plt.subplot2grid((40, 30), (row + 3, col + 4))
                            plt.text(0.5, 0.5, str(cnt), ha="center", fontsize=15)
                        else:
                            plt.subplot2grid((40, 30), (row + 3, col + 4), fc='yellow')
                            plt.text(0.5, 0.5, str(str(cnt) + " " + all_test[0].sname), ha="center", fontsize=15)
                        cnt = cnt + 1
                elif col == 10:
                    if row < 6 and row != 1 and row != 5:
                        if len(all_test) == 0:
                            plt.subplot2grid((40, 30), (row + 2, col + 4))
                            plt.text(0.5, 0.5, str(cnt), ha="center", fontsize=15)
                        else:
                            plt.subplot2grid((40, 30), (row + 2, col + 4), fc='yellow')
                            plt.text(0.5, 0.5, str(str(cnt) + " " + all_test[0].sname), ha="center", fontsize=15)
                        cnt = cnt + 1
                    elif row >= 6 and row != 7:
                        if len(all_test) == 0:
                            plt.subplot2grid((40, 30), (row + 3, col + 4))
                            plt.text(0.5, 0.5, str(cnt), ha="center", fontsize=15)
                        else:
                            plt.subplot2grid((40, 30), (row + 3, col + 4), fc='yellow')
                            plt.text(0.5, 0.5, str(str(cnt) + " " + all_test[0].sname), ha="center", fontsize=15)
                        cnt = cnt + 1


        plt.subplot2grid((40, 30), (2, 3), colspan=2, rowspan=6)
        plt.text(0.5, 0.5, "走廊", ha="center", fontsize=15)

        plt.subplot2grid((40, 30), (2, 10), colspan=2, rowspan=6)
        plt.text(0.5, 0.5, "走廊", ha="center", fontsize=15)

        plt.subplot2grid((40, 30), (9, 3), colspan=2, rowspan=6)
        plt.text(0.5, 0.5, "走廊", ha="center", fontsize=15)

        plt.subplot2grid((40, 30), (9, 10), colspan=2, rowspan=6)
        plt.text(0.5, 0.5, "走廊", ha="center", fontsize=15)

        plt.subplot2grid((40, 30), (8, 0), colspan=15, rowspan=1)
        plt.text(0.5, 0.5, "走廊", ha="center", fontsize=15)
        plt.subplot2grid((40, 30), (3, 14), colspan=1, rowspan=1)
        plt.subplot2grid((40, 30), (7, 14), colspan=1, rowspan=1)
        plt.subplot2grid((40, 30), (10, 14), colspan=1, rowspan=1)
        tt =   ac + class_id + " " + course_name
        path = 'C:\\Users\\17283\\Desktop\\考场座位视图\\' + tt+'.png'
        plt.savefig(path)
        # plt.show()

    if type == 4:
            plt.figure(figsize=(40, 30))
            plt.suptitle(time + " " + ac + class_id + " " + course_name, ha="center")
            plt.subplot2grid((40, 30), (1, 0), colspan=19)
            plt.text(0.5, 0.5, "讲台", ha="center", fontsize=15)
            cnt = 1

            for col in range(0, 15):
                for row in range(0, 13):

                    all_test = model.test.query.filter(
                        and_(model.test.course_code == course_id, class_id == model.test.classroomId,
                             ac == model.test.academicbuilding, model.test.seat == cnt)).all()

                    if col < 3:

                        if len(all_test) == 0:
                            plt.subplot2grid((40, 30), (row + 2, col))
                            plt.text(0.5, 0.5, str(cnt), ha="center", fontsize=15)
                        else:
                            plt.subplot2grid((40, 30), (row + 2, col),fc = 'yellow')
                            plt.text(0.5, 0.5, str(str(cnt) + " " + all_test[0].sname), ha="center", fontsize=15 )
                        cnt = cnt + 1

                    elif col == 3:
                         if row >= 8:

                             if len(all_test) == 0:
                                 plt.subplot2grid((40, 30), (row + 2, col))
                                 plt.text(0.5, 0.5, str(cnt), ha="center", fontsize=15)
                             else:
                                 plt.subplot2grid((40, 30), (row + 2, col), fc = 'yellow')
                                 plt.text(0.5, 0.5, str(str(cnt) + " " + all_test[0].sname), ha="center", fontsize=15)
                             cnt = cnt + 1

                    elif col > 3 and col < 11:

                        if len(all_test) == 0:
                            plt.subplot2grid((40, 30), (row + 2, col + 2))
                            plt.text(0.5, 0.5, str(cnt), ha="center", fontsize=15)
                        else:
                            plt.subplot2grid((40, 30), (row + 2, col + 2),fc ='yellow')
                            plt.text(0.5, 0.5, str(str(cnt) + " " + all_test[0].sname), ha="center", fontsize=15)
                        cnt = cnt + 1

                    elif col < 14 and col >=11:

                        if len(all_test) == 0:
                            plt.subplot2grid((40, 30), (row + 2, col + 4))
                            plt.text(0.5, 0.5, str(cnt), ha="center", fontsize=15)
                        else:
                            plt.subplot2grid((40, 30), (row + 2, col + 4),fc = 'yellow')
                            plt.text(0.5, 0.5, str(str(cnt) + " " + all_test[0].sname), ha="center", fontsize=15)
                        cnt = cnt + 1

                    elif col == 14:
                        if row != 6 and row != 7:
                            if len(all_test) == 0:
                                if row < 6:
                                    plt.subplot2grid((40, 30), (row + 2, col + 4))
                                else:
                                    plt.subplot2grid((40, 30), (row + 2, col + 4))
                                plt.text(0.5, 0.5, str(cnt), ha="center", fontsize=15)
                            else:
                                if row < 6:
                                    plt.subplot2grid((40, 30), (row + 2, col + 4), fc='yellow')
                                else:
                                    plt.subplot2grid((40, 30), (row + 2, col + 4), fc='yellow')
                                plt.text(0.5, 0.5, str(str(cnt) + " " + all_test[0].sname), ha="center", fontsize=15)
                            cnt = cnt + 1

            plt.subplot2grid((40, 30), (2, 3), colspan=1, rowspan=8)
            plt.text(0.5, 0.5, "走廊", ha="center", fontsize=15)
            plt.subplot2grid((40, 30), (2, 4), colspan=2, rowspan=13)
            plt.text(0.5, 0.5, "走廊", ha="center", fontsize=15)
            plt.subplot2grid((40, 30), (2, 13), colspan=2, rowspan=13)
            plt.text(0.5, 0.5, "走廊", ha="center", fontsize=15)
            plt.subplot2grid((40, 30), (8, 18), colspan=1, rowspan=2)
            plt.text(0.5, 0.5, "走廊", ha="center", fontsize=15)
            tt =  ac + class_id + " " + course_name
            path = 'C:\\Users\\17283\\Desktop\\考场座位视图\\' + tt + '.png'
            plt.savefig(path)
            # plt.show()

# if __name__ == '__main__':
#     # 2017年1月1日 8：10 - 10：10
#     # 2019年1月5日 14：00 - 16：00
#     # 2020年1月5日 14: 00 - 16: 00
#     time = "2020年1月5日 14: 00 - 16: 00"
#     course_id = "IS112"
#     ac = "理四"
#     class_id = "224"
#     course_name = "软件工程基础"
#     path = r"C:\Users\17283\Desktop\考场座位视图"
#     mkdir(path)
#     draw(1,time, course_id, ac , class_id,course_name)

