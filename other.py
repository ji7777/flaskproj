import snowflake.connector,os
con=snowflake.connector.connect(user=os.environ.get('user'),
password=os.environ.get('password'),
account=os.environ.get('account'),
warehouse=os.environ.get('warehouse'),
database=os.environ.get('database'),
schema=os.environ.get('schema'))

print(os.environ.get('user'))