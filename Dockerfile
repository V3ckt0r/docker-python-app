FROM ubuntu:latest
MAINTAINER Vect0r
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN pip install flask prometheus_client	
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
