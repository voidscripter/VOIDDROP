from pathlib import Path

import pytest

from voiddrop.config import Config


def test_config_creates_shared_directory(tmp_path: Path):
    shared = tmp_path / "nested" / "share"
    config = Config(directory=shared)
    assert shared.is_dir()
    assert config.directory == shared.resolve()


@pytest.mark.parametrize("kwargs", [{"port": 0}, {"port": 65536}, {"pin": "abc"}, {"pin": "123"}])
def test_config_rejects_invalid_values(tmp_path, kwargs):
    with pytest.raises(ValueError):
        Config(directory=tmp_path, **kwargs)
