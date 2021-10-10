FROM python:3.10

WORKDIR /code

COPY ./app /code/app
COPY ./config.py /code/config.py
COPY ./requirements.txt /code/requirements.txt
COPY ./run.py /code/run.py

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["python3", "run.py", "runserver", "--docker"]