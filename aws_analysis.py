import logging

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

# log = logging.getLogger(__name__)


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.utcnow(),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'aws_analysis', default_args=default_args,
    schedule_interval=timedelta(minutes=10), tags=['example', 'kubernetes', 'python', 'bash' ])


do_task = KubernetesPodOperator(
    namespace='default',
    image="python:3.6",
    cmds=["python", "/opt/aws-cost-analysis.py"],
    labels={"Name": "aws-cost-analysis" },
    name="aws-cost-analysis",
    task_id="aws-cost-analysis-task",
    env_vars= {
        "BUCKET": '{{ dag_run.conf.get("BUCKET") }}',
        "AWS_ACCESS_KEY_ID": '{{ dag_run.conf.get("AWS_ACCESS_KEY_ID") }}',
        "AWS_SECRET_ACCESS_KEY": '{{ dag_run.conf.get("AWS_SECRET_ACCESS_KEY") }}',
        "POSTGRES_HOST": '{{ dag_run.conf.get("POSTGRES_HOST") }}',
        "POSTGRES_PORT": '{{ dag_run.conf.get("POSTGRES_PORT") }}',
        "POSTGRES_DB": '{{ dag_run.conf.get("POSTGRES_DB") }}',
        "POSTGRES_USER": '{{ dag_run.conf.get("POSTGRES_USER") }}',
        "POSTGRES_PASSWORD": '{{ dag_run.conf.get("POSTGRES_PASSWORD") }}',
    },
    get_logs=True,
    dag=dag
)
