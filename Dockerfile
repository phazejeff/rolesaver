FROM python:3

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY main.py .
COPY bot.py .
COPY views ./views
COPY events ./events
COPY database ./database
COPY context ./context
COPY commands ./commands

CMD ["python3", "main.py"]