from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from speech_to_text import stream_transcribe
import asyncio

app = FastAPI(title="Streaming Speech-to-Text API")

@app.get("/")
def root():
    return {"message": "Streaming Speech-to-Text API is running!"}

@app.websocket("/ws/transcribe")
async def websocket_transcribe(websocket: WebSocket):
    """
    WebSocket endpoint for real-time speech-to-text transcription.
    Clients should send raw audio chunks (LINEAR16 PCM, 16kHz, mono) as binary messages.
    The server streams transcripts back as JSON messages.
    """
    await websocket.accept()
    transcriber = stream_transcribe()
    next(transcriber)  # Prime the generator
    try:
        while True:
            data = await websocket.receive_bytes()
            # Send audio chunk to the generator and get all available transcripts
            while True:
                try:
                    result = transcriber.send(data)
                    if result:
                        await websocket.send_json({"transcript": result})
                    else:
                        break
                except StopIteration:
                    break
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({"error": str(e)})
    finally:
        transcriber.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 