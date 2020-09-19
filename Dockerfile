FROM python:2
RUN apt-get update && apt-get install -y default-libmysqlclient-dev default-mysql-client
COPY ./requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
CMD ["gunicorn", "manage:app", "-c", "etc/gunicorn.conf.py"]
