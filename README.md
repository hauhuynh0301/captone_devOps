1. install helm chart airflow
# Add the Apache Airflow Helm chart repository
helm repo add apache-airflow https://airflow.apache.org

# Install Apache Airflow in the 'airflow' namespace, creating the namespace if it doesn't exist
helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace

2. Setup Google Cloud Credentials for Airflow
    Create a Google Cloud Service Account:
    Go to the Google Cloud Console.
    Create a service account with Storage Object Viewer (at minimum) permissions on the bucket you're working with.
    Download the service account key JSON file.
    Create a Kubernetes Secret to store the service account credentials: Assuming you have the JSON file gcs-service-account-key.json for your service account:
# bash shell
    kubectl create secret generic airflow-gcs-credentials \
    --from-file=key.json=/path/to/gcs-service-account-key.json \
    --namespace airflow

3. upgrade the Helm release
# update Apache Airflow in the 'airflow' namespace, creating the namespace if it doesn't exist
helm upgrade --install airflow apache-airflow/airflow --namespace airflow --values values.yaml
#4. Create an Airflow DAG to Iterate Over Files in Google Cloud Storage

4. Set Up a Google Cloud Storage Bucket
# bash shell
    gsutil mb gs://your-bucket-name/
4. 1. Create a Pub/Sub Topic
# bash shell 
    gcloud pubsub topics create gcs-file-uploaded
4. 2. Create a Cloud Function to Publish to Pub/Sub:
      index.js
4. 3. Deploy the Cloud Function:
# bash shell
      gcloud functions deploy gcsUploadTrigger \
      --runtime nodejs18 \
      --trigger-resource gs://your-bucket-name \
      --trigger-event google.storage.object.finalize \
      --region us-central1
5. create a DAG in Airflow to Listen to Pub/Sub or Use GCS Operators
   gcs_file_processing_dag.py
5. 1. Configure Airflow to Authenticate with BigQuery
   Create a Google Cloud Service Account for BigQuery Access
step 1 : In the Google Cloud Console, create a Service Account with the necessary roles for BigQuery access:
step 2 : BigQuery Data Editor or BigQuery Admin (depending on your needs).
step 3 : Download the JSON key file for the service account.


5. 2. Store the Key in Kubernetes as a Secret
    Assuming you have downloaded the service account key JSON as bigquery-service-account-key.json, create a Kubernetes secret for this key:
# bash shell
    kubectl create secret generic airflow-bigquery-credentials \
      --from-file=key1.json=/path/to/bigquery-service-account-key.json \
      --namespace airflow

    helm upgrade --install airflow apache-airflow/airflow --namespace airflow --values values.yaml








