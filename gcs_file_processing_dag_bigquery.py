from airflow import DAG
from airflow.providers.google.cloud.operators.gcs import GCSDownloadObjectOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyTableOperator, BigQueryInsertJobOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.utils.dates import days_ago
from airflow.operators.dummy_operator import DummyOperator

# Define the DAG
with DAG(
        'gcs_to_bigquery',
        default_args={
            'owner': 'airflow',
            'retries': 1,
        },
        description='A DAG to load data from GCS to BigQuery',
        schedule_interval='@daily',  # Can be adjusted to your schedule
        start_date=days_ago(1),
        catchup=False,
) as dag:

    start = DummyOperator(task_id='start')

    # Task 1: Download file from GCS
    download_file = GCSDownloadObjectOperator(
        task_id='download_file_from_gcs',
        bucket_name='your-gcs-bucket-name',
        object_name='your-file-name.csv',  # Example file name
        filename='/tmp/your-file-name.csv',  # Local file path in Airflow worker
    )

    # Task 2: Create BigQuery table (if it doesn't exist)
    create_bq_table = BigQueryCreateEmptyTableOperator(
        task_id='create_bq_table',
        dataset_id='your-bigquery-dataset',
        table_id='your-table-name',
        schema_fields=[
            {'name': 'column1', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'column2', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            # Define more columns as per your data
        ],
        project_id='your-gcp-project-id',
    )

    # Task 3: Load data from GCS into BigQuery
    load_data_to_bq = BigQueryInsertJobOperator(
        task_id='load_data_to_bigquery',
        configuration={
            "load": {
                "sourceUris": ["gs://your-gcs-bucket-name/your-file-name.csv"],
                "destinationTable": {
                    "projectId": "your-gcp-project-id",
                    "datasetId": "your-bigquery-dataset",
                    "tableId": "your-table-name",
                },
                "schema": {
                    "fields": [
                        {"name": "column1", "type": "STRING"},
                        {"name": "column2", "type": "INTEGER"},
                        # Define more columns
                    ]
                },
                "skipLeadingRows": 1,  # Skip header row (if applicable)
                "sourceFormat": "CSV",  # Adjust format if needed (e.g., JSON, Avro)
            }
        },
        project_id='your-gcp-project-id',
    )

    # Set task dependencies
    start >> download_file >> create_bq_table >> load_data_to_bq
