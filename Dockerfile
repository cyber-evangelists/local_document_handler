FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV FLASK_APP=main.py
ENV FLASK_ENVIRONMENT=development
# RUN pip install flask
COPY . .
EXPOSE 5000
CMD ["python","main.py"]