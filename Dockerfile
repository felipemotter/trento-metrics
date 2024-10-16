# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install debugpy

COPY . .

EXPOSE 8501 5678

ENV DEBUG=true

CMD if [ "$DEBUG" = "true" ] ; then \
        python -m debugpy --wait-for-client --listen 0.0.0.0:5678 -m streamlit run app/main.py --server.address=0.0.0.0 --server.port=8501 ; \
     else \
        streamlit run app/main.py --server.address=0.0.0.0 --server.port=8501 ; \
     fi
