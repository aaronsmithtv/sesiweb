# <img src="https://static.sidefx.com/images/apple-touch-icon.png" width="25" height="25" alt="Hbuild Logo"> sesiweb

![Test](https://github.com/aaronsmithtv/sesiweb/actions/workflows/test.yml/badge.svg)

sesiweb is a Python module used as a synchronous driver for the SideFX Web API. It provides a simple interface to interact with the API and obtain data about Houdini product builds.

Inputs are validated with Pydantic, and methods in sesiweb provide additional lookup functionality, exceptions, and models.

## Table of Contents

- [Installation](#installation)
- [Daily Build Listing](#daily-build-listing)
- [Acquiring a Build Download](#acquiring-a-build-download)
- [License](#license)

## Installation

You can install sesiweb via pip:

```shell
pip install --upgrade sesiweb
```

*Note: sesiweb is intended for Python 3, as it supports several modern Python features.*

## Daily Build Listing

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

For more information on the SideFX Web API and the returned results you can filter by, refer to the [SideFX Web API documentation](https://www.sidefx.com/docs/api/).

## Acquiring a Build Download

Using sesiweb, you can also transform a `DailyBuild` object into a `ProductBuild` object, which is a required input for acquiring a download URL.

In the script below, 

```python
# Get the latest Houdini build (filtered)
build = sw.get_latest_build(prodinfo=build, prodfilter=buildfilter)

# Get the download URL, filename and hash of the build
build_dl = sw.get_build_download(
	prodinfo=ProductBuild(**build.dict())
)

print(build_dl)
```

This will return a `BuildDownloadModel` object containing a download URL, build filename, and hash:

```shell
download_url=AnyUrl('https://gjvnth38g.cloudfront.net/download/download-build/456223/cdn/?Expires=166636236...
```

## License

sesiweb is licensed under the MIT License. See [LICENSE](LICENSE) for more information.
