"""Network capture tool for reverse engineering Flow API."""

import asyncio
import json
from pathlib import Path
from typing import Optional
from datetime import datetime

from playwright.async_api import async_playwright, Route
from rich.console import Console
from rich.table import Table


console = Console()


class APICapture:
    """Captures API requests from Flow web interface."""

    def __init__(self, output_dir: Optional[Path] = None):
        """Initialize API capture tool.

        Args:
            output_dir: Directory to save captured requests. Defaults to ~/.flow-cli/captures
        """
        self.output_dir = output_dir or (Path.home() / ".flow-cli" / "captures")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.captured_requests = []

    async def capture(
        self,
        url: str = "https://labs.google/fx/tools/flow",
        duration: int = 300,
    ):
        """Capture API requests from Flow.

        Opens browser and records all network requests for analysis.

        Args:
            url: Flow URL to navigate to.
            duration: How long to capture (seconds).
        """
        console.print("\n[bold cyan]Flow API Capture Tool[/bold cyan]")
        console.print("This tool will help you reverse engineer Flow's API endpoints.\n")
        console.print("[yellow]Instructions:[/yellow]")
        console.print("1. Browser will open and navigate to Flow")
        console.print("2. Log in to your Google account")
        console.print("3. Perform actions in Flow (generate images/videos)")
        console.print("4. All API requests will be captured")
        console.print(f"5. Capture will run for {duration} seconds or until you close the browser\n")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()

            # Enable request interception
            await context.route("**/*", self._handle_request)

            page = await context.new_page()

            # Listen for responses
            page.on("response", self._handle_response)

            try:
                await page.goto(url)

                console.print(f"[green]✓ Navigated to {url}[/green]")
                console.print("[yellow]Capturing requests... Perform actions in the browser.[/yellow]\n")

                # Wait for duration or browser close
                try:
                    await asyncio.sleep(duration)
                except:
                    pass

            finally:
                await browser.close()

                # Save captured data
                await self._save_captures()

    async def _handle_request(self, route: Route):
        """Handle intercepted request."""
        request = route.request

        # Continue the request
        await route.continue_()

    async def _handle_response(self, response):
        """Handle response."""
        request = response.request

        # Filter for API requests (adjust patterns based on Flow's API)
        url = request.url
        if not any(pattern in url for pattern in ["/api/", "/v1/", "/flow/", "labs.google"]):
            return

        # Capture request details
        try:
            headers = await request.all_headers()
            post_data = request.post_data

            response_headers = await response.all_headers()

            # Try to get response body
            try:
                response_body = await response.text()
            except:
                response_body = None

            capture = {
                "timestamp": datetime.now().isoformat(),
                "request": {
                    "method": request.method,
                    "url": url,
                    "headers": headers,
                    "post_data": post_data,
                },
                "response": {
                    "status": response.status,
                    "status_text": response.status_text,
                    "headers": response_headers,
                    "body": response_body,
                },
            }

            self.captured_requests.append(capture)

            # Print summary
            console.print(
                f"[dim]Captured: {request.method} {url[:80]}... ({response.status})[/dim]"
            )

        except Exception as e:
            console.print(f"[red]Error capturing request: {e}[/red]")

    async def _save_captures(self):
        """Save captured requests to file."""
        if not self.captured_requests:
            console.print("[yellow]No API requests captured[/yellow]")
            return

        # Save to JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"capture_{timestamp}.json"

        with output_file.open("w") as f:
            json.dump(self.captured_requests, f, indent=2)

        console.print(f"\n[bold green]✓ Saved {len(self.captured_requests)} requests to:[/bold green]")
        console.print(f"[cyan]{output_file}[/cyan]\n")

        # Show summary
        self._show_summary()

    def _show_summary(self):
        """Show summary of captured requests."""
        if not self.captured_requests:
            return

        # Group by endpoint
        endpoints = {}
        for capture in self.captured_requests:
            method = capture["request"]["method"]
            url = capture["request"]["url"]

            # Extract path
            from urllib.parse import urlparse
            parsed = urlparse(url)
            path = parsed.path

            key = f"{method} {path}"
            if key not in endpoints:
                endpoints[key] = []
            endpoints[key].append(capture)

        # Create table
        table = Table(title="Captured API Endpoints")
        table.add_column("Method", style="cyan", no_wrap=True)
        table.add_column("Path", style="white")
        table.add_column("Count", style="green", justify="right")

        for key, captures in sorted(endpoints.items()):
            method, path = key.split(" ", 1)
            table.add_row(method, path, str(len(captures)))

        console.print(table)

        # Show next steps
        console.print("\n[bold yellow]Next Steps:[/bold yellow]")
        console.print("1. Review the captured JSON file")
        console.print("2. Identify the endpoints for:")
        console.print("   - Image generation")
        console.print("   - Video generation")
        console.print("   - Job status checking")
        console.print("   - Asset listing/download")
        console.print("3. Update src/flow_cli/client.py with the correct endpoints")
        console.print("4. Update request/response formats based on captured data\n")


async def run_capture():
    """Run API capture tool."""
    capture = APICapture()
    await capture.capture()


if __name__ == "__main__":
    asyncio.run(run_capture())
