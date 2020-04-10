FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN mkdir -p /usr/src/app/templates
RUN pip install --no-cache-dir -r requirements.txt
COPY ./paypal_app.py .
COPY ./templates/index.html /usr/src/app/templates
CMD [ "python", "./paypal_app.py" ]
