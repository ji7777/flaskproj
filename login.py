from flask import Flask,render_template,url_for,request,redirect
import jsonify
import pandas as pd
from other import inser_new
app=Flask(__name__,template_folder='template',static_folder='static')
@app.route('/')
def hi():
    return render_template('work.html',i="login")
@app.route('/endd',methods=["GET","POST"])
def helo():
    e=None
    if request.method=="POST":
        x=request.form.to_dict()
        if x is None:
            e="Try again"
        else:
            print(x)
            inser_new(x['user'],x['email'])
            return redirect(url_for('ok'))
    return render_template('signup.html',e=e,i="sign up")
@app.route('/home')
def ok():
    return render_template('homepage.html',i="expense calc")

if __name__=='__main__':
    app.run(debug=True)