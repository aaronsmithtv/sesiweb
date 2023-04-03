from typing import Optional

from pydantic import AnyUrl, BaseModel


class ProductModel(BaseModel):
    """Base product build class for SideFX Web API.

    Attributes:
        product (str): The product to make requests for. Product accepts the
            following values: `'houdini', 'houdini-py3', 'houdini-py37',
            'houdini-py2', 'docker', 'sidefxlabs', 'houdini-launcher',
            'houdini-launcher-py3', 'houdini-launcher-py37', 'launcher-iso',
            'launcher-iso-py3', 'launcher-iso-py37', 'launcher-iso-py2'`
        platform (str): The operating system to install Houdini on: `'win64', 'macos',
            'macosx_arm64', 'linux'`. Does not effect Docker and SideFXLabs builds.
    """
    product: str
    platform: str


class ProductBuild(ProductModel):
    """A full product with build and version num, based on ProductModel.

    Attributes:
        product (str): The product name, e.g. `'houdini'`.
        platform (str): The platform name, e.g. `'linux'`.
        version (Optional[str]): A product version, e.g. `'17.0'`.
        build (Optional[str]): A product build, e.g. `'382'`.
    """
    version: Optional[str]
    build: Optional[str]


class DailyBuild(ProductBuild):
    """A web API return model, with date, release, status metadata appended.

    Attributes:
        product (str): The product name, e.g. `'houdini'`.
        platform (str): The platform name, e.g. `'linux'`.
        version (Optional[str]): A product version, e.g. `'17.0'`.
        build (Optional[str]): A product build, e.g. `'382'`.
        date (str): The date the build was introduced, in `'YYYY/MM/DD'` format.
        release (str): The type of release the build is tagged with, e.g.`'gold'`.
        status (str): The condition of the build, e.g. `'good'`.
    """
    date: str
    release: str
    status: str

    class Config:
        schema_extra = {
            "example": {
                "build": "382",
                "date": "2018/10/26",
                "platform": "linux_x86_64_gcc6.3",
                "product": "houdini",
                "release": "devel",
                "status": "good",
                "version": "17.0",
            }
        }


class InstallBuild(BaseModel):
    """Download & installation metadata for a returned build.

    Attributes:
        download_url (AnyUrl): A cloudfront URL to download the build from.
        filename (str): A filename for the downloadable binary.
        hash (str): A hash for the downloadable binary.
    """
    download_url: AnyUrl
    filename: str
    hash: str


class BuildDownloadModel(InstallBuild):
    """Full download metadata with build status, size and date introduced

    Attributes:
        download_url (AnyUrl): A cloudfront URL to download the build from.
        filename (str): A filename for the downloadable binary.
        hash (str): A hash for the downloadable binary.
        date (str): The date the build was introduced, in `'YYYY/MM/DD'` format.
        releases_list (str): The type of release the build is tagged with, e.g.`'gold'`.
        status (str): The condition of the build, e.g. `'good'`.
        size (int): The integer filesize of the download in bytes.
    """
    date: str
    releases_list: str
    status: str
    size: int

    class Config:
        schema_extra = {
            "example": {
                "date": "2018/10/26",
                "download_url": "https://example.cloudfront.net/download",
                "filename": "houdini-17.0.352-win64-vc141.exe",
                "hash": "001e6e62aed5a3e5c10d3f2019bf41b5",
                "releases_list": "gold",
                "status": "good",
                "size": 1114902200,
            }
        }


class HServerModel(BaseModel):
    server_name: str
    server_code: str
    version: str
    products: str


class LicenseModel(BaseModel):
    license_keys: list[str]
    server_key: str
