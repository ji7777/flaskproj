import snowflake.connector,os
from dotenv import load_dotenv
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