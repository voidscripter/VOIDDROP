"""Safe operations confined to the configured shared directory."""

from pathlib import Path
import unicodedata


def safe_filename(value: str) -> str:
    name = unicodedata.normalize("NFKC", value).replace("\\", "/").split("/")[-1]
    name = "".join(ch for ch in name if ch.isprintable() and ch not in "\x00")
    if name.startswith("."):
        raise ValueError("hidden filenames are not allowed")
    name = name.strip().strip(".")
    if name in {"", ".", ".."}:
        raise ValueError("filename is empty or invalid")
    if len(name.encode("utf-8")) > 240:
        raise ValueError("filename is too long")
    return name


def confined_path(directory: Path, filename: str) -> Path:
    clean = safe_filename(filename)
    root = directory.resolve()
    candidate = root / clean
    if candidate.resolve().parent != root:
        raise ValueError("invalid file path")
    return candidate


def list_files(directory: Path) -> list[dict[str, str | int]]:
    files = []
    for path in directory.iterdir():
        if path.is_file() and not path.is_symlink() and not path.name.startswith("."):
            stat = path.stat()
            files.append({"name": path.name, "size": stat.st_size, "modified": int(stat.st_mtime)})
    return sorted(files, key=lambda item: str(item["name"]).casefold())


def delete_file(directory: Path, filename: str) -> None:
    path = confined_path(directory, filename)
    if path.is_symlink() or not path.is_file():
        raise FileNotFoundError(filename)
    path.unlink()
