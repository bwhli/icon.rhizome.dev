import httpx


class Http:
    def __init__(self) -> None:
        pass

    @classmethod
    async def get(
        cls,
        url: str,
        headers: dict = None,
        timeout: float = 10.0,
        retries=2,
    ):
        async with httpx.AsyncClient(
            timeout=timeout, transport=httpx.AsyncHTTPTransport(retries=retries)
        ) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status
            try:
                return response.json()
            except ValueError:
                return response
