FROM python:3.11

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /usr/src/app/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]