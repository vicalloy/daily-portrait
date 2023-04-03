FROM python:3.10
RUN pip install poetry

RUN apt-get update && apt-get install -y \
		cmake \
		ffmpeg libsm6 libxext6 \
		--no-install-recommends

RUN mkdir /app
WORKDIR /app

COPY ./ ./
RUN poetry config virtualenvs.create false
RUN poetry install --only main

ENTRYPOINT ["python", "app.py"]
