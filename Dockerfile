FROM python:3.10-slim

RUN apt-get update -y && apt-get install -y git ffmpeg libavcodec-extra

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY server/model.py .
RUN python -c "from model import load;load(True);"

COPY server/api.py api.py

CMD ["python", "api.py"]