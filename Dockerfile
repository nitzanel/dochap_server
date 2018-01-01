FROM python:3.6-alpine
RUN apk add --update curl gcc g++ \
    && rm -rf /var/cache/apk/*
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
ADD ./app /app
ADD ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
