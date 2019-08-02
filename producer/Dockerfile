FROM python:3.7

WORKDIR /usr/app

ADD ./serverlog.txt ./
ADD ./requirements.txt ./

RUN pip install -r requirements.txt
ADD ./ ./

CMD python -u app.py
