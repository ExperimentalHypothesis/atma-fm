FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install  --no-cache-dir -r requirements.txt
USER root
RUN apt-get update && \
    apt-get install -y vim && \
    rm -rf /var/lib/apt/lists/*
EXPOSE 5555
ENV FLASK_APP=run.py
CMD ["flask", "run", "--host=0.0.0.0", "--port=5555"]
