FROM python:3.11 AS backend

WORKDIR /usr/src/embedchain

COPY requirements.txt .
COPY embedchain.tar.gz /usr/src/
RUN tar -zxvf /usr/src/embedchain.tar.gz -C /usr/src/
COPY api_server.py /usr/src/embedchain/

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "api_server.py"]
