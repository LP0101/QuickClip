FROM python:slim
COPY . /app
RUN pip install --upgrade pip && pip install --upgrade setuptools
RUN apt-get update && apt-get install -y gcc ffmpeg python3-dev build-essential
WORKDIR /app
RUN pip install -r requirements.txt
RUN apt-get remove -y gcc build-essential && apt-get -y autoremove
EXPOSE 5000
CMD ["/app/start.sh"]