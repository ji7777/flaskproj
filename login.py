from flask import Flask,render_template,url_for,request,redirect,session
import jsonify,pickle,random
import pandas as pd
from other import expense,valid_login,valid
from datetime import timedelta
import matplotlib.pyplot as plt
app=Flask(__name__,template_folder='template',static_folder='static')
app.secret_key='newwork'
@app.route('/',methods=["GET","POST"])
def hi():
    err=None
    if request.method=="POST":
        x=request.form["uid"]
        session['uid']=x
        err=valid_login(x)
        b=expense(x)
        session['obj']=pickle.dumps(b)
        if err is not None:
            return redirect(url_for('ok'))
        else:
            err="wrong uid"
    return render_template('work.html',err=err,i="login")
@app.route('/endd',methods=["GET","POST"])
def helo():
    err=None
    uid=None
    if request.method=="POST":
        x=request.form.to_dict()
        e=valid(x['username'])
        print(e)
        if e is None:
            print(x)
            err=None
            uid=x['username']+str(random.randint(0,10000))+x['email'][1:5]
            session['uid']=uid
            b=expense(uid)
            b.inser_new(x['username'],x['email'],uid,x['salary'])
        else:
            err=e
            uid=None
        print(err)
    return render_template('signup.html',e=err,i="sign up",uid=uid)
@app.route('/home',methods=["GET","POST"])
def ok():
    u=None
    f=''
    i=''
    data=[]
    l=session.get("obj")
    z=pickle.loads(l)
    if request.method=="POST":
        x=request.form["expense"]
        y=request.form["cost"]
        r=request.form["rec"]
        print(session)
        f=session['uid']
        z.insert_exp(x,y,r)
        print("DATA INSERTED")
        return redirect(url_for('ok'))
    i,data=z.view()
    z.viz()
        
    
    print(session,i,data)
    if 'uid' not in session:
        return redirect(url_for('log'))
    
    return render_template('homepage.html',uid=f,i="expense calc",u=u,rem=i,data=data)

    # z=session.get("obj")
        
    # u=pickle.loads(z)
            
    # print(session)
    # f=session.get('uid',None)
    
@app.route('/logout')
def log():
    session.pop('uid', None)
    session.pop('data_inserted', None)
    return render_template('logout.html')

def run_flask_app():
    app.run(debug=True,threaded=True)

if __name__=='__main__':
    run_flask_app()