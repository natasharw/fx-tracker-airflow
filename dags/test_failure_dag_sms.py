from datetime import datetime
from airflow import DAG

from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator

from airflow.operators.alphavantage_plugin import VonageSmsOperator


def vonage_sms_alert(context):

    operator = VonageSmsOperator(
        task_id=str(context['task_instance_key_str']),
        vonage_api_conn_id='vonage_api_conn_id',
        recipients=['447384700374'],
        message=f"""! Airflow alert !
        A task has failed
        DAG: {context['task_instance'].dag_id}
        Task: {context['task_instance'].task_id}
        Exception: {context['exception']}"""
    )

    return operator.execute()

dag = DAG('test_failure_dag_sms',
          schedule_interval=None,
          start_date=datetime(2020, 10, 11), catchup=False)

dag_start = DummyOperator(task_id='dag_start', dag=dag)

test_sms_alert_task = BashOperator(
    task_id='test_sms_alert_task',
    bash_command='exit 1',
    on_failure_callback=vonage_sms_alert,
    provide_context=True,
    dag=dag,
)

dag_start >> test_sms_alert_task
