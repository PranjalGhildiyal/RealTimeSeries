FROM python:3.8.17-slim-buster
COPY . /app
WORKDIR /app
RUN pip install --upgrade cython
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get -y update
RUN apt-get -y install vim nano
EXPOSE 5001
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]