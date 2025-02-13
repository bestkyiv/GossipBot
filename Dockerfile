FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r /app/requirements.txt

ENV PYTHONUNBUFFERED=1

# Run gossip_bot.py when the container launches
CMD ["python", "src/gossip_bot.py"]