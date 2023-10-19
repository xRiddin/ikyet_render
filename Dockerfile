FROM tiangolo/uvicorn-gunicorn:python3.9
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt && \
    pip install "uvicorn[standard]" gunicorn

CMD ["gunicorn", "app_websocket:app", \
 "--workers", "4", \
 "--worker-class", "uvicorn.workers.UvicornWorker", \
 "--bind", "0.0.0.0:8000", \
 "--timeout", "1000"]

EXPOSE 8000

