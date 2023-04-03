import base64
import html
import json
import time
from typing import Any, AnyStr, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .exceptions import APIError, AuthorizationError
from .model.file import ResponseFile
from .model.service import (BuildDownloadModel, DailyBuild, HServerModel,
                            LicenseModel, ProductBuild, ProductModel)


class SesiWeb:
    """Http client for SideFX Web API

    Opens a synchronous requests http session for the SideFX Web API. A full
    length access token is created in the __init__ method, from the input
    client_id and client_secret.

    A custom endpoint can be used if necessary in the endpoint_url attribute.

    Attributes:
        session (requests.Session): The requests session.
        endpoint_url (str): The SideFX web API endpoint url, default:
            `https://www.sidefx.com/api/`
        access_token_url (str): The oauth2 application token url, default:
            `https://www.sidefx.com/oauth2/application_token`
        access_token (str): The constructed access token from client_id and
            client_secret, for the SideFX Web API app oauth2 process.
        expiry_time (str): The expiration time of the access token.

    """
    def __init__(self, client_id: str, client_secret: str):
        """Construct http session and access token

        Args:
            client_id (str): SideFX Application client id
            client_secret (str): SideFX Application secret key
        """
        self.session = get_session()
        self.endpoint_url = "https://www.sidefx.com/api/"
        self.access_token_url = "https://www.sidefx.com/oauth2/application_token"
        self.access_token, self.expiry_time = get_access_token(
            access_token_url=self.access_token_url,
            client_secret_key=client_secret,
            client_id=client_id
        )

    def get_latest_builds(
            self, prodinfo: ProductModel | dict,
            only_production: Optional[bool] = True,
            prodfilter: Optional[dict] = None) -> list[DailyBuild]:
        """List all latest SideFX product builds, with metadata

        Args:
            prodinfo (ProductModel | dict): The input product and platform data,
                (e.g houdini & linux).
            only_production (Optional[bool]): Whether builds are daily (False)
                or production (True), default: True
            prodfilter (Optional[dict]): An optional filter for the results of
                latest builds. Accepted keys are `'build', 'date',
                'release', 'status', 'version'`.

        Returns:
            list[DailyBuild]: A list of builds, with returned metadata for each
                build.
        """
        api_command = "download.get_daily_builds_list"

        build_dict = dict(prodinfo)
        build_dict.update({'only_production': only_production})

        post_data = dict(json=json.dumps([api_command, [], build_dict]))
        resp_builds = self.get_session_response(post_data)

        if prodfilter:
            resp_builds = filter_list_response(resp_builds, prodfilter)

        builds = [DailyBuild.parse_obj(resp_build) for resp_build in resp_builds]

        return builds

    def get_latest_build(
            self, prodinfo: ProductModel | dict,
            only_production: Optional[bool] = True,
            prodfilter: Optional[dict] = None) -> DailyBuild:
        """Single return method for get_latest_builds

        Args:
            prodinfo (ProductModel | dict): The input product and platform data,
                (e.g houdini & linux).
            only_production (Optional[bool]): Whether builds are daily (False)
                or production (True), default: True
            prodfilter (Optional[dict]): An optional filter for the results of
                latest builds. Accepted keys are `'build', 'date',
                'release', 'status', 'version'`.

        Returns:
            list[DailyBuild]: A list of builds
        """
        return self.get_latest_builds(prodinfo, only_production, prodfilter)[0]

    def get_build_download(
            self, prodinfo: ProductBuild | dict) -> BuildDownloadModel:
        """Using ProductBuild object data, get download info for the build

        Args:
            prodinfo (ProductBuild | dict): Info based on the appropriate
                product, build and version.

        Returns:
            BuildDownloadModel: Download, hash and filename data.
        """
        api_command = "download.get_daily_build_download"

        build_dict = dict(prodinfo)
        post_data = dict(json=json.dumps([api_command, [], build_dict]))
        resp_build = self.get_session_response(post_data)
        build_dl = BuildDownloadModel.parse_obj(resp_build)
        return build_dl

    def get_nc_license(self, srvinfo: HServerModel):
        """Generate a non-commercial license key

        Args:
            srvinfo (HServerModel): License server data to generate NC key to.

        Returns:
            LicenseModel: A full license key string accompanied with a matching
                server key.
        """
        api_command = "license.get_non_commercial_license"

        build_dict = dict(srvinfo)
        post_data = dict(json=json.dumps([api_command, [], build_dict]))
        resp_build = self.get_session_response(post_data)
        build_dl = LicenseModel.parse_obj(resp_build)
        return build_dl

    def get_session_response(
            self, post_data: dict[str, Any],
            timeout: Optional[int] = None) -> Any:
        """Get an appropriate response from constructed requests session.

        Args:
            post_data (dict[str, Any]): SideFX Web API POST request data
            timeout (Optional[int]): Optional timeout length, default: None

        Returns:
            Any: Session response.
        """
        response = self.session.post(
            self.endpoint_url,
            headers={"Authorization": "Bearer " + self.access_token},
            data=post_data,
            timeout=timeout)
        if response.status_code == 200:
            if response.headers.get("Content-Type") == "application/octet-stream":
                return ResponseFile(response)
            return response.json()

        raise APIError(
            response.status_code,
            extract_traceback(response))


def get_session() -> requests.Session:
    """Get a requests http session

    Returns:
        requests.Session: A http session
    """
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, ],
        method_whitelist=["GET", "POST"],
        backoff_factor=1,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)
    return http


def get_access_token(
        client_id: str,
        client_secret_key: str,
        access_token_url: str,
        timeout: Optional[int] = None) -> (AnyStr, AnyStr):
    """Construct the access token for API requests

    Given an API client (id and secret key) that is allowed to make API
    calls, return an access token that can be used to make calls.

    If request is made using the /token URL directly then assume the app a
    client-credentials based application.

    Args:
        client_id (str): SideFX Web API supplied client id
        client_secret_key (str): SideFX Web API supplied client secret
        access_token_url (str): The request URL made
        timeout (Optional[int]): The timeout length in seconds for the POST
            request, default: None

    Returns:
        (AnyStr, AnyStr): A tuple containing the access token, and length
            of time before token expiry.
    """
    post_data = {}
    if access_token_url.endswith("/token") or access_token_url.endswith("/token/"):
        post_data["grant_type"] = "client_credentials"

    auth_header = f"{client_id}:{client_secret_key}".encode()

    response = requests.post(
        access_token_url,
        headers={
            "Authorization": f"Basic {base64.b64encode(auth_header).decode('utf-8')}",
        },
        data=post_data,
        timeout=timeout)

    if response.status_code != 200:
        status_msg = f"{response.status_code}: {extract_traceback(response)}"
        raise AuthorizationError(response.status_code, status_msg)

    response_json = response.json()
    access_token_expiry_time = time.time() - 2 + response_json["expires_in"]
    return response_json["access_token"], access_token_expiry_time


def extract_traceback(response: requests.Response) -> AnyStr:
    """Extracts error message from non-200 response

    Helper function to extract a traceback from the web server response
    if an API call generated a server-side exception and the server is running
    in debug mode.  In production mode, the server will send back just the
    stack trace without the need to parse any html.

    Args:
        response (requests.Respones): The non-200 response

    Returns:
        AnyStr: The HTML converted traceback message
    """
    error_message = response.text
    if response.status_code != 500:
        return error_message

    traceback = ""
    for line in error_message.split("\n"):
        if traceback and line == "</textarea>":
            break
        if line == "Traceback:" or traceback:
            traceback += line + "\n"

    if traceback:
        traceback = error_message

    return html.unescape(traceback)


def without_keys(d: dict, keys: list[str]) -> dict:
    """Return a dict without keys specified in list

    Args:
        d (dict): Dict to remove keys from
        keys (list[str]): Keys to remove

    Returns:
        dict: Original dict with removed keys
    """
    return {k: d[k] for k in d.keys() - keys}


def filter_list_response(results: list[dict], resfilter: dict) -> list[dict]:
    """Returns a filtered dict array

    Args:
        results (list[dict]): A list of dict objects to filter
        resfilter (dict): Key/value pairs to filter by

    Returns:
        list[dict]:
    """
    def filter_func(d):
        return all(
            d[k] == v if k in d else KeyError() for k, v in resfilter.items()
        )

    return list(filter(filter_func, results))
