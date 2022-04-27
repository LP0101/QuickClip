FROM python:slim

COPY . /app
WORKDIR /app
RUN pip install flask
CMD ["flask", "run", "--host=0.0.0.0"]