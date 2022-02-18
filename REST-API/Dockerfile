FROM python:3.9

LABEL maintainer="Yegane Amirjani yeganeh.a.m7979@gmail.com"

EXPOSE 5000

WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

CMD ["python3", "app.py"]