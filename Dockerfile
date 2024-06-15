# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY app/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Needed for remote debugging (Python Tools for Visual Studio Debugging)
RUN pip install debugpy

# Debug tools
RUN apt-get update \
    && apt-get install -y procps iputils-ping curl \
    && echo "alias ll='ls -la'" >> /root/.bashrc

CMD ["python", "app.py"]
