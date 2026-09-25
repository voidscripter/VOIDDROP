"""Validated runtime configuration."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    host: str = "0.0.0.0"
    port: int = 8080
    directory: Path = Path.home() / "VOIDDROP"
    pin: str | None = None

    def __post_init__(self) -> None:
        if not 1 <= self.port <= 65535:
            raise ValueError("port must be between 1 and 65535")
        if self.pin is not None and (not self.pin.isdigit() or not 4 <= len(self.pin) <= 12):
            raise ValueError("PIN must contain 4 to 12 digits")
        object.__setattr__(self, "directory", self.directory.expanduser().resolve())
        self.directory.mkdir(parents=True, exist_ok=True)
        if not self.directory.is_dir():
            raise ValueError("shared directory is not a directory")
