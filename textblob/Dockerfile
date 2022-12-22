FROM rayproject/ray


WORKDIR /app

RUN pip install ray[serve]
RUN pip install requests
RUN pip install torch

# these libs hold the models we use
RUN pip install transformers
RUN pip install textblob
RUN pip install vader

COPY . .

ARG HOST
ARG TEXT_BLOB_PORT

ENV HOST=${HOST}
ENV TEXT_BLOB_PORT=${TEXT_BLOB_PORT}

RUN echo "HOST = ${HOST}"
RUN echo "PORT = ${TEXT_BLOB_PORT}"

CMD ["sh", "-c", "serve run --host $HOST --port $TEXT_BLOB_PORT classifier_textblob:classifier"]