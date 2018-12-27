FROM python:3.6
MAINTAINER Moshfiqur Rahman <rahman.moshfiqur@gmail.com>

COPY app/requirements.txt /usr/src/app/
WORKDIR /usr/src/app
RUN pip install -r requirements.txt

COPY app/ /usr/src/app
EXPOSE 10080
CMD ["gunicorn", "serve:app", "-c", "/usr/src/app/gunicorn_config.py"]