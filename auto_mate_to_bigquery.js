const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

exports.gcsToBigQuery = async (event, context) => {
    const fileName = event.name;
    const bucketName = event.bucket;

    // Specify the BigQuery dataset and table to load data into
    const dataset = 'your-bigquery-dataset';
    const table = 'your-bigquery-table';

    // Construct the URI for the GCS file
    const gcsUri = `gs://${bucketName}/${fileName}`;

    // Set metadata for loading the TXT file into BigQuery
    const metadata = {
        sourceFormat: 'CSV', // BigQuery treats TXT files as CSV format
        skipLeadingRows: 1,  // Skip the header row, if applicable
        fieldDelimiter: '\t', // Assuming the file is tab-delimited
        encoding: 'UTF-8',    // Ensure the correct encoding
    };

    // Load the file from GCS into BigQuery
    await bigquery
        .dataset(dataset)
        .table(table)
        .load(gcsUri, metadata)
        .then(() => {
            console.log(`Successfully loaded ${fileName} from GCS to BigQuery.`);
        })
        .catch(err => {
            console.error('Error loading data into BigQuery:', err);
        });
};
