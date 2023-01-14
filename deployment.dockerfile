FROM python:3.10.8


WORKDIR /app

# RUN pip install ray[serve]
# RUN pip install requests
# RUN pip install torch

# # these libs hold the models we use
# RUN pip install transformers
# RUN pip install textblob
# RUN pip install vader

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./*classifier .

ARG HOST
ARG PORT

ENV HOST=${HOST}
ENV PORT=${PORT}

RUN echo "HOST = ${HOST}"
RUN echo "PORT = ${PORT}"

CMD ["sh", "-c", "serve run --host $HOST --port $PORT main:sentiment_analysis"]