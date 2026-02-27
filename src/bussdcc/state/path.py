from typing import Tuple

Path = Tuple[str, ...]


def parse_path(path: str) -> Path:
    if not path:
        raise ValueError("path cannot be empty")
    return tuple(path.split("."))
