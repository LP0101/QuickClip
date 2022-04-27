FROM python:slim

COPY . /app
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential
RUN pip install -r requirements.txt
RUN apt-get remove -y build-essential && apt-get -y autoremove
EXPOSE 5000
CMD ["/app/start.sh"]