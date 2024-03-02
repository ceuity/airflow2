"""KubernetesPodOperator example DAG.
This example DAG demonstrates how to use the KubernetesPodOperator to launch a simple Docker container.
"""

import logging
import os
import sys
from distutils.util import strtobool
from pathlib import Path

import pendulum
from airflow.models.param import Param
from airflow import DAG, AirflowException
from airflow.operators.bash import BashOperator
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.providers.cncf.kubernetes.secret import Secret
from kubernetes.client import models as k8s

logger = logging.getLogger("airflow.task")
image = "python:3.11.8-bookworm"
in_cluster = bool(strtobool(os.environ.get("KPO_CLUSTER_FLAG", "False")))
config_file = os.environ.get("KPO_CONFIG_PATH", "/home/airflow/.kube/config")


default_args = {
    "owner": "ceuity",
    "depends_on_past": True,
    "wait_for_downstream": True,
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

# aws_credential = Secret('volume', '/root/.aws', 'aws-k8s-userspace')
# google_service_account_key = Secret('volume', '/root/.google', 'airflow-secret-google')
# github_ssh_key = Secret('volume', '/root/ssh', 'airflow-secret-gitkey')

task1 = BashOperator(
    task_id="task1",
    bash_command="echo k8s test && date",
    dag=dag,
)

task2 = KubernetesPodOperator(
    dag=dag,
    task_id="task2",
    name="k8s-test-dag",
    namespace="research",
    image_pull_policy="IfNotPresent",  # Always
    image=image,
    labels={"app": "airflow-app-k8s-test"},
    startup_timeout_seconds=1800,
    cmds=["/bin/sh", "-c"],
    arguments=["echo $HOME; " "echo {{ ds }} && " "sleep infinity"],
    env_vars={
        "PYTHONUNBUFFERED": "1",
    },  # 스크립트 실행시, python 차원에서 로깅을 뱉지않는현상 해결.
    container_resources=k8s.V1ResourceRequirements(
        requests={"cpu": "1", "memory": "1Gi"},
        limits={"cpu": "1", "memory": "1Gi"},
    ),
    # secrets=[aws_credential, google_service_account_key, github_ssh_key],
    # volumes=volumes,
    # volume_mounts=volume_mounts,
    in_cluster=in_cluster,
    config_file=config_file,
    is_delete_operator_pod=True,
    get_logs=True,
)
task2.template_fields = ["image", "cmds", "arguments", "env_vars", "config_file"]  # 'pod_template_file'


task1 >> task2
