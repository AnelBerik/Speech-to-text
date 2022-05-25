from google.cloud import speech
import json
import io

from google.cloud import storage
import os

def transcribe(path, locale):
    client = speech.SpeechClient()

    with io.open(path, "rb") as audio_file:
        content = audio_file.read()

    storage_path = 'video.wav'
    storage_client = storage.Client(project="august-impact-350608")
    bucket = storage_client.get_bucket('anel')
    blob = bucket.blob(storage_path)
    blob.upload_from_filename(path)
    print("uploaded")

    uri = "gs://anel/video.wav"

    audio = speech.RecognitionAudio(uri=uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=locale,
        enable_automatic_punctuation=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    response = operation.result(timeout=300)

    text = ""
    confidence = 0
    index = 0

    for result in response.results:
        # The first alternative is the most likely one for this portion.
        text += result.alternatives[0].transcript + " "
        confidence += result.alternatives[0].confidence
    return text, confidence
