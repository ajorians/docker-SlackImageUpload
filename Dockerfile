FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install cron
RUN apt-get update

RUN apt-get install -y \
    cron \
    procps \
    curl \
    vim \
    less

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY post_image.py .
COPY images ./images
COPY crontab /etc/cron.d/slack-image-cron

# Set correct permissions and register cron job
RUN chmod 0644 /etc/cron.d/slack-image-cron \
    && crontab /etc/cron.d/slack-image-cron \
    && touch /var/log/cron.log

VOLUME ["/data"]

# Start cron in foreground
CMD ["cron", "-f"]
