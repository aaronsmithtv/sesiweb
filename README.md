# sesiweb

sesiweb is a Python module used as a driver for the SideFX web API. It provides a simple interface to interact with the API and obtain data about Houdini product builds.

## Installation

You can install sesiweb via pip:

```shell
pip install sesiweb
```
## Usage

To use sesiweb, you need to provide your SideFX API credentials:


```python
from sesiweb import SesiWeb

sesi_secret = "your_secret_key"
sesi_id = "your_client_id"

sw = SesiWeb(sesi_secret, sesi_id)
```

Once you have created an instance of SesiWeb, you can call its methods to retrieve data:


```python
# Get the most recent Houdini product builds
build = {"product": "houdini", "platform": "linux", "version": "18.5"}
latest_builds = sw.get_latest_builds(build)

# Get download info for a specific build
product_build = {"product": "houdini", "platform": "linux", "version": "18.5.351"}
build_download = sw.get_build_download(product_build)
```

For more information on the SideFX Web API, refer to the [SideFX Web API documentation](https://www.sidefx.com/docs/api/).

## License

sesiweb is licensed under the MIT License. See [LICENSE](LICENSE) for more information.
