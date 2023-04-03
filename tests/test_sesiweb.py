import os

from src.sesiweb import SesiWeb
from src.sesiweb.model.service import ProductBuild, ProductModel

client_id = os.environ.get("SIDEFX_CLIENT")
client_secret = os.environ.get("SIDEFX_SECRET")


def test_sesiweb_initialization():
    sesiweb = SesiWeb(client_id, client_secret)
    assert sesiweb is not None


def test_get_latest_builds():
    sesiweb = SesiWeb(client_id, client_secret)
    prodinfo = ProductModel(product="houdini", platform="linux")
    prodfilter = {"status": "good", "release": "gold"}
    latest_builds = sesiweb.get_latest_builds(
        prodinfo=prodinfo,
        only_production=False,
        prodfilter=prodfilter
    )
    assert latest_builds is not None
    assert len(latest_builds) > 0


def test_get_latest_build():
    sesiweb = SesiWeb(client_id, client_secret)
    prodinfo = ProductModel(product="houdini", platform="linux")
    prodfilter = {"status": "good", "release": "gold"}
    latest_builds = sesiweb.get_latest_build(
        prodinfo=prodinfo,
        only_production=False,
        prodfilter=prodfilter
    )
    assert latest_builds is not None


def test_get_dl():
    sesiweb = SesiWeb(client_id, client_secret)
    prodinfo = ProductModel(product="houdini", platform="linux")
    prodfilter = {"status": "good", "release": "gold"}
    latest_build = sesiweb.get_latest_build(
        prodinfo=prodinfo,
        only_production=False,
        prodfilter=prodfilter
    )

    build_dl = sesiweb.get_build_download(
        prodinfo=ProductBuild(**latest_build.dict())
    )

    assert build_dl is not None
