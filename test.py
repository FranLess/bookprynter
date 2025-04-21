from pathlib import Path
import click
from click_types import PDF, PathFile, PagesRange


@click.command()
@click.option(
    "--pdf",
    prompt="Where is you pdf located? ",
    # type=PDF(),
    help="path to your file(pdf).",
)
@click.option(
    "--dest",
    prompt="Where do you want to store the output file? ",
    # type=PathFile(),
    help="output path of your modified pdf",
    default="./out",
    show_default="./out",
)
# TODO implementar validación de paginas dentro del rango del pdf
@click.option(
    "--pages_range",
    prompt="Your pages range [n-n]: ",
    type=PagesRange(),
    help="range of your the number pages from your pdf you want to print (example: 12-18)",
)
@click.option(
    "--output_name", prompt="Your output file name: ", help="output file name"
)
def cli(pdf: Path, dest: Path, pages_range: tuple[int, int]):
    """Simple program that greets NAME for a total of COUNT times."""
    click.echo(f"Your pages range is {pages_range[0]}-{pages_range[1]}")


if __name__ == "__main__":
    cli()
