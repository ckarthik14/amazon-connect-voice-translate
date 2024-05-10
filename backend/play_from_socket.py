import websocket
import pyaudio
import threading
import base64
import json
from pydub import AudioSegment
from pydub.playback import play
import io

def on_message(ws, message):
    # Assuming the message is audio data
    # Convert bytes data to audio format if necessary, here assuming it's already in correct format
    audio = json.loads(message)["audio_data"]
    decoded_message = base64.b64decode(audio)
    
    audio = AudioSegment.from_file(io.BytesIO(decoded_message), format="mp3")
    # Convert to raw audio data bytes for PyAudio
    print("Sample width:", audio.sample_width)
    print("Channels:", audio.channels)
    print("Frame Rate", audio.frame_rate)

    raw_data = audio.raw_data
    frames.append(raw_data)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_reason):
    print("WebSocket closed with status {0} and reason: {1}".format(close_status_code, close_reason))

def on_open(ws):
    def run(*args):
        # Here you could send a message that you're ready to receive data, or handle any handshake
        print("WebSocket opened and ready to receive data")
    thread = threading.Thread(target=run)
    thread.start()

# Setup PyAudio
p = pyaudio.PyAudio()
frames_per_buffer = 1024  # Adjust this value to your specific needs

# Make sure to match the parameters with those of the audio format
stream = p.open(format=p.get_format_from_width(2),
                channels=1,
                rate=22050,
                output=True,
                frames_per_buffer=frames_per_buffer)

frames = []  # Shared list to hold the audio frames coming from the websocket


# Setup WebSocket
# websocket.enableTrace(True)
ws = websocket.WebSocketApp("wss://qv1241nc27.execute-api.us-east-1.amazonaws.com/dev/",
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
ws.on_open = on_open

# Start WebSocket in a thread
wst = threading.Thread(target=ws.run_forever)
wst.start()

try:
    while True:
        if frames:
            frame = frames.pop(0)
            stream.write(frame)
except KeyboardInterrupt:
    ws.close()
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Program exited gracefully")
