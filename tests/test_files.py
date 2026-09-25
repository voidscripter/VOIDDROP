from pathlib import Path

import pytest

from voiddrop.files import confined_path, delete_file, list_files, safe_filename


def test_safe_filename_reduces_paths_to_filename():
    assert safe_filename("../../etc/passwd") == "passwd"
    assert safe_filename(r"folder\photo.png") == "photo.png"


@pytest.mark.parametrize("name", ["", ".", "..", "../", "\x00", ".hidden"])
def test_safe_filename_rejects_empty_names(name):
    with pytest.raises(ValueError):
        safe_filename(name)


def test_confined_path_stays_inside_directory(tmp_path: Path):
    assert confined_path(tmp_path, "safe.txt") == tmp_path / "safe.txt"


def test_listing_and_delete(tmp_path: Path):
    (tmp_path / "visible.txt").write_text("data")
    (tmp_path / ".partial").write_text("hidden")
    outside = tmp_path.parent / "outside.txt"
    outside.write_text("outside")
    (tmp_path / "link").symlink_to(outside)
    assert [item["name"] for item in list_files(tmp_path)] == ["visible.txt"]
    delete_file(tmp_path, "visible.txt")
    assert not (tmp_path / "visible.txt").exists()
    assert outside.read_text() == "outside"
    with pytest.raises((FileNotFoundError, ValueError)):
        delete_file(tmp_path, "link")
