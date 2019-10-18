# 

from flask import Flask, session, redirect, url_for, escape, request, render_template
from flask import jsonify
from flask_cors import *

import sqlite3
app = Flask(__name__)
CORS(app, supports_credentials=True)



@app.route('/')
@app.route('/api')
def index():
    return render_template("login.html")

@app.route('/api/ChooseClass',methods = ['GET', 'POST'])
def ChooseClass():
    if request.method == 'POST':
        classID = request.form.get('classID')
        peopleID = request.form.get('peopleID')
        # if session['username'] != peopleID or session['position'] != 2:
        #     return jsonify({'status': 1})
        order = 'SELECT * from PEOPLETOCLASS WHERE PEOPLEID=' + peopleID
        print (order)
        conn = sqlite3.connect('choose-class-system.db')
        c = conn.cursor()
        c.execute(order)
        cursor = c.fetchall()
        for row in cursor:
            if row[1] == classID:
                return jsonify({'status': '2'})
        if len(cursor) >= 2:
            return jsonify({'status': '3'})
        order = 'INSERT INTO PEOPLETOCLASS (PEOPLEID, CLASSID) VALUES ("' + peopleID +'","' + classID +'")'
        print (order)
        c.execute(order)
        conn.commit()
        conn.close()
        return jsonify({'status':0})
    return jsonify({'status': '4'})

@app.route('/api/Student/WithdrawClass',methods = ['GET', 'POST'])
def WithdrawClass():
    if request.method == 'POST':
        classID = request.form.get('classID')
        peopleID = request.form.get('peopleID')
        # if session['username'] != peopleID or session['position'] != 2:
        #     return jsonify({'status': 1})
        order = 'SELECT * from PEOPLETOCLASS WHERE PEOPLEID=' + peopleID +' AND CLASSID='+ classID
        print (order)
        conn = sqlite3.connect('choose-class-system.db')
        c = conn.cursor()
        c.execute(conn)
        cursor = c.fetchall()
        for row in cursor:
            order = 'DELETE FROM PEOPLETOCLASS WHERE PEOPLEID=' + peopleID +' AND CLASSID='+ classID
            print (order)
            c.execute(order)
            conn.commit()
            conn.close()
            return jsonify({'status': '0'})
        return jsonify({'status': '2'})
    return jsonify({'status': '3'})

@app.route('/api/Student/ClassStatus',methods = ['GET', 'POST'])
def StudentClassStatus():
    if request.method == 'POST':
        # print("????")
        peopleID = request.form.get('peopleID')
        # print(peopleID)
        # if session['username'] != peopleID or session['position']!= 2:
        #     return jsonify({'status': 1})
        order = 'SELECT * from PEOPLETOCLASS WHERE PEOPLEID = ' +peopleID
        print (order)
        conn = sqlite3.connect('choose-class-system.db')
        c = conn.cursor()
        # cursor = 
        c.execute(order)
        cursor = c.fetchall()
        t={}
        for num in range(1,len(cursor)):
            t[str(num)] = {
                'classID':   cursor[num - 1][0],
                'className': cursor[num-1][1],
                'classTime': cursor[num-1][2],
                'address':   cursor[num-1][3],
                'teacher':   cursor[num-1][4],
                'comments':  cursor[num-1][5],
                'count':     cursor[num-1][6],
                'point':     cursor[num-1][7],
                'score':     cursor[num-1][8]
            }
        return jsonify({'status': '0', 'class':t})
    return jsonify({'status': '2'})

@app.route('/api/Class/detail',methods = ['GET', 'POST'])
def ClassDetail():
    if request.method == 'POST':
        classID = request.form.get('classID')
        conn = sqlite3.connect('choose-class-system.db')
        c = conn.cursor()
        order = 'SELECT * FROM CLASS WHERE CLASSID = '+classID
        print(order)
        c.execute(order)
        cur = c.fetchall()
        if len(cur) == 0:
            return jsonify({'status':'1'})
        return jsonify({'status':         '0',
                        'classTime':      cur[0][2],
                        'classAddress':   cur[0][3],
                        'comments':       cur[0][5]})
    return jsonify({'status':'2'})    


@app.route('/api/Class',methods = ['GET', 'POST'])
def ClassStatus():
    if request.method == 'POST':
        classID = request.form.get('classID')
        peopleID = request.form.get('peopleID')
        # if session['username'] != peopleID:
        #     return jsonify({'status': 1})
        order = 'SELECT * from CLASS'
        print (order)
        conn = sqlite3.connect('choose-class-system.db')
        c = conn.cursor()
        c.execute(order)
        cursor = c.fetchall()
        conn.close()
        t={}
        for num in range(0,len(cursor)):
            t[num] = (  {
                'classID':   cursor[num][0],
                'className': cursor[num][1],
                'teacher':   cursor[num][4],
                'count':     cursor[num][6],
                'point':     cursor[num][7],
                'score':     cursor[num][8]
            })
        print(t)
        return jsonify({'status': '0', 'class':t})
    return jsonify({'status': '2'})

@app.route('/api/Student/Status',methods = ['GET', 'POST'])
def StudentStatus():
    if request.method == 'POST':
        peopleID = request.form.get('peopleID')
        print(peopleID)
        # if 'username' in session:
        #     print("ok!!!")
        #     return jsonify({'status':0})
        # if session['username'] != peopleID or session['position'] != 1:
        #     return jsonify({'status': 1})
        conn = sqlite3.connect('choose-class-system.db')
        c = conn.cursor()
        order = 'SELECT * FROM PEOPLE WHERE ID= ' + peopleID
        c.execute(order)
        cur = c.fetchall()
        if len(cur) == 0:
            return jsonify({'status': '2'})
        return jsonify({'status': '0','name':cur[0][2],'college':cur[0][5],'admissionYear':cur[0][6]})
    return jsonify({'status':'3'})

@app.route('/api/Teacher/Status',methods = ['GET', 'POST'])
def TeacherStatus():
    if request.method == 'POST':
        peopleID = request.form.get('peopleID')
        # if session['username'] != peopleID or session['position'] != 1:
        #     return jsonify({'status': 1})
        conn = sqlite3.connect('choose-class-system.db')
        c = conn.cursor()
        order = 'SELECT * FROM PEOPLE WHERE ID=' + peopleID
        c.execute(order)
        cur = c.fetchall()
        if len(cur) == 0:
            return jsonify({'status': '2'})
        return jsonify({'status': '0','name':cur[0][2],'peopleID':cur[0][0]})
    return jsonify({'status':'3'})



@app.route('/api/Teacher/AddClass', methods = ['GET', 'POST'])
def AddClass():
    if request.method == 'POST':
        peopleID = request.form.get('peopleID')
        # if session['username'] != peopleID or session['position'] != 1:
        #     return jsonify({'status': 1})
        conn = sqlite3.connect('choose-class-system.db')
        c = conn.cursor()

        className = request.form.get('className')
        classTime = request.form.get('classTime')
        classAddress = request.form.get('classAddress')
        count = request.form.get('count')
        classPoint = request.form.get('classPoint')
        comments = request.form.get('comments')
        order = 'INSERT INTO CLASS(CLASSNAME,CLASSTIME,ADDRESS,TEACHER,COMMENTS,COUNT,POINT) VALUES ("'\
            + className +'","'+classTime +'","'+ classAddress+'",'+ "0" + ',"' +comments +'",'+count+','+classPoint+')'
        print (order)
        c.execute(order)

        conn.commit()
        conn.close()
        return jsonify({'status': '0'})
    return jsonify({'status': '3'})

@app.route('/api/Teacher/UpdataClass', methods  = ['GET', 'POST'])
def TeacherUpdataClass():
    if request.method == 'POST':
        peopleID = request.form.get('peopleID')
        conn = sqlite3.connect('choose-class-system.db')
        c = conn.cursor()
        classID = request.form.get('classID')
        className = request.form.get('className')
        classTime = request.form.get('classTime')
        classAddress = request.form.get('classAddress')
        count = request.form.get('count')
        classPoint = request.form.get('classPoint')
        comments = request.form.get('comments')
        order = 'UPDATE CLASS SET CLASSNAME='+className+' CLASSTIME='+classTime+' ADDRESS'+classAddress+\
            ' COMMENTS'+comments+' COUNT'+count+' POINT'+point+' WHERE CLASSID='+classID
        print(order)
        c.execute(order)
        conn.commit()
        conn.close()
        return jsonify({'status': '0'})
    return jsonify({'status': '2'})


@app.route('/api/Manager/SetPower', methods = ['GET', 'POST'])
def SetPower():
    if request.method == 'POST':
        peopleID = request.form.get('peopleID')
        # if session['username'] != request.rootID or session['position'] != 0:
        #     return jsonify({'status': 1})
        conn = sqlite3.connect('choose-class-system.db')
        c = conn.cursor()
        order = 'SELECT * FROM PEOPLE WHERE ID=' + peopleID
        cur = c.execute(order)
        if len(cur) == 0:
            return jsonify({'status': '2'})
        order = 'UPDATA PEOPLE SET POSITION ='+request.power+' WHERE ID = '+peopleID
        print(order)
        c.execute(order)
        conn.commit()
        conn.close()
        return jsonify({'status':'0'})
    return jsonify({'status':'3'})

@app.route('/api/Manager/UpdataClass', methods = ['GET', 'POST'])
def ManagerUpdataClass():
    if request.method == 'POST':
        peopleID = request.form.get('peopleID')
        # if session['username'] != peopleID or session['position'] != 0:
        #     return jsonify({'status': 1})
        conn = sqlite3.connect('choose-class-system.db')
        c = conn.cursor()
        classID = request.form.get('classID')
        className = request.form.get('className')
        classTime = request.form.get('classTime')
        classAddress = request.form.get('classAddress')
        count = request.form.get('count')
        classPoint = request.form.get('classPoint')
        comments = request.form.get('comments')
        score = request.form.get('score')
        order = 'UPDATE CLASS SET CLASSNAME='+className+' CLASSTIME='+classTime+' ADDRESS='+classAddress+' COMMENTS='+comments+' COUNT='+count+' POINT='+point+\
            ' SCORE='+score+' WHERE CLASSID='+classID
        print(order)
        c.execute(order)
        conn.commit()
        conn.close()
        return jsonify({'status': '0'})
    return True

@app.route('/api/Manager/DeleteClass', methods = ['GET', 'POST'])
def ManagerDeleteClass():
    peopleID = request.form.get('peopleID')
    classID = request.form.get('classID')
    # if session['username'] != peopleID:
    #     return jsonify({'status': 1})
    # if session['position'] != 0:
    #    return jsonify({'status':'3'})
    conn = sqlite3.connect('choose-class-system.db')
    c = conn.cursor()
    order = 'SELECT * FROM CLASS WHERE CLASSID = '+classID
    # cur = 
    c.execute(order)
    cur = c.fetchall()
    if len(cur) == 0:
        return jsonify({'status':'2'})
    order = 'DELETE FROM CLASS WHERE CLASSID = ' +classID
    c.execute(order)
    conn.commit()
    conn.close()
    return jsonify({'status':'0'})
    return True

@app.route('/api/Manager/DeleteStudent', methods = ['GET', 'POST'])
def DeleteStudent():
    if request.method == 'POST':
        peopleID = request.form.get('peopleID')
        studentID = request.form.get('studentID')
        # if session['username'] != peopleID:
        #     return jsonify({'status': 1})
        # if session['position'] != 0:
        #     return jsonify({'status':3})
        conn = sqlite3.connect('choose-class-system.db')
        c = conn.cursor()
        order = 'SELECT * FROM PEOPLE WHERE ID = '+studentID
        # cur =
        c.execute(order)
        cur = c.fetchall()
        if len(cur) == 0:
            return jsonify({'status':'2'})
        order = 'DELETE FROM PEOPLE WHERE ID = ' +studentID
        c.execute(order)
        conn.commit()
        conn.close()
        return jsonify({'status':'0'})
    return jsonify({'status':'3'})

@app.route('/api/SignUp', methods = ['GET','POST'])
def SignUp():
    if request.method == 'POST':
        print(request)
        name = request.form.get('peopleName')
        ID = request.form.get('peopleID')
        print (ID)
        conn = sqlite3.connect('choose-class-system.db')
        c = conn.cursor()
        order = 'SELECT * FROM PEOPLE WHERE ID = '+ID
        c.execute(order)
        cur = c.fetchall()
        if len(cur) :
            return jsonify({'status':'1'})
        passwd = request.form.get('passwd')
        college = request.form.get('college')
        position = request.form.get('position')
        admissionYear = request.form.get('admissionYear')
        print(position)
        telephone = request.form.get('telephone')
        order = 'INSERT INTO PEOPLE (ID,PASSWORD,NAME,POSITION,TELEPHONE,COLLEGE,COURSE,YEAR) VALUES("' + ID +'","'+passwd + '","' +name +'",'+\
            str(position)+',"'+telephone+'","'+college + '","'+ admissionYear + '")'
        print(order)
        c.execute(order)
        conn.commit()
        conn.close()
        return jsonify({'status':'0'})


# userInDataBase uses to check if the user in the datebase.
# if the username or password is wrong, return 1.
def userInDataBase(username,passwd):
    # session[username] = 'teacher'
    order = 'SELECT * FROM PEOPLE WHERE ID='+ username
    print(order)
    conn = sqlite3.connect('choose-class-system.db')
    c = conn.cursor()
    print (order)
    c.execute(order)
    cursor = c.fetchall()
    print(cursor)
    for row in cursor:
        if row[1] == passwd:
            session['username'] = username
            session['position'] = row[3]
            session['name'] = row[2]
            return jsonify({'status': '0','peopleID': row[0], 'name': row[2], 'position' : str(row[3]),'college': row[5], 'admissionYear':row[6]})
        else:
            return jsonify({'status': '1'})
    return jsonify({'status': '1'})

@app.route('/api/ChangePassword', methods = ['GET','POST'])
def changePassword():
    if request.method == 'POST':
        username = request.form['username']
        passwd = request.form['password']
        order = 'SELECT * FROM PEOPLE WHERE ID = '+username
        conn = sqlite3.connect('choose-class-system.db')
        c = conn.cursor()
        print (order)
        # cur = 
        c.execute(order)
        cur = c.fetchall()
        if len(cur) == 0:
            return jsonify({'status':'1'})
        order = 'UPDATA PEOPLE SET PASSWORD =' + passwd + 'WHERE ID = '+username
        c.execute(order)
        c.commit()
        c.close()
        return jsonify({'status':'0'})
    return jsonify({'status':'2'})

@app.route('/api/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        passwd = request.form['password']
        print(username)
        print(passwd)
        return userInDataBase(username,passwd)
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=text name=password>
            <p><input type=submit value=Login>
        </form>
    '''

# if username isn't in session return 1 
@app.route('/api/logout')
def logout():
    username = session.get('username')
    if username != request.form['peopleID']:
        return jsonify({'status': '1'})
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('position', None)
    return jsonify({'status': '0'})

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run(debug = True)