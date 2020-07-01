FROM python:3.6
WORKDIR /app
COPY . .
COPY manage.py requirement.txt /app/
RUN pip install -r requirement.txt
RUN wget -O- https://dl.bintray.com/rabbitmq/Keys/rabbitmq-release-signing-key.asc | apt-key add -
RUN wget -O- https://dl.bintray.com/rabbitmq/Keys/rabbitmq-release-signing-key.asc | apt-key add -
RUN apt-get update && curl -fsSL https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc | apt-key add - && curl -fsSL https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc | apt-key add -
RUN apt-key adv --keyserver "hkps://keys.openpgp.org" --recv-keys "somekey" && apt-get install apt-transport-https -y && apt-get update -y
RUN apt-get install rabbitmq-server -y && service rabbitmq-server start
RUN apt-get install supervisor -y
COPY mysite-celery.conf /etc/supervisor/conf.d/
CMD python manage.py runserver 0.0.0.0:8000


