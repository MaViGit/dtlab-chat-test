FROM python:3-slim-buster
WORKDIR /var/dtlab-chat
VOLUME /var/dtlab-chat
COPY *.py ./
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_ENV=development, FLASK_APP=server.py
CMD ["flask", "run", "--host", "0.0.0.0"]