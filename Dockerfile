FROM python:3.6.2
RUN apt-get -qq update
RUN apt-get -y install python-dev

RUN pip install virtualenv
RUN virtualenv /.env -p python3.6

COPY ./requirements.txt ./

RUN /.env/bin/pip3 install -r requirements.txt

WORKDIR /app_root
COPY ./app.py ./
COPY ./shrim ./shrim

RUN /.env/bin/apistar create_tables


CMD ["/.env/bin/apistar" , "run"]
