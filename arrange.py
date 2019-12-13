from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
import model
from sqlalchemy import and_
from queue import Queue,LifoQueue,PriorityQueue

def check(tea, course):
    id = tea.tId
    l = len(course)
    for i in range(0, l):
        if id == course[i].teacher_id:
            return False
    return True

def arrangment():
    # 主要可用
    q1 = Queue(maxsize=0)
    # 这次不可用
    q2 = Queue(maxsize=0)
    # 上次遗留
    q3 = Queue(maxsize=0)

    all_teas = model.teacher.query.filter().all()
    tt = len(all_teas)
    for i in range(0, tt):
        q1.put(all_teas[i])

    miny = 9999
    minm = 13
    mind = 50
    maxy = 0
    maxm = 0
    maxd = 0
    all_results = model.course.query.filter().all()
    num = len(all_results)
    for i in range(0, num):
        if miny > all_results[i].year:
            miny = all_results[i].year
            minm = all_results[i].month
            mind = all_results[i].day
        elif miny == all_results[i].year and minm > all_results[i].month:
            miny = all_results[i].year
            minm = all_results[i].month
            mind = all_results[i].day
        elif miny == all_results[i].year and minm == all_results[i].month and mind > all_results[i].day:
            miny = all_results[i].year
            minm = all_results[i].month
            mind = all_results[i].day


    for i in range(0, num):
            if maxy < all_results[i].year:
                maxy = all_results[i].year
                maxm = all_results[i].month
                maxd = all_results[i].day
            elif maxy == all_results[i].year and maxm < all_results[i].month:
                maxy = all_results[i].year
                maxm = all_results[i].month
                maxd = all_results[i].day
            elif maxy == all_results[i].year and maxm == all_results[i].month and maxd < all_results[i].day:
                maxy = all_results[i].year
                maxm = all_results[i].month
                maxd = all_results[i].day

            print(str(maxy)+" "+str(maxm)+" "+str(maxd)+" "+str(miny) +" "+str(minm)+" "+str(mind))


    for year in range(miny, maxy+1):
        for month in range(minm, maxm+1):
            for day in range(mind, maxd+1):
                for time in range(1, 5):
                    while q2.empty() == False:
                        tea = q2.get()
                        q3.put(tea)
                    ctt2 = 0
                    courses = model.course.query.filter(and_(model.course.year == year, model.course.month == month, model.course.day == day, model.course.time == time)).all()
                    classrooms = model.classroom.query.filter().all()
                    classrooms1 = model.classroom.query.filter(model.classroom.type == 1).all()
                    classrooms2 = model.classroom.query.filter(model.classroom.type == 2).all()
                    classrooms3 = model.classroom.query.filter(model.classroom.type == 3).all()

                    co1 = len(classrooms1)
                    co2 = len(classrooms2)
                    co3 = len(classrooms3)
                    #现在分配到第几间理四五楼的教室
                    now2 = 0
                    #现在分配到的第几间南校的type3的教室
                    now3 = 0
                    coo = len(courses)
                    p108 = 0
                    #开始遍历安排这个时间段的课程
                    for i in range(0, coo):
                        nn = 0
                        tt = courses[i].iscomputer
                        print(courses[i].course_name)
                        print(courses[i].iscomputer)
                        cnt = 0 #安排到的学生次序
                        #这门课的学生总计
                        studys = model.study.query.filter(model.study.course_code == courses[i].course_code).all()
                        #这门课的学生人数
                        nn = len(studys)
                        print(nn)
                        if nn == 0:
                            continue
                        # print(nn)
                        pa = [0] * (co1 + 1)

                        if tt == 1:
                           #预处理安排的教室数量
                           if nn% 48 == 0:
                              classnum = nn/48
                           else:
                              classnum = nn/48 + 1
                           #现在安排完成的教室数量
                           now = 0
                           #需要多一个人的教室数量
                           ful = nn % classnum
                           #每个教室的基础人数
                           pnum = int(nn / classnum)
                           # pa = [0] * (co1 + 1)
                           print(co1)
                           for j in range(0, co1):
                               pa[j] = 0

                           for j in range(0, co1):
                                if now >= classnum:
                                    break
                                if pa[j] == 0:
                                    if now < ful:
                                       ne = int(96 / (pnum + 1))
                                       up = int((pnum + 1) / 4) + 1
                                       ffp = int(pnum + 1) % 4
                                       ftt = 0
                                       ppp = 0
                                       for nnn in range(cnt, int(cnt + pnum + 1)):
                                         if nnn >= nn:
                                             break
                                         #保证每一排的过道第一个位置有人坐
                                         if ftt == up:
                                             seat = (int(seat / 24) + 1) * 24
                                             ftt = 1
                                             ppp = ppp + 1
                                             if ppp == ffp:
                                                 up = up -1

                                         elif nnn == cnt:
                                           seat = 0
                                           ppp = 0
                                           ftt = 1
                                           if ppp == ffp:
                                               up = up - 1
                                         elif int(seat/24) != int((seat + ne)/24) or ftt == up:
                                            seat = (int(seat / 24) + 1)*24
                                            ftt = 1
                                            ppp = ppp + 1
                                            if ppp == ffp:
                                                up = up - 1

                                         elif int(int(seat + ne) % 24) >= 14 and int(seat % 24) < 14:
                                             seat = (int(seat / 24))*24 + 14
                                             ftt = ftt + 1

                                         else:
                                            seat = seat + ne
                                            ftt = ftt + 1

                                         #存入数据库
                                         test = model.test()
                                         test.sId = studys[nnn].sId
                                         test.academicbuilding = classrooms1[j].academicbuilding
                                         test.classroomId = classrooms1[j].classroomId
                                         test.time = courses[i].str_time
                                         test.seat = seat + 1
                                         test.sname = studys[nnn].sname
                                         test.course_name = courses[i].course_name
                                         test.course_code = courses[i].course_code

                                         print(test.sId)

                                         model.db.session.add(test)
                                         model.db.session.commit()
                                       pa[j] = 1
                                       cnt = cnt +pnum +1
                                       ful = ful +1
                                       now = now + 1

                                       for ppt in range(0, 2):
                                           if q3.empty():
                                              tea = q1.get()
                                           else:
                                              tea = q3.get()
                                           while check(tea, courses) == False:
                                               q2.put(tea)
                                               if q3.empty():
                                                   tea = q1.get()
                                               else:
                                                   tea = q3.get()

                                           jian = model.invigilate()
                                           jian.course_code = courses[i].course_code
                                           jian.course_name = courses[i].course_name
                                           jian.academicbuilding = classrooms1[j].academicbuilding
                                           jian.classroomId = classrooms1[j].classroomId
                                           jian.time = courses[i].str_time
                                           jian.isstop = 1
                                           jian.tId = tea.tId
                                           jian.tname =tea.tname
                                           q1.put(tea)
                                           model.db.session.add(jian)
                                           model.db.session.commit()

                                       jian = model.invigilate()
                                       jian.course_code = courses[i].course_code
                                       jian.course_name = courses[i].course_name
                                       jian.academicbuilding = classrooms1[j].academicbuilding
                                       jian.classroomId = classrooms1[j].classroomId
                                       jian.time = courses[i].str_time
                                       jian.isstop = 0
                                       jian.tId = courses[i].teacher_id
                                       jian.tname = courses[i].teachingteacher
                                       model.db.session.add(jian)
                                       model.db.session.commit()

                                       exam = model.exam()
                                       exam.academicbuilding = classrooms1[j].academicbuilding
                                       exam.classroomId = classrooms1[j].classroomId
                                       exam.course_name = courses[i].course_name
                                       exam.time = courses[i].str_time
                                       exam.course_code = courses[i].course_code
                                       exam.type = 1
                                       model.db.session.add(exam)
                                       model.db.session.commit()

                                    else:
                                        ne = int(96 / pnum)
                                        up = int(pnum / 4) + 1
                                        ftt = 0
                                        ffp = int(pnum % 4)
                                        ppp = 0
                                        for nnn in range(cnt, int(cnt + pnum)):
                                            if nnn >= nn:
                                                break
                                            # 保证每一排的第一个位置有人坐
                                            if ftt == up:
                                                seat = (int(seat / 24) + 1) * 24
                                                ftt = 1
                                                ppp = ppp + 1
                                                if ppp == ffp:
                                                    up = up - 1

                                            elif nnn == cnt:
                                                seat = 0
                                                ftt = 1
                                                if ppp == ffp:
                                                    up = up - 1

                                            elif int(seat / 24) != int((seat + ne) / 24) or ftt == up:
                                                seat = (seat / 24 + 1) * 24
                                                ftt = 1
                                                ppp = ppp + 1
                                                if ppp == ffp:
                                                    ppp = ppp - 1

                                            elif int(int(seat + ne) % 24) >= 14 and int(seat % 24) < 14:
                                                seat = int(seat / 24) * 24 + 14
                                                ftt = ftt + 1

                                            else:
                                                seat = seat + ne
                                                ftt = ftt + 1

                                            test = model.test()
                                            test.sId = studys[nnn].sId
                                            test.academicbuilding = classrooms1[j].academicbuilding
                                            test.classroomId = classrooms1[j].classroomId
                                            test.time = courses[i].str_time
                                            test.seat = seat + 1
                                            test.sname = studys[nnn].sname
                                            test.course_name = courses[i].course_name
                                            test.course_code = courses[i].course_code

                                            print(test.sId)

                                            model.db.session.add(test)
                                            model.db.session.commit()

                                        for ppt in range(0, 2):
                                            if q3.empty():
                                                tea = q1.get()
                                            else:
                                                tea = q3.get()
                                            while check(tea, courses) == False:
                                                q2.put(tea)
                                                if q3.empty():
                                                    tea = q1.get()
                                                else:
                                                    tea = q3.get()

                                            jian = model.invigilate()
                                            jian.course_code = courses[i].course_code
                                            jian.course_name = courses[i].course_name
                                            jian.academicbuilding = classrooms1[j].academicbuilding
                                            jian.classroomId = classrooms1[j].classroomId
                                            jian.time = courses[i].str_time
                                            jian.isstop = 1
                                            jian.tId = tea.tId
                                            jian.tname = tea.tname
                                            q1.put(tea)
                                            model.db.session.add(jian)
                                            model.db.session.commit()

                                        jian = model.invigilate()
                                        jian.course_code = courses[i].course_code
                                        jian.course_name = courses[i].course_name
                                        jian.academicbuilding = classrooms1[j].academicbuilding
                                        jian.classroomId = classrooms1[j].classroomId
                                        jian.time = courses[i].str_time
                                        jian.isstop = 0
                                        jian.tId = courses[i].teacher_id
                                        jian.tname = courses[i].teachingteacher
                                        model.db.session.add(jian)
                                        model.db.session.commit()
                                        cnt = cnt + pnum

                                        exam = model.exam()
                                        exam.academicbuilding = classrooms1[j].academicbuilding
                                        exam.classroomId = classrooms1[j].classroomId
                                        exam.course_name = courses[i].course_name
                                        exam.time = courses[i].str_time
                                        exam.course_code = courses[i].course_code
                                        exam.type = 1
                                        model.db.session.add(exam)
                                        model.db.session.commit()
                                pa[j] = 1
                                now = now +1
                        else:
                            #排在理四108
                            if nn >= 82 and nn <= 115 and p108 == 0:
                                pnum = nn
                                p108 = 1
                                # 当前排到第几排
                                ppp = 0
                                seat = 0
                                ful = int(pnum % 8)
                                rn = 0
                                row_max_num = int(pnum / 8) + 1
                                for nnn in range(0, pnum):
                                    if nnn == nn:
                                        break
                                    if nnn == 0:
                                        seat = 0
                                        rn = 1
                                        if ppp == ful:
                                            row_max_num = row_max_num - 1
                                    elif rn == row_max_num and ppp != 7:
                                        seat = (int(seat / 13) + 2) * 13
                                        if seat == 52:
                                            seat = 39
                                        if seat == 143:
                                            seat = 130
                                        ppp = ppp + 1
                                        if ppp == ful:
                                            row_max_num = row_max_num - 1
                                        # if ppp == 6:
                                        #     row_max_num = row_max_num + 1
                                        rn = 1
                                    else:
                                        seat = seat + 1
                                        rn = rn + 1

                                    test = model.test()
                                    test.sId = studys[nnn].sId
                                    test.academicbuilding = str("理四")
                                    test.classroomId = str("108")
                                    test.time = courses[i].str_time
                                    test.seat = seat + 1
                                    if test.seat >= 40:
                                        test.seat = test.seat + 5
                                    test.sname = studys[nnn].sname
                                    test.course_name = courses[i].course_name
                                    test.course_code = courses[i].course_code
                                    print(test.sId)
                                    model.db.session.add(test)
                                    model.db.session.commit()
                                for ppt in range(0, 2):
                                    if q3.empty():
                                        tea = q1.get()
                                    else:
                                        tea = q3.get()
                                    while check(tea, courses) == False:
                                        q2.put(tea)
                                        if q3.empty():
                                            tea = q1.get()
                                        else:
                                            tea = q3.get()

                                    jian = model.invigilate()
                                    jian.course_code = courses[i].course_code
                                    jian.course_name = courses[i].course_name
                                    jian.academicbuilding = "理四"
                                    jian.classroomId = "108"
                                    jian.time = courses[i].str_time
                                    jian.isstop = 1
                                    jian.tId = tea.tId
                                    jian.tname = tea.tname
                                    q1.put(tea)
                                    model.db.session.add(jian)
                                    model.db.session.commit()

                                jian = model.invigilate()
                                jian.course_code = courses[i].course_code
                                jian.course_name = courses[i].course_name
                                jian.academicbuilding = "理四"
                                jian.classroomId = "108"
                                jian.time = courses[i].str_time
                                jian.isstop = 0
                                jian.tId = courses[i].teacher_id
                                jian.tname = courses[i].teachingteacher
                                model.db.session.add(jian)
                                model.db.session.commit()

                                exam = model.exam()
                                exam.academicbuilding = "理四"
                                exam.classroomId = "108"
                                exam.course_name = courses[i].course_name
                                exam.time = courses[i].str_time
                                exam.course_code = courses[i].course_code
                                exam.type = 4
                                model.db.session.add(exam)
                                model.db.session.commit()

                            else:
                                #需要多少理四五楼的教室
                                if int(nn % 49) == 0:
                                    nt = int(nn/49)
                                else:
                                    nt = int(nn/49) + 1
                                # 78为南校教室的最大容量，待更改
                                if int(nn % 81) == 0:
                                    ntt = int(nn/81)
                                else:
                                    ntt = int(nn/81) + 1
                                #将座位排在理四五楼的教室
                                if int(nn/ntt/81) <= int(nn/nt/49) and co2 - now2 >= nt:
                                    now2 += nt
                                    ful2 = int(nn % nt)
                                    pnum = int(nn / nt) + 1
                                    cnt = 0
                                    for ttt in range(0, nt):
                                        if ttt == ful2:
                                            pnum = pnum - 1
                                        #当前排到第几排
                                        ppp = 0
                                        if pnum > 35:
                                            ba = 7
                                        else:
                                            ba = 5
                                        row_max_num = int(pnum % ba)
                                        row_max = int(pnum / ba) + 1
                                        rn = 0
                                        ff = 0
                                        for nnn in range(cnt, cnt + pnum):
                                            if nnn >= nn:
                                                break
                                            # if ppp == row_max_num:
                                            #      row_max = row_max - 1
                                            if nnn == cnt:
                                                if pnum > 35:
                                                    seat = 0
                                                else:
                                                    seat = 7
                                                rn = rn + 1
                                                ppp = 0
                                                if ppp == row_max_num:
                                                    row_max = row_max - 1
                                            elif rn == row_max:
                                                seat = (int(seat / 7) + 2) * 7
                                                if seat == 63 and ba == 5:
                                                    seat = 70
                                                rn = 1
                                                ppp = ppp + 1
                                                if ppp == row_max_num:
                                                    row_max = row_max - 1
                                            elif int((seat + 1) % 7) == 0:
                                                seat = seat + 8
                                                rn = 1
                                                ppp = ppp + 1
                                                if ppp == row_max_num:
                                                    row_max = row_max - 1
                                            else:
                                                seat = seat + 1
                                                rn = rn + 1

                                            test = model.test()
                                            test.sId = studys[nnn].sId
                                            test.academicbuilding = classrooms2[ctt2].academicbuilding
                                            test.classroomId = classrooms2[ctt2].classroomId
                                            test.time = courses[i].str_time
                                            test.seat = seat + 1
                                            test.sname = studys[nnn].sname
                                            test.course_name = courses[i].course_name
                                            test.course_code = courses[i].course_code
                                            print(test.sId)
                                            model.db.session.add(test)
                                            model.db.session.commit()
                                        for ppt in range(0, 2):
                                            if q3.empty():
                                                tea = q1.get()
                                            else:
                                                tea = q3.get()
                                            while check(tea,courses) == False :
                                                q2.put(tea)
                                                if q3.empty():
                                                    tea = q1.get()
                                                else:
                                                    tea = q3.get()

                                            jian = model.invigilate()
                                            jian.course_code = courses[i].course_code
                                            jian.course_name = courses[i].course_name
                                            jian.academicbuilding = classrooms2[ctt2].academicbuilding
                                            jian.classroomId = classrooms2[ctt2].classroomId
                                            jian.time = courses[i].str_time
                                            jian.isstop = 1
                                            jian.tId = tea.tId
                                            jian.tname = tea.tname
                                            q1.put(tea)
                                            model.db.session.add(jian)
                                            model.db.session.commit()

                                        jian = model.invigilate()
                                        jian.course_code = courses[i].course_code
                                        jian.course_name = courses[i].course_name
                                        jian.academicbuilding = classrooms2[ctt2].academicbuilding
                                        jian.classroomId = classrooms2[ctt2].classroomId
                                        jian.time = courses[i].str_time
                                        jian.isstop = 0
                                        jian.tId = courses[i].teacher_id
                                        jian.tname = courses[i].teachingteacher
                                        model.db.session.add(jian)
                                        model.db.session.commit()


                                        exam = model.exam()
                                        exam.academicbuilding = classrooms2[ctt2].academicbuilding
                                        exam.classroomId = classrooms2[ctt2].classroomId
                                        exam.course_name = courses[i].course_name
                                        exam.time = courses[i].str_time
                                        exam.course_code = courses[i].course_code
                                        exam.type = 2
                                        model.db.session.add(exam)
                                        model.db.session.commit()

                                        ctt2 = ctt2 + 1
                                        cnt = cnt + pnum

                                #将座位排在南校的普通教室
                                else:
                                    lazy = 0
                                    ctt3 = now3
                                    now3 += ntt
                                    ful3 = int(nn % ntt)
                                    pnum = int(nn / ntt) + 1
                                    cnt = 0
                                    ba = 7
                                    for ttt in range(0, ntt):
                                        if ttt == ful3:
                                            pnum = pnum - 1
                                        # 当前排到第几排
                                        ppp = 0
                                        seat = 0
                                        row_max_num = int(pnum % ba)
                                        row_max = int(pnum / ba) + 1
                                        rn = 0
                                        ff = 0
                                        for nnn in range(cnt, cnt + pnum):
                                            if nnn >= nn:
                                                break
                                            if nnn == cnt:
                                                seat = 0
                                                rn = rn + 1
                                                ppp = 0
                                                if ppp == row_max_num:
                                                    row_max = row_max - 1
                                            elif rn == row_max and ppp != 6:
                                                seat = (int(seat / 12) + 2) * 12
                                                if seat == 48:
                                                    seat = 36
                                                if seat == 108:
                                                    seat = 96
                                                rn = 1
                                                ppp = ppp + 1
                                                if ppp == row_max_num and lazy == 0:
                                                    row_max = row_max - 1
                                                if ppp == 2:
                                                    row_max = row_max + 1
                                                if ppp == 5 and lazy == 0:
                                                    row_max = row_max - 1
                                                if row_max > 12:
                                                    row_max = 12
                                                    lazy = 1
                                            # elif int((seat + 1) % 12) == 0 and ppp != 6:
                                            #     seat = seat + 12
                                            #     rn = 1
                                            #     ppp = ppp + 1
                                            #     if ppp == row_max_num and lazy == 0:
                                            #         row_max = row_max - 1
                                            #     if ppp == 2:
                                            #         row_max = row_max + 1
                                            #     if ppp == 5:
                                            #         row_max = row_max - 1
                                            #     if row_max > 12:
                                            #         row_max = 12
                                            else:
                                                seat = seat + 1
                                                rn = rn + 1

                                            test = model.test()
                                            test.sId = studys[nnn].sId
                                            test.academicbuilding = classrooms3[ctt3].academicbuilding
                                            test.classroomId = classrooms3[ctt3].classroomId
                                            test.time = courses[i].str_time
                                            test.seat = seat + 1
                                            test.sname = studys[nnn].sname
                                            test.course_name = courses[i].course_name
                                            test.course_code = courses[i].course_code
                                            print(test.sId)
                                            model.db.session.add(test)
                                            model.db.session.commit()
                                        for ppt in range(0, 2):
                                            if q3.empty():
                                                tea = q1.get()
                                            else:
                                                tea = q3.get()
                                            while check(tea, courses) == False:
                                                q2.put(tea)
                                                if q3.empty():
                                                    tea = q1.get()
                                                else:
                                                    tea = q3.get()

                                            jian = model.invigilate()
                                            jian.course_code = courses[i].course_code
                                            jian.course_name = courses[i].course_name
                                            jian.academicbuilding = classrooms3[ctt3].academicbuilding
                                            jian.classroomId = classrooms3[ctt3].classroomId
                                            jian.time = courses[i].str_time
                                            jian.isstop = 1
                                            jian.tId = tea.tId
                                            jian.tname = tea.tname
                                            q1.put(tea)
                                            model.db.session.add(jian)
                                            model.db.session.commit()

                                        jian = model.invigilate()
                                        jian.course_code = courses[i].course_code
                                        jian.course_name = courses[i].course_name
                                        jian.academicbuilding = classrooms3[ctt3].academicbuilding
                                        jian.classroomId = classrooms3[ctt3].classroomId
                                        jian.time = courses[i].str_time
                                        jian.isstop = 0
                                        jian.tId = courses[i].teacher_id
                                        jian.tname = courses[i].teachingteacher
                                        model.db.session.add(jian)
                                        model.db.session.commit()


                                        exam = model.exam()
                                        exam.academicbuilding = classrooms3[ctt3].academicbuilding
                                        exam.classroomId = classrooms3[ctt3].classroomId
                                        exam.course_name = courses[i].course_name
                                        exam.time = courses[i].str_time
                                        exam.course_code = courses[i].course_code
                                        exam.type = 3
                                        model.db.session.add(exam)
                                        model.db.session.commit()

                                        ctt3 = ctt3 + 1
                                        cnt = cnt + pnum




































