FROM python:latest
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN chmod +x wait-for-it.sh
# ENTRYPOINT [ "./wait-for-it.sh", "rabbitmq:5672", "--" ]
CMD ["python","main.py"]