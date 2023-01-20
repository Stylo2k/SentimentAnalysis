table of contents:
- [Setup](#setup)
- [Deployment](#deployment)
- [Development](#development)

# Setup

Firstly you will have to configure your environment variables. You can do this by creating a .env file in the root directory of the project and adding the following variables:

```bash
HOST=0.0.0.0
PORT=3000
DASHBOARD_PORT=8265
DASHBOARD_HOST=0.0.0.0
```
Or by :
```bash
cp .env.example .env
```

> You can also find the .env.example file in the root directory of the project.

# Deployment

To deploy:

```bash
docker compose up
```

Now you can access the dashboard at [http://localhost:\$DASHBOARD_PORT](http://127.0.0.1:$DASHBOARD_PORT)

You can also access the sentiment analysis API at [http://localhost:\$PORT/se/](http://127.0.0.1:$PORT/se/)

To view the swagger documentation for the API, go to [http://localhost:\$PORT/docs/](http://127.0.0.1:$PORT/se/docs)


# Development 

To build the image, run the following command:
```bash
docker compose -f development.yml up -d
```
Now a docker container should be running with the name `se_dev` with your current working directory mounted to the `/app` directory inside the container.

Now attach to the container by running the following command:

```bash
docker exec -it se_dev bash
```

Now you can develop on your local machine and the changes will be reflected in the container.

To run the application, run the following command:

```bash
serve run main:sentiment_analysis
```

An alternative way to build the image is by running the following command:

```bash
docker build -f dev.dockerfile -t se_dev .
```

To run the image, run the following command:

```bash
 docker run -p 2000-4000:2000-4000  -p 7001-9000:7001-9000 --shm-size=2.25gb -v $(pwd):/app -it se_dev bash
```
> preferably you should do `-p 2000:9000 ` but sometimes the OS is using some of the ports.

Note: the container will be running in the background, to attach to it run the following command:

```bash
docker stop se_dev
```

or simply if you are using vscode and have the docker extension installed choose the option to open the folder in a container and then choose the dev.dockerfile.

Or make a .devcontainer folder then a devcontainer.json file and paste the following inside:
```json
{
	"name": "Existing Dockerfile",
	"build": {
		"context": "..",
		"dockerfile": "../dev.dockerfile"
	}
}
```