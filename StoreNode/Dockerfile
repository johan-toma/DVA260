FROM python:3.9-slim
RUN apt-get update

WORKDIR /storenode
COPY store.py /storenode/
COPY requirements.txt /storenode/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000

##environment variables for mongodb
ENV MONGODB_URI="mongodb://localhost:27017/"

CMD ["python", "store.py"]


