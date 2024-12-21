from airflow import DAG
from airflow.providers.google.cloud.operators.pubsub import PubSubPullOperator
from airflow.providers.google.cloud.operators.gcs import GCSDownloadObjectOperator
from airflow.utils.dates import days_ago
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.google.cloud.hooks.pubsub import PubSubHook

def process_pubsub_message(message, **kwargs):
    """
    This function will be called to process the message from Pub/Sub
    and then download the file from GCS.
    """
    bucket_name = message['bucketName']
    file_name = message['fileName']

    # Use GCS operator to download the file
    download_file = GCSDownloadObjectOperator(
        task_id=f'download_{file_name}',
        bucket_name=bucket_name,
        object_name=file_name,
        filename=f'/tmp/{file_name}',
    )
    download_file.execute(context=kwargs)
    print(f"File {file_name} downloaded and processed.")

with DAG(
        'gcs_file_processing_with_pubsub',
        default_args={
            'owner': 'airflow',
            'retries': 1,
        },
        description='Process files uploaded to GCS with Pub/Sub and Airflow',
        schedule_interval=None,  # Triggered by Pub/Sub, no need for a schedule
        start_date=days_ago(1),
        catchup=False,
) as dag:

    start = DummyOperator(task_id='start')

    # Pull the Pub/Sub messages
    pull_pubsub_messages = PubSubPullOperator(
        task_id='pull_pubsub_messages',
        project_id='<your-project-id>',
        subscription_id='<your-subscription-id>',
        max_messages=1,  # Pull 1 message at a time
        ack_messages=True
    )

    # Process the messages and download the file from GCS
    process_file = PythonOperator(
        task_id='process_file_from_pubsub',
        python_callable=process_pubsub_message,
        op_args=["{{ task_instance.xcom_pull(task_ids='pull_pubsub_messages') }}"],
        provide_context=True,
    )

    start >> pull_pubsub_messages >> process_file
