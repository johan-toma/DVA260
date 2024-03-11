FROM python:3.9-slim
RUN apt-get update

WORKDIR /datanode
COPY data_generator.py /datanode/
##EXPOSE 5000 

CMD ["python", "data_generator.py"]
