FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./order_flask.py .
CMD [ "python", "./order_flask.py" ]
EXPOSE 8010
