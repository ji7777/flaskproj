import snowflake.connector,os
from dotenv import load_dotenv
import matplotlib
import numpy as np
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import pandas as pd,datetime as dt
import matplotlib.dates as mdates

load_dotenv()
con=snowflake.connector.connect(user=os.environ.get('user'),
password=os.environ.get('password'),
account=os.environ.get('account'),
warehouse=os.environ.get('warehouse'),
database=os.environ.get('database'),
schema=os.environ.get('schema'))
cur=con.cursor()
x=cur.execute("select * from exp_login")
y=x.fetchall()
print(y)
class expense:
    def __init__(self,uid):
        self.uid=uid
    def inser_new(self,uid,username,email,sal):
        self.username=username
        self.email=email
        self.sal=sal
        cur.execute('insert into exp_login values(%s,%s,%s,%s)',(self.username,self.email,self.uid,self.sal))
        con.commit()
    
    def insert_exp(self,desc,cost,rec=None):
        self.desc=desc
        self.cost=cost
        self.rec=rec
        if self.rec=='':
            self.rec=0
        elif self.cost=='':
            self.cost=0
        print(self.desc,self.cost,self.rec)
        t=dt.date.today().isoformat()
        cur.execute('insert into expense values(%s,%s,%s,%s,%s)',(self.desc,self.cost,self.uid,self.rec,t))
        con.commit()
    def view(self):
        cur.execute('select * from expense where uid=%s',self.uid)
        f=cur.fetchall()
        y=pd.DataFrame(data=f,columns=['desc','cost','uid','rec','date'])
        
        cur.execute('select salary,uid from exp_login where uid=%s',self.uid)
        z=pd.DataFrame(data=cur.fetchall(),columns=['salary','uid'])
        
        o=pd.merge(y,z,how='left',on='uid')
        e=o.groupby(['uid','salary'])[['cost','rec']].sum().reset_index()
        e.columns = ['uid', 'salary', 'totalcost', 'totalrec']
        re=[]
        p=0
        q=0
        for i,row in o.iterrows():
            if row['cost'] is None:
                p=0
            if row['rec'] is None:
                q=0
            else:
                q+=row['rec']
            if row['cost'] is not None:
                p+=row['cost']
            re.append(row['salary']-p+q)
        o['rem']=re
        if e.empty:
            e=None
        else:
            e=int((e['salary']-e['totalcost']+e['totalrec']).iloc[0])
        return e,o[['desc','cost','rec','salary','rem','date']]
    def viz(self):
        e, d = self.view()
        fig1 = plt.figure(1,facecolor='lightgrey')
        w = 0.5
        grouped_data = d.groupby('date').sum().reset_index()
        print(grouped_data)
# Get the unique dates and their corresponding indices
        dates = np.arange(len(grouped_data['date']))

# Plot the bars using the grouped data
        plt.bar(dates, grouped_data['cost'], w, label="cost")
        plt.bar(dates+w, grouped_data['rec'], w, label="rec")
        # Calculate positions for bars
        # dates = np.arange(len(d['date'].unique().astype('str').tolist()))
        # print(dates,len(d['cost']),len(d['rec']),d['date'])
        # plt.bar(dates, d['cost'], w, label="cost")
        # plt.bar(dates + w, d['rec'], w, label="rec")

        # Plot expected salary
        if not d.empty:
            x = d['salary'].iloc[0]
            plt.axhline(x, color='r', linestyle='--', label="expected")

        plt.xlabel('Date', color='r')
        plt.ylabel('Money', color='r')
        plt.xticks(dates + w / 2, d['date'].unique().astype('str').tolist())  # Set x-ticks
        plt.legend()
        plt.savefig('static/new.png')
        plt.close()

        return 1

def valid_login(uid):
    cur.execute('select * from exp_login where uid=%s',uid)
    f=cur.fetchall()
    print(f)
    if f:
        return "valid"
    else:
        return None
def valid(a):
        cur.execute('select * from exp_login where username=%s',(a))
        y=cur.fetchall()
        if y:
            return "User already exist. Try new email id"
        else:
            return None
