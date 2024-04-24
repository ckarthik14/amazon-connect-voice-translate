import React, { useState } from 'react';
import AWS from 'aws-sdk';

const App = () => {
  const [isFetching, setIsFetching] = useState(false);

  const fetchAudioAndPlay = () => {
    setIsFetching(true);

    // Initialize AWS SDK
    AWS.config.update({
      accessKeyId: 'YOUR_ACCESS_KEY_ID',
      secretAccessKey: 'YOUR_SECRET_ACCESS_KEY',
      region: 'YOUR_AWS_REGION',
    });

    const s3 = new AWS.S3();
    const kinesis = new AWS.Kinesis();

    // Fetch audio file from S3
    const params = {
      Bucket: 'YOUR_S3_BUCKET_NAME',
      Key: 'path/to/audio/file.mp3', // Change this to the path of your audio file in S3
    };

    s3.getObject(params, (err, data) => {
      if (err) {
        console.error('Error fetching audio file from S3:', err);
        setIsFetching(false);
        return;
      }

      const audioBuffer = data.Body;

      // Create an audio element dynamically
      const audio = new Audio(URL.createObjectURL(new Blob([audioBuffer])));

      // Autoplay the audio
      audio.play().catch(err => {
        console.error('Error playing audio:', err);
      });

      // Send audio data to Kinesis
      const putParams = {
        Data: audioBuffer,
        PartitionKey: '1', // Change this as needed to partition your data
        StreamName: 'YOUR_KINESIS_STREAM_NAME',
      };

      kinesis.putRecord(putParams, (err, data) => {
        if (err) {
          console.error('Error putting record to Kinesis:', err);
          return;
        }
        console.log('Record put to Kinesis:', data);
      });
    });
  };

  return (
    <div>
      <button onClick={fetchAudioAndPlay} disabled={isFetching}>
        {isFetching ? 'Fetching Audio...' : 'Fetch and Play Audio'}
      </button>
    </div>
  );
};

export default App;