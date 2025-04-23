from pathlib import Path
import click
import pypdf
from pypdf import PdfWriter, PdfReader


class PdfSplitter:
    """Handles splitting PDFs into smaller files based on page ranges and creating even/odd page parts."""

    def __init__(
        self, pdf_path: Path, dest_path: Path, page_range: tuple[int, int], outname: str
    ):
        """
        Initialize the PDF splitter.

        Args:
            pdf_path: Path to the input PDF file.
            dest_path: Directory to save output files.
            page_range: Tuple of (start_page, end_page) (1-based indexing).
            outname: Base name for output files.
        """
        self.input_pdf = pdf_path
        self.output_dir = dest_path
        self.page_range = page_range
        self.outname = outname

        self.start_page = page_range[0]
        self.end_page = page_range[1]
        self.oname = self.output_dir.absolute() / f"{self.outname}"
        self.splitted_pdf: tuple[PdfWriter,
                                 str] = PdfWriter(), f"{self.oname}.pdf"
        self.parts: list[tuple[PdfWriter, str]] = [
            (PdfWriter(), f"{self.oname}-part0.pdf"),
            (PdfWriter(), f"{self.oname}-part1.pdf")
        ]

    def split_pdf(self, show_progress: bool = True) -> list[str]:
        """
        Extract a page range from the PDF and save it as a new file.

        Args:
            show_progress: Show a progress bar if True.

        Returns:
            The parts path for printing as strings
        """
        reader = PdfReader(self.input_pdf)
        # Convert to 0-based
        page_iter = range(self.start_page - 1, self.end_page)

        self._process_pages(reader, page_iter, show_progress)
        self._create_parts()
        self._save_files()
        paths = [x[1] for x in self.parts]
        return paths

    def _process_pages(self, reader: PdfReader, page_iter: range, show_progress: bool):
        """Process pages with optional progress bar."""
        if show_progress:
            with click.progressbar(
                page_iter,
                label="Extracting pages",
                length=len(page_iter),
                show_eta=True,
            ) as bar:
                self._add_pages_to_writer(reader, bar)
        else:
            self._add_pages_to_writer(reader, page_iter)

    def _add_pages_to_writer(self, reader: PdfReader, page_iter):
        """Add pages from reader to writer."""
        for page_num in page_iter:
            self.splitted_pdf[0].add_page(reader.pages[page_num])

    def _is_even_page_count(self) -> bool:
        """Check if the splitted PDF has an even number of pages."""
        return len(self.splitted_pdf[0].pages) % 2 == 0

    def _create_parts(self):
        """Create even/odd page parts from the splitted PDF."""
        if self._is_even_page_count():
            self._distribute_pages_evenly()
        else:
            self._handle_odd_pages()

    def _distribute_pages_evenly(self, pages=None):
        """Distribute pages evenly between parts[0] (even) and parts[1] (odd)."""
        pages = pages or self.splitted_pdf[0].pages
        with click.progressbar(pages, label='Creating part 0') as bar:
            for index, page in enumerate(bar):
                if index % 2 == 0:
                    self.parts[0][0].add_page(page)

        with click.progressbar(reversed(pages), label='Creating part 1') as bar:
            for index, page in enumerate(bar):
                if index % 2 == 0:
                    self.parts[1][0].add_page(page)

    def _handle_odd_pages(self):
        """Handle odd number of pages by putting last page in a third part."""
        self.parts.append((PdfWriter(), f'{self.oname}-part2.pdf'))
        self.parts[2][0].add_page(self.splitted_pdf[0].pages[-1])
        self._distribute_pages_evenly(self.splitted_pdf[0].pages[:-1])

    def _save_files(self):
        """Save all PDF files (main split and parts)."""
        # Save main split file
        with open(self.splitted_pdf[1], "wb") as f:
            self.splitted_pdf[0].write(f)

        # Save part files
        for i, part in enumerate(self.parts):
            with open(part[1], "wb") as f:
                part[0].write(f)
