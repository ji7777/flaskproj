import snowflake.connector,os
con=snowflake.connector.connect(user=os.get_env('user')
password=os.get_env('password')
account=os.get_env('account')
warehouse=os.get_env('warehouse')
database=os.get_env('database')
schema=os.get_env('schema'))

print(os.environ('user'))