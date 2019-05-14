FROM python:3.6

WORKDIR /opt/webapp

ADD ./requirements.txt /tmp/requirements.txt

RUN pip install --trusted-host pypi.python.org -r /tmp/requirements.txt


COPY . /opt/webapp

#EXPOSE 80

#RUN adduser myuser
#USER myuser


CMD gunicorn --bind 0.0.0.0:$PORT run