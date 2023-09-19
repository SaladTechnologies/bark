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