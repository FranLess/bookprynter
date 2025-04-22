from pathlib import Path
import click
from options_args import OPTIONS
import print_procces


# TODO implementar validación de paginas dentro del rango del pdf

@click.command()
@click.option("--pdf", **OPTIONS["pdf"])
@click.option("--dest", **OPTIONS["dest"])
@click.option("--pages_range", **OPTIONS["pages_range"])
@click.option("--output_name", **OPTIONS["output_name"])
@click.confirmation_option("--print", **OPTIONS["print"])
def cli(
    pdf: Path,
    dest: Path,
    pages_range: tuple[int, int],
    output_name: str,
):
    """Simple program that greets NAME for a total of COUNT times."""

    click.echo(f"Your document name is: {pdf.name} ({pdf.absolute()})")
    click.echo(f"Yout destination folder is: {dest.absolute()}")
    click.echo(
        f"Your printing range of the pdf is: {pages_range[0]}-{pages_range[1]}")
    click.echo(f"Your destination filename is: {output_name}")

    confimation = click.confirm("Do you want to proced?", abort=True)
    click.confirm(
        "Please confirm 3 more times (PRES ENTER) [1/3]", abort=True, default=True)
    click.confirm(
        "Please confirm 3 more times (PRES ENTER) [2/3]", abort=True, default=True)
    click.confirm(
        "Please confirm 3 more times (PRES ENTER) [3/3]", abort=True, default=True)
    a = print_procces.PdfSplitter(pdf, dest, pages_range, output_name)
    a.split_pdf()

    # TODO pdf is splitted and ready to be printed, now just print it
    # choice a printer
    # would be nice to choice a colormode too
    # print it with cups, lp document.pdf -d your_printer -o ColorMode=Monochrome
    selected_printer = click.prompt("WHICH PRINTER YOU WANT")


if __name__ == "__main__":
    cli()
