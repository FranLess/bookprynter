import click
from pathlib import Path


from pathlib import Path
import click
from typing import Tuple


class BasePathValidator(click.ParamType):
    """Base class for path validation with common functionality."""


    def validate_path(self, path: Path) -> Tuple[bool, str]:
        """Common path validation logic to be implemented by subclasses."""
        raise NotImplementedError

    def convert(self, value, param, ctx) -> Path:
        path = Path(value)
        is_valid, message = self.validate_path(path)

        if not is_valid:
            self.fail(
                f"{message}\nPath searched: {path.absolute()}",
                param,
                ctx,
            )
        return path


class PDF(BasePathValidator):
    """Validates that a path points to an existing PDF file."""
    name = "filepath"

    @staticmethod
    def validate_path(path: Path) -> Tuple[bool, str]:
        if not path.exists():
            return False, "Path/file not found"
        if not path.is_file():
            return False, "Path must be a file"
        if not path.name.lower().endswith(".pdf"):
            return False, "File must be a PDF"
        return True, ""


class PathFile(BasePathValidator):
    """Validates that a path points to an existing directory."""
    name = "dest"

    @staticmethod
    def validate_path(path: Path) -> Tuple[bool, str]:
        if not path.exists():
            return False, "Path not found"
        if path.is_file():
            return False, "Path must be a directory, not a file"
        return True, ""


class PagesRange(click.ParamType):
    """Validates and converts page range input (e.g., '12-14')."""
    name = "pages_range"

    def convert(self, value, param, ctx) -> Tuple[int, int]:
        if isinstance(value, tuple) and len(value) == 2:
            return value

        try:
            if isinstance(value, str):
                start, end = map(int, value.split("-"))
                return start, end
        except (ValueError, AttributeError):
            pass

        self.fail(
            "Invalid range format. Please use 'start-end' (e.g., '12-14')",
            param,
            ctx,
        )
