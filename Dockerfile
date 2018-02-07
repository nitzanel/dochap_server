FROM python:3.6-alpine
RUN apk add --update curl gcc g++ \
    && rm -rf /var/cache/apk/*
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
WORKDIR /app
ADD ./base_requirements.txt /app/base_requirements.txt
RUN pip install -r base_requirements.txt
ADD ./requirements.txt /app/requirements.txt
#RUN pip install -r requirements.txt
ADD ./dochap_tool /dochap_tool
WORKDIR /dochap_tool
RUN python /dochap_tool/setup.py install
WORKDIR /app
ADD ./app/download_and_setup_db.py /app/download_and_setup_db.py
RUN python /app/download_and_setup_db.py
ADD ./app /app
CMD ["python", "app.py"]
