# This docker file is meant to be used for development purposes
# It is not meant to be used in production
# So when wanting to run the app in development mode, use this docker file
# To build the image, run the following command:
# docker build -f dev.dockerfile -t ray-serve-dev .
# To run the image, run the following command:

# docker run -p 2000-9000:2000-9000 -v $(pwd):/app -it ray-serve-dev bash

# or simply if you are using vscode and have the docker extension installed
# choose the option to open the folder in a container and then choose this Dockerfile

FROM python:3.10.8


WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt


ENTRYPOINT ["/bin/bash"]