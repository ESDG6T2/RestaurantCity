FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./paypal_app.py .
CMD [ "python", "./paypal_app.py" ]
