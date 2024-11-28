FROM python:3.10

ENV TELEGRAM_BOT_TOKEN=your_bot_token
ENV ACCESS_CHECK=true

ENV DEBUG=false
ENV STAGE_CHAT_ID=-111111111

ENV CORETEAM_PEOPLE=tag1,tag_2,tagThree

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python-dev \
    build-essential \
    python3-venv

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY /src .

# Command to run the bot
CMD ["python3", "/app/gossip_bot.py"]