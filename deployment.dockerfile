FROM python:3.10.8


WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ARG HOST
ARG PORT
ARG DASHBOARD_PORT

ENV HOST=${HOST}
ENV PORT=${PORT}
ENV DASHBOARD_PORT=${DASHBOARD_PORT}

RUN echo "HOST = ${HOST}"
RUN echo "PORT = ${PORT}"
RUN echo "DASHBOARD_PORT = ${DASHBOARD_PORT}"


CMD ["sh", "-c", "ray start --head --dashboard-port=$DASHBOARD_PORT --dashboard-host=0.0.0.0 && serve run --host $HOST --port $PORT main:sentiment_analysis"]