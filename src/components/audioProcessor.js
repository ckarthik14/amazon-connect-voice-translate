import React, { useState, useEffect } from 'react';
import AWS from 'aws-sdk';

const AudioProcessor = ({ streamName, region }) => {
    const [audioUrl, setAudioUrl] = useState('');

    useEffect(() => {
        // Configure AWS
        AWS.config.update({
            region: region,
            credentials: new AWS.CognitoIdentityCredentials({
                IdentityPoolId: 'YOUR_IDENTITY_POOL_ID', // Replace with your Cognito Identity Pool ID
            })
        });

        const kinesis = new AWS.Kinesis({ apiVersion: '2013-12-02' });

        const fetchShardIterator = async () => {
            try {
                const streamData = await kinesis.describeStream({ StreamName: streamName }).promise();
                const shardId = streamData.StreamDescription.Shards[0].ShardId;

                const shardIteratorData = await kinesis.getShardIterator({
                    StreamName: streamName,
                    ShardId: shardId,
                    ShardIteratorType: 'TRIM_HORIZON' // Start reading from the earliest record
                }).promise();

                return shardIteratorData.ShardIterator;
            } catch (error) {
                console.error('Error fetching shard iterator:', error);
            }
        };

        const getRecords = async (shardIterator) => {
            try {
                const recordsData = await kinesis.getRecords({ ShardIterator: shardIterator }).promise();
                if (recordsData && recordsData.Records.length > 0) {
                    recordsData.Records.forEach(record => {
                        const audioBlob = b64ToBlob(atob(record.Data), 'audio/mp3');
                        const newAudioUrl = URL.createObjectURL(audioBlob);
                        setAudioUrl(newAudioUrl);
                    });
                }
                setTimeout(() => getRecords(recordsData.NextShardIterator), 5000); // Continue polling
            } catch (error) {
                console.error('Error fetching records:', error);
            }
        };

        fetchShardIterator().then(shardIterator => {
            if (shardIterator) {
                getRecords(shardIterator);
            }
        });

    }, [streamName, region]);

    const b64ToBlob = (b64Data, contentType = 'audio/mp3', sliceSize = 512) => {
        const byteCharacters = atob(b64Data);
        const byteArrays = [];

        for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
            const slice = byteCharacters.slice(offset, offset + sliceSize);
            const byteNumbers = new Array(slice.length);
            for (let i = 0; i < slice.length; i++) {
                byteNumbers[i] = slice.charCodeAt(i);
            }
            const byteArray = new Uint8Array(byteNumbers);
            byteArrays.push(byteArray);
        }

        const blob = new Blob(byteArrays, {type: contentType});
        return blob;
    };

    return (
        <div>
            <h1>Kinesis Audio Stream</h1>
            {audioUrl && <audio src={audioUrl} controls autoPlay />}
        </div>
    );
};

export default AudioProcessor;
