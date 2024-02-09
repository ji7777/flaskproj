from flask import Flask,render_template,url_for,request
import pandas as pd
app=Flask(__name__,template_folder='template',static_folder='static')
@app.route('/')
def hi():
    return render_template('work.html')
@app.route('/endd')
def helo():
    return render_template('signup.html')
if __name__=='__main__':
    app.run()