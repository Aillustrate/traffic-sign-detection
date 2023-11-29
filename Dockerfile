# pull official base image
FROM python:3.10-bookworm

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY ./app .
COPY ./requirements.txt .
RUN mkdir -p ./models/yolov8m/weights
RUN wget -O best.pt "https://www.dropbox.com/scl/fi/ye3qi9oylkywupdglalp1/best.pt?rlkey=z7q4ojubm0sez264ucvh74rf7&dl=0"
RUN mv best.pt ./models/yolov8m/weights/best.pt
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
CMD ["python3", "main.py"] 