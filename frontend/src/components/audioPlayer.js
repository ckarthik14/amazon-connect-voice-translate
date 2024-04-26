import React, { useEffect, useState, useRef} from 'react';

const AudioPlayer = ({ wsUrl }) => {
  const [audioUrl, setAudioUrl] = useState('');
  const audioRef = useRef(null);

  useEffect(() => {
    const socket = new WebSocket(wsUrl);

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const audioBlob = new Blob([data.audio_data], { type: 'audio/mp3' });
      const url = URL.createObjectURL(audioBlob);
      setAudioUrl(url);
    };

    // audioRef.current.muted = false; // Apply the muted state to the audio element
    // audioRef.current.play(); // Play the audio

    return () => socket.close();
  }, [wsUrl]);

  return (
    <div>
      {/* <audio src={audioUrl} ref={audioRef} controls autoPlay /> */}
      <p>Streaming Audio</p>
    </div>
  );
};

export default AudioPlayer;
