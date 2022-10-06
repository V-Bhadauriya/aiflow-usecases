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
    'kubernetes_sample', default_args=default_args,
    schedule_interval=timedelta(minutes=10), tags=['example', 'kubernetes', 'python', 'bash' ])


python_task = KubernetesPodOperator(namespace='default',
                                    image="python:3.6",
                                    cmds=["python", "-c"],
                                    arguments=[
                                        "print('{{ dag_run.conf.get("message") }}')"
                                    ],
                                    labels={"foo": "bar"},
                                    name="loadfile",
                                    task_id="passing-task-python",
                                    get_logs=True,
                                    dag=dag
                                    )
