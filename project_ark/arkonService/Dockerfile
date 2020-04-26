FROM python:3.7-slim-stretch


ENV SERVICE_PORT=5000
ENV MONGO_CONN="mongodb+srv://admin:4dm1n@cluster0-r5yzx.mongodb.net/test?retryWrites=true&w=majority"
ENV SERVICE_DIR=/home/metadata/service

RUN mkdir -p ${SERVICE_DIR}
RUN mkdir -p ${SERVICE_DIR}/src
WORKDIR ${SERVICE_DIR}

COPY src/ ./src
COPY requirements.txt .
COPY app.py .

RUN pip install -r requirements.txt

EXPOSE ${SERVICE_PORT}

CMD ["python","app.py"]
