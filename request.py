import sys
from flask import Flask, jsonify, request,render_template,session,redirect,url_for,json
import pymysql 
import requests
import traceback
import cgi
from flask.sessions import SessionInterface
from flask.sessions import SessionMixin
from itsdangerous import Signer, BadSignature, want_bytes

import requests
from bs4 import Tag, BeautifulSoup as bs
from lxml import html

import random
import numpy as np

from collections import Counter   

from datetime import date

import os
import time
app = Flask(__name__)
#student_ID=""
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_USE_SIGNER'] = False  
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 7200
app.config['SESSION_FILE_THRESHOLD'] = 100  
app.config['SECRET_KEY'] = "advancedsw"
#我來感受一下的
#conn = pymysql.connect(host=‘127.0.0.1‘, port=3307, user=‘root‘, passwd=‘hch123‘, db=‘zst‘, charset=‘utf8‘)
#db= pymysql.connect(host="127.0.0.1",port=3307,user="advancedsw",password="advancedsw",db="advancedsw")

db= pymysql.connect(host="127.0.0.1",port=3306,user="root",password="",db="test") # 育恆的db
cursor=db.cursor()

#-----------------首頁功能------------------------

@app.route('/') #進入點
def f_index():
    username=session.get('username')
    if username:
        return render_template('index.html',login_message=1,user=username)
    else:
        return render_template('index.html',login_message=0)

@app.route('/index') #首頁畫面
def login_in():
    username=session.get('username')
    if username:
        return render_template('index.html',login_message=1,user=username)
    else:
        return render_template('index.html',login_message=0)

@app.route('/Searchrecipe' ,methods=['GET', 'POST']) #搜尋食譜畫面
def Searchrecipe():
    username=session.get('username')
    SearchByfood = request.values['SearchByfood']
    SearchByingredient=request.values['SearchByingredient']
    if SearchByfood: #藉由餐點(炒飯) 找實作影片
        #print(SearchByfood)
        select="SELECT * FROM `linkandrecipe`, `recipe` WHERE mealname='%s' and recipe.mealid=linkandrecipe.mealid"%(SearchByfood)
        #print(select)
        cursor.execute(select)
        data=cursor.fetchall()
        
        if username:
            return render_template('findvideo.html',login_message=1,user=username,linkdata=data,recipe=SearchByfood)
        else:
            return render_template('findvideo.html',login_message=0,linkdata=data,recipe=SearchByfood)

    elif SearchByingredient:#藉由食材(鹽 糖 等等)找實作影片
        Findrecipelink=[]
        #print(SearchByingredient)
        ingredient=SearchByingredient.split()
        #print(ingredient)
        temp=[]
        if(len(ingredient)==1):
                select="SELECT mealname FROM `foodandrecipe`, `food`,`recipe` WHERE ingredientname='%s' and food.ingredientid=foodandrecipe.ingredientid and foodandrecipe.mealid=recipe.mealid"%(ingredient[0])
                cursor.execute(select)
                data=cursor.fetchall()
                for i in range(len(data)):
                    ans=str(data[i])
                    ans=ans.strip('()')
                    ans=ans.strip(',')
                    ans=ans.strip('\'') 
                    select="SELECT * FROM `linkandrecipe`, `recipe` WHERE mealname='%s' and recipe.mealid=linkandrecipe.mealid"%(ans)
                    cursor.execute(select)
                    link_data=cursor.fetchall()
                    for j in range(len(link_data)):
                        Findrecipelink.append(link_data[j])
                if username:
                    return render_template('findvideo.html',login_message=1,user=username,linkdata=tuple(Findrecipelink))
                else:
                    return render_template('findvideo.html',login_message=0,linkdata=tuple(Findrecipelink))
                    
        else:
            for i in range(len(ingredient)):
                select="SELECT mealname FROM `foodandrecipe`, `food`,`recipe` WHERE ingredientname='%s' and food.ingredientid=foodandrecipe.ingredientid and foodandrecipe.mealid=recipe.mealid"%(ingredient[i])
                print(select)
                cursor.execute(select)
                data=cursor.fetchall()
                for j in range(len(list(data))):
                    temp.append(list(data)[j])    
            count=dict(Counter(temp))
            temp2=[key for key,value in count.items()if value ==len(ingredient)]
            for i in range(len(temp2)):
                ans=str(temp2[i])
                ans=ans.strip('()')
                ans=ans.strip(',')
                ans=ans.strip('\'')
                select="SELECT * FROM `linkandrecipe`, `recipe` WHERE mealname='%s' and recipe.mealid=linkandrecipe.mealid"%(ans)
                cursor.execute(select)
                link_data=cursor.fetchall()
                for j in range(len(link_data)):
                    Findrecipelink.append(link_data[j])
            if username:
                return render_template('findvideo.html',login_message=1,user=username,linkdata=tuple(Findrecipelink))
            else:
                return render_template('findvideo.html',login_message=0,linkdata=tuple(Findrecipelink))
    

#-----------------首頁功能------------------------


#-----------------菜單功能------------------------
@app.route('/menu') #菜單畫面
def menu():
    username=session.get('username')
    if username:
        return render_template('menu.html',login_message=1,user=username)
    else:
        return render_template('menu.html',login_message=0)


@app.route('/random',methods=['GET', 'POST']) #隨機菜單
def random_func():
    random_day = int(request.values['random_day'])
    num_of_meal = int(request.values['num_of_meal'])
    print("random:",random_day)
    print("num_of_meal:",num_of_meal)

    select = "SELECT * FROM `recipe`"
    cursor.execute(select)
    data = cursor.fetchall()
    print("data[0]: ",data[0])
    print("type of data: ", type(data[0]))
    print("len of data: ",len(data))

    day_and_meal = [[0 for i in range(random_day)]for j in range(num_of_meal)]
    for i in range(num_of_meal):
        for j in range(random_day):
            temp = data[random.randint(0,len(data)-1)][1]
            day_and_meal[i][j] = temp

    print(day_and_meal)
    print("temp: ",type(day_and_meal))
    print(len(day_and_meal[0]))
    return render_template('randomMenu.html',meal_from_back=day_and_meal, meal_i=len(day_and_meal[0]))

#-----------------菜單功能------------------------


#-----------------登入/登出功能------------------------

@app.route('/login') #登入頁面
def login():
    session.clear()
    return render_template('login.html')

@app.route('/logout') #登出畫面
def logout():
    session.clear()
    return redirect('/')

@app.route('/confirm', methods=['GET', 'POST'])  #登入
def confirm():  
    session.clear()
    ID = request.values['account']
    pwd =request.values['password']
    if(ID.isupper):
        ID=ID.upper()
    session['username']=ID
    session.permanent=True
    session.get('username')
    select="SELECT * FROM `user` WHERE account='%s' and password='%s'"%(ID,pwd)
    print(select)
    cursor.execute(select)
    data=cursor.fetchone()
    if(data!=None):
        return redirect('/')
    else:
        return '請註冊'

#-----------------登入/登出功能------------------------


#-----------------註冊功能------------------------

@app.route('/register') #註冊畫面
def register():
    session.clear()
    return render_template('register.html')


@app.route('/action', methods=['GET', 'POST'])  #註冊
def action():
    session.clear()
    ID = request.values['account']
    pwd =request.values['password']
    if(ID.isupper):
        ID=ID.upper()
    insert="INSERT INTO user (account, password) VALUES(%s,%s)"
    print(insert)
    try:
        cursor.execute(insert,(ID,pwd))
        db.commit()
    except:
        db.rollback()
    return render_template("login.html",register_message=1)

#-----------------註冊功能------------------------


#-----------------冰箱功能------------------------

@app.route('/addrefrig') #新增畫面
def addrefrig():
    username=session.get('username')
    if username:
        return render_template('addrefrig.html',login_message=1,user=username)
    
@app.route('/refrig') #冰箱畫面
def refrig():
    username=session.get('username')
    if username:
        select="SELECT * FROM `refrigerator` WHERE account='%s'"%(username)
        #print(select)
        cursor.execute(select)
        data=cursor.fetchall()
        if (data!=None):
            return render_template('refrig.html',login_message=1,user=username,userdata=data,lendata=len(data))
        else:
            return render_template('refrig.html',login_message=1,user=username)
    else:
        return '請先登入'
@app.route('/addingredient', methods=['GET', 'POST'])  #新增食材到冰箱
def addingredient():
    username=session.get('username')
    ingredientname = request.values['ingredientname']
    expire =request.values['expire']

    select="SELECT * FROM `refrigerator` WHERE account='%s'"%(username)
    cursor.execute(select)
    data=cursor.fetchall()

    start_time=date.today()
    start_time=str(start_time)
    start_time=start_time.split('-')
    end_time=expire.split('-')
    
    deadline=[]

    for i in range(3):
        deadline.append(int(end_time[i])-int(start_time[i]))
    answer=deadline[0]*365+deadline[1]*30+deadline[2]
    print(answer) 
    insert="INSERT INTO `refrigerator` (selfid, ingredientname, expire, account, deadline) VALUES(%s,%s,%s,%s,%s)"
    print(insert)
    try:
        cursor.execute(insert,(len(data)+1,ingredientname,expire,username,str(answer)))
        db.commit()
    except:
        db.rollback()
    return redirect('/refrig')

@app.route('/delete' , methods=['GET', 'POST'])  #刪除冰箱的食材
def delete():
    username=session.get('username')
    selfid=request.form.get("selfid")
    #print(username)
    #print(selfid)
    select="SELECT * FROM `refrigerator` WHERE account='%s'"%(username)
    cursor.execute(select)
    data=cursor.fetchall()
    #print(select)

    delete="DELETE FROM `refrigerator` WHERE account='%s' and selfid='%s'"%(username,selfid)
    print(delete)

    cursor.execute(delete)
    db.commit()
    i=int(selfid)       
    print(i)
    while(i!=len(data)):    
        i+=1
        update='UPDATE `refrigerator` SET `selfid` = '+str(i-1)+' WHERE `selfid` = '+str(i)+''
        #print(update)
        cursor.execute(update)
        db.commit()
    return redirect('/refrig')

#-----------------冰箱功能------------------------



# @app.route('/searchCourse')  #課程檢索
# def f_sear1ch1():
#     student=session.get('username')
#     name=session.get('name')
#     Class=session.get('Class')
#     login_message=session.get('login_message')
#     alert_msg=""
     
#     return render_template('searchCourse.html',alert_msg=alert_msg,student=student,name=name,Class=Class,login_message=login_message)
# @app.route('/research')  #課程檢索
# def research():   
#     student=session.get('username')
#     name=session.get('name')
#     Class=session.get('Class')
#     login_message=session.get('login_message')
#     msg=request.values['alert_msg']
#     print(msg)
#     return render_template('searchCourse.html',alert_msg=msg,student=student,name=name,Class=Class,login_message=login_message)
        
# @app.route('/search1', methods=['GET', 'POST']) # 下拉式選單
# def search():
#     student=session.get('username')
#     name=session.get('name')
#     Class=session.get('Class')
#     login_message=session.get('login_message')
    
#     college=(str(request.form['college']))
#     query="SELECT *,if(COUNT(section)>1,section+COUNT(section)-1,section) AS endsection  FROM course NATURAL JOIN coursetime GROUP BY c_id,day HAVING  course.class='%s'"%(college)
#     cursor.execute(query)
#     data =cursor.fetchall()
#     for  value in data:
#          print(value)
#     return render_template('Courselist.html',books=data,student=student,name=name,Class=Class,login_message=login_message)

# @app.route('/search2', methods=['GET', 'POST']) #textbox搜尋
# def search2():
    
#     student=session.get('username')
#     name=session.get('name')
#     Class=session.get('Class')
#     login_message=session.get('login_message')
    
#     c_id=(str(request.form['C_ID']))
#     c_name=(str(request.form['C_name']))
#     t_id=(str(request.form['T_ID']))
#     query="SELECT *,if(COUNT(section)>1,section+COUNT(section)-1,section) AS endsection  FROM course NATURAL JOIN coursetime GROUP BY c_id,day HAVING "
#     if(c_id!="" and c_name!="" and t_id!=""):
#         query+="course.c_id LIKE \"%%%s%%\" and course.c_name LIKE \"%%%s%%\" and course.instructor LIKE \"%%%s%%\""%(c_id,c_name,t_id)
#     elif(c_id!="" and c_name!=""):
#         query+="course.c_id LIKE \"%%%s%%\" and course.c_name LIKE \"%%%s%%\""%(c_id,c_name)
#     elif(c_id!="" and t_id!=""):
#         query+="course.c_id LIKE \"%%%s%%\" and course.instructor LIKE \"%%%s%%\""%(c_id,t_id)
#     elif(c_name!="" and t_id!=""):
#         query+="course.c_name LIKE \"%%%s%%\" and course.instructor LIKE \"%%%s%%\""%(c_name,t_id)    
#     elif(c_id!=""):
#         query+="course.c_id LIKE \"%%%s%%\""%(c_id)
#     elif(c_name!=""):
#         query+="course.c_name LIKE \"%%%s%%\""%(c_name)
#     elif(t_id!=""):
#         query+="course.instructor LIKE \"%%%s%%\""%(t_id)
#     else:
#         return "None"
#     cursor.execute(query)
#     data =cursor.fetchall()
#     for  value in data:
#          print(value)
#     return render_template('Courselist.html',books=data,student=student,name=name,Class=Class,login_message=login_message)

# @app.route('/Courselist_admin', methods=['GET', 'POST']) # admin 搜尋學生課表
# def search3():
#     student=session.get('username')
#     name=session.get('name')
#     Class=session.get('Class')
#     login_message=session.get('login_message')
    
#     stu_id=str(request.form['stu_id'])
#     stu_id=stu_id.upper()
#     query="SELECT c_id,s_id,c_name,credits,queue,day,section,section+COUNT(section)-1 AS endsection FROM course natural join(timetable NATURAL JOIN coursetime)GROUP BY s_id,c_id,day HAVING s_id='%s'"%(stu_id)
#     cursor.execute(query)
#     data =cursor.fetchall()
#     for  value in data:
#          print(value)
#     return render_template('Courselist_admin.html',books=data,student=student,name=name,Class=Class,login_message=login_message)
    
    

# @app.route('/add')  # 加選課程
# def add():
#     student=session.get('username')
#     name=session.get('name')
#     Class=session.get('Class')
#     login_message=session.get('login_message')
#     message="加選成功"
#     course=list(request.args.values())
    
#     cursor.execute("SELECT c_id,s_id,c_name,credits,queue,day,section,section+COUNT(section)-1 AS endsection FROM course natural join(timetable NATURAL JOIN coursetime)GROUP BY s_id,c_id,day HAVING s_id=\"%s\""%(student))
#     data=cursor.fetchall()

#     cursor.execute("SELECT *,section+COUNT(section)-1 AS endsection FROM course NATURAL JOIN coursetime GROUP BY c_id,day HAVING course.c_id ='%s'"%(course[0]))
#     coursetime=cursor.fetchall()
#     print(course)
    
#     for i in coursetime:#判斷衝堂
#         for j in data:
#             if(i[8]==j[5] and int(i[9])<=int(j[6]) and int(i[10])>=int(j[7])):
#                 print(i)
#                 print(j)
#                 return redirect(url_for('research',alert_msg="衝堂",student=student,name=name,Class=Class,login_message=login_message))
    
 
#     credit=int(0)
#     sum_cre=int(0)
#     for i in data:#判斷重複選課and課程人數
#         if(course[1]==i[2]):
#             return redirect(url_for('research',alert_msg="不可重複選課",student=student,name=name,Class=Class,login_message=login_message))
#     if(int(course[4])>=int(course[5])):
#         return redirect(url_for('research',alert_msg="課程人數已滿",student=student,name=name,Class=Class,login_message=login_message))    
        
#     cursor.execute("SELECT credits FROM course natural join timetable GROUP BY s_id,c_id HAVING s_id='%s'"%(student)) # 判斷學分是否超過30學分
#     credit=cursor.fetchall()
#     for i in credit:
#         sum_cre+=i[0]
    
#     if(int(sum_cre)+int(course[3])>30):
#         print(int(sum_cre)+int(course[3]))
#         return redirect(url_for('research',alert_msg="超過30學分",student=student,name=name,Class=Class,login_message=login_message))
    
#     cursor.execute("INSERT INTO timetable(s_id,c_id,queue) VALUES ('%s','%s',0);"%(student,course[0]))#加選
#     cursor.execute("UPDATE `course` SET `num_of_students`=%d WHERE `c_id`='%s'"%(int(course[4])+1,course[0])) 
#     db.commit()
    
#     return redirect(url_for('research',alert_msg="加選成功",student=student,name=name,Class=Class,login_message=login_message))

# @app.route('/pop') #退選課程
# def pop():
#     student=session.get('username')
#     name=session.get('name')
#     Class=session.get('Class')
#     login_message=session.get('login_message')
#     alert_msg=""
#     course=list(request.args.values())
#     credit=int(0)
#     cursor.execute("SELECT sum(credits) FROM timetable join course WHERE `s_id`='%s'"%(student)) # 判斷學分是否低於12學分
#     credit=cursor.fetchall()
    
    
#     sum_cre=int(0)   
#     cursor.execute("SELECT c_name FROM timetable join course WHERE c_name='%s'"%(course[1]))
#     noclass=cursor.fetchall()

#     cursor.execute("SELECT credits FROM course natural join timetable GROUP BY s_id,c_id HAVING s_id='%s'"%(student)) # 判斷學分是否超過30學分
#     credit=cursor.fetchall()
#     for i in credit:
#         sum_cre+=i[0]
        
#     if(len(noclass)==0):
#         return redirect(url_for('research',alert_msg="課表無此課",student=student,name=name,Class=Class,login_message=login_message))   
#     if(int(sum_cre)-int(course[3])<12):
#         return redirect(url_for('research',alert_msg="低於12學分不可退選",student=student,name=name,Class=Class,login_message=login_message))#低於12學分
#     if(course[2]=="M" and course[6]==Class):
#         return redirect(url_for('research',alert_msg="必修不可退",student=student,name=name,Class=Class,login_message=login_message))#必修不可退
    
    
#     cursor.execute("DELETE FROM timetable WHERE s_id='%s' and c_id='%s';"%(student,course[0]))
#     cursor.execute("UPDATE `course` SET `num_of_students`=%d WHERE `c_id`='%s'"%(int(course[4])-1,course[0])) 
#     db.commit()
#     return redirect(url_for('research',alert_msg="退選成功",student=student,name=name,Class=Class,login_message=login_message))

# @app.route('/pop1') #admin退選課程
# def pop1():
#     student=session.get('username')
#     name=session.get('name')
#     Class=session.get('Class')
#     login_message=session.get('login_message')
#     alert_msg=""
#     course=list(request.args.values())
#     print(course)
#     cursor.execute("DELETE FROM timetable WHERE s_id='%s' and c_id='%s'and queue=0;"%(course[1],course[0]))
#     cursor.execute("SELECT num_of_students FROM `course` WHERE c_id='%s'"%(course[0]))
#     data=cursor.fetchone()
#     print(str(data[0]))
#     cursor.execute("UPDATE `course` SET `num_of_students`=%d WHERE `c_id`='%s'"%(int(str(data[0]))-1,course[0])) 
#     db.commit()
#     return redirect(url_for('research',alert_msg="退選成功",student=student,name=name,Class=Class,login_message=login_message))
    
# @app.route('/schedule') #課表
# def schedule():
#     student=session.get('username')
#     name=session.get('name')
#     Class=session.get('Class')
#     login_message=session.get('login_message')
    
#     cursor.execute("SELECT c_id,s_id,c_name,credits,queue,day,section,section+COUNT(section)-1 AS endsection FROM course natural join(timetable NATURAL JOIN coursetime)GROUP BY s_id,c_id,day HAVING s_id=\"%s\""%(student))
#     data=cursor.fetchall()
#     print(session.get('name'),session.get('Class'))
    
#     list1=[]
#     list1.append((len(data),"",0,0))
#     n=int(0)
#     for i in data:
#         print(i)
#         if(i[5]=='一'): n=1
#         elif(i[5]=='二'): n=2
#         elif(i[5]=='三'): n=3
#         elif(i[5]=='四'): n=4
#         elif(i[5]=='五'): n=5
#         elif(i[5]=='六'): n=6
#         elif(i[5]=='日'): n=7
#         else: n=0
#         list1.append((n,i[2],i[6],i[7]))
#     for i in list1:
#         print(i)
#     return render_template('schedule.html',books=list1,student=student,name=name,Class=Class,login_message=login_message)




        
     
    
if __name__ == "__main__": 
    app.run(debug=False, host='127.0.0.1', port=5000)  
    sys.exit()
    
