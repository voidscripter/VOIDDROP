"""Small process-local PIN gate."""

import hmac
import secrets


class PinAuth:
    def __init__(self, pin: str | None) -> None:
        self._pin = pin
        self._token = secrets.token_urlsafe(32)

    @property
    def enabled(self) -> bool:
        return self._pin is not None

    def verify_pin(self, supplied: str) -> bool:
        return self._pin is not None and hmac.compare_digest(self._pin, supplied)

    def verify_token(self, supplied: str | None) -> bool:
        return self._pin is None or (supplied is not None and hmac.compare_digest(self._token, supplied))

    @property
    def token(self) -> str:
        return self._token
