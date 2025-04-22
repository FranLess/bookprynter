from click_types import PDF, PathFile, PagesRange
import click


def h(ctx: click.Context, param, value):
    if not value:
        ctx.abort()


# 1. Define options separately
OPTIONS = {
    "pdf": dict(
        prompt="Where is your pdf located? ",
        type=PDF(),
        help="path to your file (pdf).",
    ),
    "dest": dict(
        prompt="Where do you want to store the output file? ",
        type=PathFile(),
        help="output path of your modified pdf",
        default="./out",
        show_default="./out",
    ),
    "pages_range": dict(
        prompt="Your pages range [n-n]: ",
        type=PagesRange(),
        help="range of pages from your pdf (example: 12-18)",
    ),
    "output_name": dict(
        prompt="Your output file name: ",
        help="output file name",
    ),
    "print": dict(
        prompt="Do you want to print the pages?",
        help="Confirm before printing.",
        callback=h,
    )
}
