# Development 

To build the image, run the following command:

```bash
docker build -f dev.dockerfile -t ray-serve-dev .
```

To run the image, run the following command:

```bash
 docker run -p 2000-9000:2000-9000 -v $(pwd):/app -it ray-serve-dev bash
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