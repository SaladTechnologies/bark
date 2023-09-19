# bark
An inference server for Bark

## Build

```bash
docker buildx build \
-t saladtechnologies/bark:latest \
--provenance=false \
--output type=docker \
.
```

## Run

```bash
docker run --rm \
--gpus all \
-p 8000:8000 \
-e HOST="0.0.0.0" \
-e PORT="8000" \
saladtechnologies/bark:latest
```

## Test

```bash
curl  -X POST \
  'http://localhost:8000/generate' \
  --header 'Accept: */*' \
  --header 'User-Agent: Thunder Client (https://www.thunderclient.com)' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "text": "My name is Suno, and uh - I am an artificial intelligence that generates sound from text. Can you tell, or do I sound human?",
  "voice_preset": "v2/en_speaker_0"
}' -o outputs/sample.mp3
```