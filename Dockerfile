FROM python:3.10-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    cmake \
    ninja-build \
    patchelf \
    build-essential \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/* 

RUN python -m pip install --upgrade pip setuptools wheel
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 3000
CMD python ./app.py