"""BashOperator Test DAG.
This is a Test.
"""

from datetime import timedelta
from pathlib import Path

import pendulum
from airflow import DAG, models, settings
from airflow.models.param import Param, ParamsDict
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from common.callback import success_callback, failure_callback


default_args = {
    "owner": "ceuity",
    "depends_on_past": False,
    "wait_for_downstream": False,
    "start_date": pendulum.today("Asia/Seoul").add(days=-1),
    "email": ["everland7942@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    # "queue": "testing_queue",
    # 'retries': 1,
    # 'retry_delay': timedelta(minutes=5),
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # "on_success_callback": success_callback,
    "on_failure_callback": failure_callback,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    "trigger_rule": "all_success",
}


dag = DAG(
    dag_id=Path(__file__).stem,
    description=__doc__.partition(".")[0],
    doc_md=__doc__,
    schedule=None,
    catchup=False,
    # params=params,
    default_args=default_args,
)

task1 = BashOperator(
    task_id="task1",
    bash_command="date",
    dag=dag,
)

task3 = BashOperator(
    task_id="task3",
    bash_command="""
        {% for i in range(5) %}
            echo "{{ ds }}"
            echo "{{ macros.ds_add(ds, 7)}}"
            echo "{{ params.my_param }}"
        {% endfor %}
        """,
    params={"my_param": "Parameter I passed in"},
    dag=dag,
    on_success_callback=success_callback,
)


task1 >> task3
