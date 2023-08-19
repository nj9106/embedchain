FROM python:3.11 AS backend

WORKDIR /usr/src/embedchain
COPY requirements.txt .
COPY 
RUN pip install -r requirements.txt

COPY ../../../embedchain /usr/src/
COPY api_server.py /usr/src/embedchain/

EXPOSE 5000

CMD ["python", "api_server.py"]
