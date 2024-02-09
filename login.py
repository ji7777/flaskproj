from flask import Flask,render_template,url_for,request,redirect
import jsonify
import pandas as pd
app=Flask(__name__,template_folder='template',static_folder='static')
@app.route('/')
def hi():
    return render_template('work.html')
@app.route('/endd',methods=["GET","POST"])
def helo():
    if request.method=="POST":
        x=request.form.to_dict()
        if x is None:
            return "error",404
        else:
            return redirect(url_for('hi'))
    return render_template('signup.html')

if __name__=='__main__':
    app.run(debug=True)