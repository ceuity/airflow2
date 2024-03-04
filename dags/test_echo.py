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
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}


params = {
    "integer": Param(type="integer"),
}

dag = DAG(
    dag_id=Path(__file__).stem,
    description=__doc__.partition(".")[0],
    doc_md=__doc__,
    schedule=None,
    catchup=False,
    params=params,
    default_args=default_args,
)

task1 = BashOperator(
    task_id="task1",
    bash_command="date",
    dag=dag,
)

task2 = BashOperator(
    task_id="task2",
    bash_command="""
        echo {{ params }};
        {% for i in range(30) %}
            date
            sleep 1
        {% endfor %}
        """,
    dag=dag,
)

task1 >> task2
