FROM python:3.9-slim
RUN apt-get update

WORKDIR /storenode
#copy python script and requiremente stext into /storenode in the container
COPY store.py /storenode/
COPY requirements.txt /storenode/
#install python dependencies that are in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "store.py"]


