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
docker build -f dev.dockerfile -t se-dev .
```

To run the image, run the following command:

```bash
 docker run -p 2000-4000:2000-4000  -p 7001-9000:7001-9000 --shm-size=2.25gb -v $(pwd):/app -it se-dev bash
```
> preferably you should do `-p 2000:9000 ` but sometimes the OS is using some of the ports.

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