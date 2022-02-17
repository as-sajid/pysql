
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
   print(df_orders) 
   print(df_details) 
except SQLAlchemyError as e:
   print(e)