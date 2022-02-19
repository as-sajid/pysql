
import pandas as pd
import cx_Oracle
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
lib_dir = r"C:\instantclient_19_13"
cx_Oracle.init_oracle_client(lib_dir=lib_dir)
try:
   engine = sqlalchemy.create_engine("oracle+cx_oracle://pysql:pysql@localhost:1521/?service_name=xepdb1", arraysize=1000)
 
   orders_sql = """SELECT * FROM orders"""; 
   df_orders = pd.read_sql(orders_sql, engine)
   details_sql = """SELECT * FROM details""";
   df_details = pd.read_sql(details_sql, engine)
   #print(df_orders) 
   #print(df_details) 

   ''' merge the data frames with common column'''
   df_orders_details = df_orders.merge(df_details)
   #Adding column for total sales
   df_orders_details['total'] = df_orders_details.price * df_orders_details.quantity * (1 - df_orders_details.discount/100)
   #Calculating discount
   df_orders_details['off'] = df_orders_details.price * df_orders_details.quantity * (df_orders_details.discount/100)
   #calcylating sales
   df_sales = df_orders_details[['ordate','empl', 'total', 'off']]
   ##Rounding off
   df_orders_details = df_orders_details.round(2)
   print(df_sales)
   ###using group by
   df_date_empl = df_sales.groupby(['ordate','empl']).sum()
   print(df_date_empl)
except SQLAlchemyError as e:
   print(e)