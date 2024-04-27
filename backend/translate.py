import boto3
from pydub import AudioSegment
from pydub.playback import play
from base64 import b64encode, b64decode
import io

def translate_text(text, source_lang='en', target_lang='hi'):
    # Initialize AWS Translate Client
    translate_client = boto3.client('translate')
    result = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_lang,
        TargetLanguageCode=target_lang
    )

    return result['TranslatedText']

def synthesize_speech(text='Hello, world!', voice='Aditi', language_code='hi-IN'):
    # First, translate the text from English to Hindi
    translated_text = translate_text(text)
    print("Hindi: ", "\u0920\u0940\u0915 \u0939\u0948?")

    # Initialize a boto3 client for Polly
    polly_client = boto3.client('polly')

    # Request speech synthesis in Hindi
    response = polly_client.synthesize_speech(
        Text="\u0920\u0940\u0915 \u0939\u0948?",
        OutputFormat='mp3',
        VoiceId=voice,
        LanguageCode=language_code
    )

    # Access the audio stream from the response
    if "AudioStream" in response:
        audio_stream = response['AudioStream'].read()
        # print("Audio bytes: ", audio_stream)

        encoded_audio = b64encode(audio_stream).decode('utf-8')
        # print("Encoded audio: ", encoded_audio)

        decoded_audio = b64decode(encoded_audio)
        # print("Decoded audio: ", decoded_audio)

        # Use pydub to play the audio data
        song = AudioSegment.from_file(io.BytesIO(decoded_audio), format="mp3")
        play(song)
    else:
        print("Could not stream audio")
        return None

# Example usage
synthesize_speech("Hello, this is a test of AWS Translate and Polly!", "Aditi")
