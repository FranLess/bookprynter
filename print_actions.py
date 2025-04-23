from pdf_process import PdfSplitter
import subprocess, os, time
import click

class PrinterActions:

        
    
    @staticmethod
    def get_available_printers() -> list[str]:
        """Get all available printers using lpstat."""
        try:
            result = subprocess.run(
                ["lpstat", "-e"],
                check=True,
                stdout=subprocess.PIPE,
                text=True
            )
            return [line.strip() for line in result.stdout.splitlines()]
        except subprocess.CalledProcessError:
            click.echo("❌ Failed to get printers list", err=True)
            return []
    
    @staticmethod
    def wait_for_print_completion(printer: str, timeout: int = 300) -> bool:
        """Wait until no jobs remain in the print queue."""
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                result = subprocess.run(
                    ["lpstat", "-o", printer],
                    stdout=subprocess.PIPE,
                    text=True
                )
                if not result.stdout.strip():
                    return True
                time.sleep(5)
            except subprocess.CalledProcessError:
                return False
        return False

    @staticmethod
    def print_pdf(printer: str, file_path: str) -> bool:
        """Print a PDF file using lp."""
        if not os.path.exists(file_path):
            click.echo(f"❌ File not found: {file_path}", err=True)
            return False
            
        try:
            subprocess.run(
                ["lp", "-d", '-o', 'print-color-mode=gray', printer, file_path],
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            click.echo(f"❌ Print failed: {e}", err=True)
            return False
         
    @classmethod
    def execute_workflow(c, parts: tuple[str, str, str]) -> None:
        """Run the complete printing workflow."""
        # Get available printers
        printers = c.get_available_printers()
        if not printers:
            click.echo('No printers available...')
            raise click.Abort()
            
        # Select printer automatically (first available)
        printer = click.prompt('Select the printer',
                               type=click.Choice(printers),
                               default=printers[0],
                               show_default=True)
        # Print Part 0
        if not parts:
            click.echo("❌ No parts provided", err=True)
            return
            
        click.echo("\n⚠️ Confirmation required ")
        for i in range(5):
            click.confirm(
                f"Please confirm more times (PRES ENTER) [{i + 1}/5]", abort=True, default=True)

        click.echo("\n🖨️ Printing Part 0...")
        if not c.print_pdf(printer, parts[0]):
            return
            
        # Wait for completion
        click.echo("⏳ Waiting for Part 0 to finish printing...")
        if not c.wait_for_print_completion(printer):
            click.echo("❌ Timed out waiting for print job", err=True)
            return

        # 5-step confirmation for remaining parts
        click.echo("\n⚠️ Confirmation required to print remaining parts")
        for i in range(5):
            click.confirm(
                f"Please confirm more times (PRES ENTER) [{i + 1}/5]", abort=True, default=True)

        # Print remaining parts
        for part_num, part_file in enumerate(parts[1:3], 1):  # Only parts 1 and 2
            if part_file and os.path.exists(part_file):
                click.echo(f"\n🖨️ Printing Part {part_num}...")
                c.print_pdf(printer, part_file)
            else:
                click.echo(f"⚠️ Part {part_num} not available, skipping")

