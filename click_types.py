import click
from pathlib import Path


class PDF(click.ParamType):
    name = "filepath"

    def is_valid_pdf(path: Path) -> tuple[bool, str]:
        if not path.exists():
            return False, "path/file not found"
        if not path.is_file():
            return False, "path must be a file"
        if not path.name.endswith(".pdf"):
            return False, "file must be a pdf"

        return True, ""

    def convert(self, value, param, ctx) -> Path:
        file_path = Path(value)
        valitadion = PDF.is_valid_pdf(file_path)
        if not valitadion[0]:
            self.fail(
                f"""{valitadion[1]}
                file searched: {file_path.absolute()}""",
                param,
                ctx,
            )
        return file_path


class PathFile(click.ParamType):
    name = "dest"

    def is_valid_path(path: Path) -> tuple[bool, str]:
        if not path.exists():
            return False, "path not found"
        if path.is_file():
            return False, "path is a file"
        return True, ""

    def convert(self, value, param, ctx) -> Path:
        path = Path(value)
        validation = PathFile.is_valid_path(path)
        if not validation[0]:
            self.fail(
                f"""{validation[1]}
                path searched: {path.absolute()}""",
                param,
                ctx,
            )

        return path


class PagesRange(click.ParamType):
    name = "pages_range"

    def convert(self, value: str, param, ctx):
        if type(value) == tuple and len(value) == 2:
            return value

        try:
            pages = value.split("-")
            page_range: tuple[int, int] = int(pages[0]), int(pages[1])
        except Exception as e:
            self.fail(
                "invalid range, please insert a valid one (example 12-14)", param, ctx
            )

        return page_range
