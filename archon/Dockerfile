FROM python:3

RUN mkdir /app
RUN mkdir /app/log

ADD requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

ADD . /app
WORKDIR /app
VOLUME /app
#ENV MONGODB_PORT_27017_TCP_ADDR localhost

CMD [ "python", "report.py" ]
