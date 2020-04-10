FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./menu.py .
EXPOSE 5001
CMD [ "python", "./menu.py" ]
