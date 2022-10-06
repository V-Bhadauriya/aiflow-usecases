import logging

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import \
    KubernetesPodOperator
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

start = DummyOperator(task_id='run_this_first', dag=dag)


def run_this_func(**context):
    """
    Print the payload "message" passed to the DagRun conf attribute.
    :param context: The execution context
    :type context: dict
    """
    print("context", context)
    print("Remotely received value of {} for key=message".format(context["dag_run"].conf["message"]))

#PythonOperator usage
run_this = PythonOperator(task_id="run_this", python_callable=run_this_func, dag=dag, provide_context=True)


python_task = KubernetesPodOperator(namespace='default',
                                    image="python:3.6",
                                    cmds=["python", "-c"],
                                    arguments=["print('hello world')"],
                                    labels={"foo": "bar"},
                                    name="passing-python",
                                    task_id="passing-task-python",
                                    get_logs=True,
                                    dag=dag
                                    )

bash_task = KubernetesPodOperator(namespace='default',
                                  image="ubuntu:16.04",
                                  cmds=["bash", "-cx"],
                                  arguments=["date"],
                                  labels={"foo": "bar"},
                                  name="passing-bash",
                                  # is_delete_operator_pod=False,
                                  task_id="passing-task-bash",
                                  get_logs=True,
                                  dag=dag
                                  )

python_task.set_upstream(start)
bash_task.set_upstream(start)
