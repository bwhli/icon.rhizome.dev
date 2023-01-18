import httpx


class HttpClient:
    def __init__(self) -> None:
        pass

    @staticmethod
    async def get(
        url: str,
        headers: dict = None,
        timeout: float = 10.0,
        retries: int = 2,
    ):
        async with httpx.AsyncClient(
            timeout=timeout, transport=httpx.AsyncHTTPTransport(retries=retries)
        ) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status
            return response

    @staticmethod
    async def post(
        url: str,
        payload: dict,
        headers: dict = None,
        timeout: float = 10.0,
        retries: int = 2,
        auth: tuple = None,
    ):
        async with httpx.AsyncClient(
            timeout=timeout, transport=httpx.AsyncHTTPTransport(retries=retries)
        ) as client:
            response = await client.post(url, headers=headers, json=payload, auth=auth)
            response.raise_for_status
            return response
