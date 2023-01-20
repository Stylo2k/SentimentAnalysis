FROM python:3.10.8


WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ARG HOST
ARG PORT

ENV HOST=${HOST}
ENV PORT=${PORT}

RUN echo "HOST = ${HOST}"
RUN echo "PORT = ${PORT}"

CMD ["sh", "-c", "serve run --host $HOST --port $PORT main:sentiment_analysis"]