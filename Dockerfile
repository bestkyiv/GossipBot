# Use the official Python image as a base
FROM python:3.10

RUN apt-get install -y python3 python3-pip python-dev build-essential python3-venv

WORKDIR /app

COPY requirements.txt .
COPY settings.ini .

RUN pip install --no-cache-dir -r requirements.txt

COPY /src .

# Command to run the bot
CMD python3 /app/gossip_bot.py;
