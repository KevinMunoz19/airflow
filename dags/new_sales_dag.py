import os
from datetime import datetime

import pandas as pd
from airflow import DAG
from airflow.contrib.hooks.fs_hook import FSHook
from airflow.hooks.mysql_hook import MySqlHook
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from structlog import get_logger

COLUMNS = {
    "ORDERNUMBER": "order_number",
    "QUANTITYORDERED": "quantity_ordered",
    "PRICEEACH": "price_each",
    "ORDERLINENUMBER": "order_line_number",
    "SALES": "sales",
    "ORDERDATE": "order_date",
    "STATUS": "status",
    "QTR_ID": "qtr_id",
    "MONTH_ID": "month_id",
    "YEAR_ID": "year_id",
    "PRODUCTLINE": "product_line",
    "MSRP": "msrp",
    "PRODUCTCODE": "product_code",
    "CUSTOMERNAME": "customer_name",
    "PHONE": "phone",
    "ADDRESSLINE1": "address_line_1",
    "ADDRESSLINE2": "address_line_2",
    "CITY": "city",
    "STATE": "state",
    "POSTALCODE": "postal_code",
    "COUNTRY": "country",
    "TERRITORY": "territory",
    "CONTACTLASTNAME": "contact_last_name",
    "CONTACTFIRSTNAME": "contact_first_name",
    "DEALSIZE": "deal_size"
}

DATE_COLUMNS = ["ORDERDATE"]

logger = get_logger()

dag = DAG('new_sales_dag', description='A new approach for the sales dag',
          default_args={
              'owner': 'obed.espinoza',
              'depends_on_past': False,
              'max_active_runs': 1,
              'start_date': days_ago(5)
          },
          schedule_interval='0 1 * * *',
          catchup=False)


def process_file(**kwargs):
    logger.info(kwargs['execution_date'])
    file_path = f"{FSHook('fs_default').get_path()}/sales.csv"
    connection = MySqlHook('mysql_default').get_sqlalchemy_engine()
    df = (pd.read_csv(file_path, encoding="ISO-8859-1", parse_dates=DATE_COLUMNS).rename(columns=COLUMNS))
    logger.info(df)

    with connection.begin() as transaction:
        transaction.execute('Delete from test.sales where 1=1')
        df.to_sql('sales', con=transaction, schema='test', if_exists='append', index=False)

    logger.info(f'Records inserted {len(df.index)}')
    os.remove(file_path)

sensor = FileSensor(filepath='sales.csv',
                    fs_conn_id='fs_default',
                    task_id='check_for_file',
                    poke_interval=5,
                    timeout=60,
                    dag=dag
                    )

operador = PythonOperator(task_id='process_file',
                          dag=dag,
                          python_callable=process_file,
                          provide_context=True
)

sensor >> operador
