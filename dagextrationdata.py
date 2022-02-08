from datetime import datetime, timedelta
from airflow import DAG
import config as config
from datetime import date
from airflow.models import DAG
from airflow.utils.dates import days_ago
import awswrangler as wr
from airflow.operators.python_operator import PythonOperator


def extract_load_data():
    print(f"Getting data from {config.BUCKET_RAW}...")
    raw_path = f"s3://{config.BUCKET_RAW}/"
    raw_df = wr.s3.read_csv(path=raw_path)
    print (raw_df)
    
    print(f"Writing data to {config.DB_NAME}...")
    
    raw_df.to_sql(
        name=config.TBL_NAME,
        con=config.engine,
        schema = "public",
        if_exists="replace",
        index=True,
    )
    print(f"Data written to {config.DB_NAME}")

DAG_DEFAULT_ARGS = {'owner': 'MG', 'depends_on_past': False, 'start_date': datetime.utcnow(), 'retries': 1, 'retry_delay': timedelta(minutes=5)}

with DAG(
    "extract_load_data",
    default_args=DAG_DEFAULT_ARGS,
    schedule_interval="0 3 * * *",
    catchup = False) as dag:

    from_s3_to_postgres = PythonOperator(task_id="extract_load_data", python_callable=extract_load_data,
    dag = dag
    )

from_s3_to_postgres
