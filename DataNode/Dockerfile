FROM python:3.9-slim
RUN apt-get update
RUN apt-get install -y flask
RUN apt-get install -y pandas
RUN apt-get install -y requests

WORKDIR /datanode
COPY data_generator.py /datanode/
EXPOSE 5000

CMD ["python", "data_generator.py"]
