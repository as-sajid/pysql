
import pandas as pd
import cx_Oracle
import sys
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
lib_dir = r"C:\instantclient_19_13"
cx_Oracle.init_oracle_client(lib_dir=lib_dir)
try:
   engine = sqlalchemy.create_engine("oracle+cx_oracle://pysql:pysql@localhost:1521/?service_name=xepdb1", arraysize=1000)
   orders_sql = """SELECT ordate, empl, 
   sum(price*quantity*(1-discount/100)) AS total,
    sum(price*quantity*(discount/100)) AS off
    FROM orders INNER JOIN details 
    ON orders.pono = details.pono
    GROUP BY ordate, empl
    order by ordate""";
   df_orders = pd.read_sql(orders_sql, engine)
   print(df_orders);

except SQLAlchemyError as e:
   print(e)
sys.exit();
