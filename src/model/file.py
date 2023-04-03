from requests import Response


class ResponseFile:
    """Binary content stream class

    This object is returned from API functions that stream binary content.
    Call the API function from a `with` statement, and call the read method
    on the object to read the data in chunks.
    """
    def __init__(self, response: Response):
        self.response = response

    def __enter__(self):
        return self.response.raw

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.response.close()
