# sesiweb

sesiweb is a Python module used as a driver for the SideFX web API. It provides a simple interface to interact with the API and obtain data about Houdini product builds.

Inputs are validated with Pydantic, and methods in sesiweb provide additional lookup functionality, exceptions, and models.

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

Once you have created an instance of SesiWeb, you can call its methods to retrieve data. For example, `get_latest_builds` will return a list of the `DailyBuild` object:


```python
# Get the most recent Houdini product builds
build = {"product": "houdini", "platform": "linux", "version": "19.5"}
latest_builds = sw.get_latest_builds(build)

print(latest_builds)
```

This will return:

```shell
[DailyBuild(product='houdini', platform='linux_x86_64_gcc9.3', version='19.5', build='569', date='2023/03/29', release='gold', status='good'), DailyBuild(...
```

You can also filter builds with the `prodfilter` arg:

```python
buildfilter = {"status": "good", "release": "gold"}

latest_builds = sw.get_latest_builds(
    prodinfo=build,
    prodfilter=buildfilter
)
```

For more information on the SideFX Web API, refer to the [SideFX Web API documentation](https://www.sidefx.com/docs/api/).

## License

sesiweb is licensed under the MIT License. See [LICENSE](LICENSE) for more information.
