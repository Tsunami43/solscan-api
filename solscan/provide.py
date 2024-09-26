from asyncio import sleep
from typing import Optional, Dict, Any
from httpx import AsyncClient, ConnectTimeout, ReadTimeout, HTTPError
from urllib.parse import urlencode
from .errors.network import HTTPRequestError


class HTTPClient:

    def __init__(self, endpoint: str):

        self.endpoint = endpoint

    async def send_request(
        self,
        token: str,
        method: str,
        params: Optional[Dict[str, Any]] = None,
        timeout: int = 30,
        retries: int = 0,
    ) -> Dict:

        headers = {"accept": "*/*", "token": token}

        if params:
            url = self.endpoint + method + "?" + urlencode(params)
        else:
            url = self.endpoint + method

        async with AsyncClient(timeout=timeout) as client:
            try:
                response = await client.get(url=url, headers=headers)
                response.raise_for_status()
                if method == "account/exportTransactions":
                    return response.content.decode("utf-8")
                return response.json()
            except HTTPError as e:
                if e.response.status_code == 429:
                    if retries >= 6:
                        raise HTTPRequestError(
                            f"Retry limit reached ({retries}). {e}",
                            method,
                            params,
                            original_exception=e,
                        ) from e
                    await sleep(2**retries)
                    return await self.send_request(method, params, retries + 1)
                else:
                    raise HTTPRequestError(
                        str(e), method, params, original_exception=e
                    ) from e
            except ConnectTimeout as e:
                raise HTTPRequestError(
                    f"ConnectTimeout: {method}", method, params, original_exception=e
                ) from e
            except ReadTimeout as e:
                raise HTTPRequestError(
                    f"ReadTimeout: {method}", method, params, original_exception=e
                ) from e
            except Exception as e:
                raise HTTPRequestError(
                    f"An unexpected error occurred: {e}",
                    method,
                    params,
                    original_exception=e,
                ) from e
