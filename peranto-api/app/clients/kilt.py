import typing as t

from httpx import Client, Response, HTTPError


class RedditClientError(Exception):
    def __init__(self, message: str, raw_response: t.Optional[Response] = None):
        self.message = message
        self.raw_response = raw_response
        super().__init__(self.message)


class KiltClient:
    base_url: str = "http://localhost:5000/kilt/"
    base_error: t.Type[RedditClientError] = RedditClientError

    def __init__(self) -> None:
        self.session = Client()
        self.session.headers.update(
            {"Content-Type": "application/json", "User-agent": "recipe bot 0.1"}
        )

    async def _perform_request(  # type: ignore
        self, method: str, path: str, *args, **kwargs
    ) -> Response:
        res = None
        try:
            res = getattr(self.session, method)(
                f"{self.base_url}{path}", *args, **kwargs
            )
            res.raise_for_status()
        except HTTPError:
            raise self.base_error(
                f"{self.__class__.__name__} request failure:\n"
                f"{method.upper()}: {path}\n"
                f"Message: {res is not None and res.text}",
                raw_response=res,
            )
        return res

# authenticate send request to kilt server to authenticate user
    def authenticate(self, presentation:str) -> Response:
        return self._perform_request(
            "post",
            "present",
            json={"presentation": presentation},
        )
    
    async def signup(self, email: str, light_did_uri: str) -> Response:
        return await self._perform_request(
            "post",
            "register",
            json={"email": email, "lightDidUri": light_did_uri},
        )
    