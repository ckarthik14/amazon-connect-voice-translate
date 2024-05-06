import React, { useEffect, useState, useRef } from 'react';

const AudioPlayer = (wsUrl) => {
  const [isReadyToPlay, setIsReadyToPlay] = useState(false);
  const audioContextRef = useRef(null);
  const nextTimeRef = useRef(0);

  const openSocket = async () => {
    const socket = new WebSocket(wsUrl);
    
    // Initialize the AudioContext when the component mounts
    audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();

    socket.onmessage = async (event) => {
      console.log('CDEBUG: Message from server ', event.data);

      const data = JSON.parse(event.data);

      console.log('CDEBUG: Encoded Data', data.audio_data);

      const binaryString = window.atob(data.audio_data);
      
      console.log('CDEBUG: Decoded Audio', binaryString);

      const len = binaryString.length;
      const bytes = new Uint8Array(len);
      for (let i = 0; i < len; i++) {
        bytes[i] = binaryString.charCodeAt(i);
      }

      // Decode the audio data and play it
      if (audioContextRef.current) {
        const audioBuffer = await audioContextRef.current.decodeAudioData(bytes.buffer);
        playAudio(audioBuffer);
      }
    };

    socket.onopen = () => {
      console.log('CDEBUG: WebSocket Connected');
    };

    socket.onerror = (error) => {
      console.error('CDEBUG: WebSocket Error: ', error);
    };

    socket.onclose = (event) => {
      console.log('CDEBUG: WebSocket Disconnected: ', event);
    };

    return () => {
      socket.close();
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }
    };
  };

  const playAudio = (audioBuffer) => {
    const source = audioContextRef.current.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(audioContextRef.current.destination);
    const currentTime = audioContextRef.current.currentTime;
    const nextTime = nextTimeRef.current > currentTime ? nextTimeRef.current : currentTime;
    source.start(nextTime);
    nextTimeRef.current = nextTime + audioBuffer.duration;
  };

  return { openSocket }

  // return (
  //   <div>
  //     <div onClick={handleUserInteraction}>
  //       <p>Click anywhere to enable audio and start streaming</p>
  //     </div>
  //   </div>
  // );
};

export default AudioPlayer;
