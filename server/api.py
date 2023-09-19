from model import load
import soundfile as sf
from pydub import AudioSegment
import numpy as np
from io import BytesIO
import time
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from typing import Optional
from pydantic import BaseModel
import uvicorn
import os

host = os.getenv("HOST", "127.0.0.1")
port = os.getenv("PORT", "8000")

port = int(port)


def predict(processor, model, text, voice_preset=None):
    inputs = processor(text, voice_preset=voice_preset, return_tensors="pt")
    inputs = {k: v.to("cuda") for k, v in inputs.items()}
    speech_values = model.generate(**inputs, do_sample=True)

    sampling_rate = model.generation_config.sample_rate
    speech = speech_values.cpu().numpy().squeeze()
    scaled_speech = np.int16(speech * 32767)

    wav = BytesIO()
    sf.write(wav, scaled_speech, sampling_rate, format="WAV", subtype="PCM_16")

    audio = AudioSegment.from_wav(wav)
    dur_ms = len(audio)

    mp3 = BytesIO()
    audio.export(mp3, format="mp3")

    return mp3, dur_ms


class GenerateRequest(BaseModel):
    # Add your input parameters here
    text: str
    voice_preset: Optional[str] = None


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/hc")
async def health_check():
    return "OK"


@app.post("/generate", response_class=StreamingResponse)
def generate(req: GenerateRequest = Body(...)):
    try:
        mp3, dur_ms = predict(processor, model, req.text, req.voice_preset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return StreamingResponse(mp3, media_type="audio/mpeg")


if __name__ == "__main__":
    print("Loading model...")
    start = time.perf_counter()
    processor, model = load()
    end = time.perf_counter()
    print(f"Model loaded in {end - start:.2f}s")

    print("Generating test audio...")
    start = time.perf_counter()
    test_text = "Hello, my name is Suno and I like to Bark!"
    mp3, dur_ms = predict(processor, model, test_text)
    end = time.perf_counter()
    print(f"Test audio ({dur_ms / 1000:.2f}s) generated in {end - start:.2f}s")
    uvicorn.run(app, host=host, port=port)
