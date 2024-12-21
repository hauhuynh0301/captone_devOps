const { PubSub } = require('@google-cloud/pubsub');
const pubSubClient = new PubSub();

exports.gcsUploadTrigger = async (event, context) => {
    const fileName = event.name;
    const bucketName = event.bucket;

    const message = {
        fileName,
        bucketName,
    };

    const topicName = 'gcs-file-uploaded';
    const dataBuffer = Buffer.from(JSON.stringify(message));

    // Publish to Pub/Sub
    await pubSubClient.topic(topicName).publish(dataBuffer);

    console.log(`Published message to Pub/Sub topic: ${topicName}`);
};
