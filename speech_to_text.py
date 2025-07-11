import os
import queue
import threading
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import StreamingRecognizeRequest, StreamingRecognitionConfig, RecognitionConfig
import gzip, json

# Ensure credentials are set
if os.path.exists('key.json'):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.abspath('key.json')


def stream_transcribe(language_code="en-US", sample_rate=16000):
    """
    Generator for real-time streaming transcription using Google Cloud Speech-to-Text API.
    Yields partial/final transcripts as audio chunks are sent in.
    """
    client = speech.SpeechClient()
    requests_queue = queue.Queue()
    responses_queue = queue.Queue()
    stop_event = threading.Event()
    final_transcripts = []

    def request_generator():
        while not stop_event.is_set():
            try:
                chunk = requests_queue.get(timeout=0.1)
                if chunk is None:
                    break
                yield StreamingRecognizeRequest(audio_content=chunk)
            except queue.Empty:
                continue

    def response_worker():
        try:
            config = StreamingRecognitionConfig(
                config=RecognitionConfig(
                    encoding=RecognitionConfig.AudioEncoding.LINEAR16,
                    sample_rate_hertz=sample_rate,
                    language_code=language_code,
                    enable_automatic_punctuation=True,
                    enable_word_time_offsets=False,
                    enable_word_confidence=True,
                    model="latest_long",
                    use_enhanced=True
                ),
                interim_results=True,
                single_utterance=False
            )
            for response in client.streaming_recognize(config=config, requests=request_generator()):
                for result in response.results:
                    if result.is_final:
                        transcript = result.alternatives[0].transcript
                        responses_queue.put(transcript)
                        final_transcripts.append(transcript)
        except Exception as e:
            responses_queue.put(f"[ERROR] {str(e)}")
        finally:
            responses_queue.put(None)

    # Start the response worker thread
    thread = threading.Thread(target=response_worker, daemon=True)
    thread.start()

    try:
        while True:
            # Receive audio chunk from caller
            chunk = (yield)
            requests_queue.put(chunk)
            # Check for new transcript
            while not responses_queue.empty():
                transcript = responses_queue.get()
                if transcript is None:
                    return
                yield transcript
    finally:
        stop_event.set()
        requests_queue.put(None)
        with open('transcripts.json', 'w', encoding='utf-8') as f_plain:
            json.dump(final_transcripts, f_plain, ensure_ascii=False, indent=2)
        with gzip.open('transcripts.json.gz', 'wt', encoding='utf-8') as f_gz:
            json.dump(final_transcripts, f_gz)
        thread.join() 