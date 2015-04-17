FROM python

ADD . /code/
WORKDIR /code/

RUN pip install -r requirements-dev.txt -e .

CMD py.test
