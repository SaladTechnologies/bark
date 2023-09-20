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

See the list of voice preset options: https://suno-ai.notion.site/8b8e8749ed514b0cbf3f699013548683?v=bc67cff786b04b50b3ceb756fd05f68c

```bash
curl  -X POST \
  'http://localhost:8000/generate' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "text": "My name is Suno, and uh - I am an artificial intelligence that generates sound from text. Can you tell, or do I sound human?",
  "voice_preset": "v2/en_speaker_4"
}' -o outputs/sample.mp3
```