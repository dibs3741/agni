FROM python:3.6.5-alpine 

RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd


WORKDIR /app
ADD ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app
COPY ./data /app/data
COPY src/main/python/* /app/src/main/python/
#RUN ls -altr src/main/python
#RUN which python

CMD python -u src/main/python/app.py
