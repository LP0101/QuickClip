FROM python:slim

COPY . /app
WORKDIR /app
RUN apt-get update && apt-get install -y gcc ffmpeg
RUN pip install --upgrade pip && pip install --upgrade setuptools
RUN pip install -r requirements.txt
RUN apt-get remove -y gcc && apt-get -y autoremove
EXPOSE 5000
CMD ["/app/start.sh"]