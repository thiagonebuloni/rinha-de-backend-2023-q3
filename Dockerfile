FROM python:3.9.7

WORKDIR /user/app

COPY requirements.txt ./

# RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

CMD [ "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "80" ]
