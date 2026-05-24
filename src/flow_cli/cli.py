"""Command-line interface for Flow CLI."""

import asyncio
import json
from pathlib import Path
from typing import Optional
from enum import Enum

import typer
from rich.console import Console
from rich.table import Table
from rich import print as rprint

from .auth import FlowAuthenticator
from .client import FlowClient
from .config import Config
from .models import (
    ImageGenerationRequest,
    VideoGenerationRequest,
    AspectRatio,
    CameraMovement,
    AssetType,
)


app = typer.Typer(
    name="flow",
    help="Command-line interface for Google Flow - AI filmmaking with Veo and Imagen",
    add_completion=True,
)

console = Console()


class OutputFormat(str, Enum):
    """Output format."""
    TEXT = "text"
    JSON = "json"


# ==========================================
# Authentication Commands
# ==========================================


@app.command()
def login(
    profile: Optional[str] = typer.Option(
        None,
        "--profile",
        "-p",
        help="Profile name/email to use",
    ),
    headless: bool = typer.Option(
        False,
        "--headless",
        help="Run browser in headless mode",
    ),
):
    """Authenticate with Google Flow.

    Opens a browser window for you to log in to your Google account.
    Authentication cookies will be saved for future use.
    """

    async def _login():
        auth = FlowAuthenticator()
        await auth.login(profile_name=profile, headless=headless)

    asyncio.run(_login())


@app.command()
def logout(
    profile: Optional[str] = typer.Option(
        None,
        "--profile",
        "-p",
        help="Profile email to remove",
    ),
):
    """Remove authentication profile."""
    auth = FlowAuthenticator()

    if auth.logout(email=profile):
        console.print("[green]✓ Profile removed successfully[/green]")
    else:
        console.print("[yellow]No profile found to remove[/yellow]")


@app.command()
def profiles():
    """List all authentication profiles."""
    config = Config()
    profiles_list = config.list_profiles()

    if not profiles_list:
        console.print("[yellow]No profiles found. Run 'flow login' to authenticate.[/yellow]")
        return

    default_email = config.get_config().get("default_profile")

    table = Table(title="Flow Profiles")
    table.add_column("Email", style="cyan")
    table.add_column("Created", style="dim")
    table.add_column("Last Used", style="dim")
    table.add_column("Default", style="green")

    for p in profiles_list:
        is_default = "✓" if p.email == default_email else ""
        table.add_row(p.email, p.created_at[:10], p.last_used[:10], is_default)

    console.print(table)


# ==========================================
# Generate Commands
# ==========================================


generate_app = typer.Typer(help="Generate images and videos")
app.add_typer(generate_app, name="generate")


@generate_app.command("image")
def generate_image(
    prompt: str = typer.Argument(..., help="Text prompt for image generation"),
    aspect_ratio: AspectRatio = typer.Option(
        AspectRatio.SQUARE,
        "--ratio",
        "-r",
        help="Image aspect ratio",
    ),
    style: Optional[str] = typer.Option(
        None,
        "--style",
        "-s",
        help="Style preset (e.g., photorealistic, artistic)",
    ),
    negative_prompt: Optional[str] = typer.Option(
        None,
        "--negative",
        "-n",
        help="Negative prompt (what to avoid)",
    ),
    seed: Optional[int] = typer.Option(
        None,
        "--seed",
        help="Random seed for reproducibility",
    ),
    wait: bool = typer.Option(
        True,
        "--wait/--no-wait",
        help="Wait for generation to complete",
    ),
    output: OutputFormat = typer.Option(
        OutputFormat.TEXT,
        "--output",
        "-o",
        help="Output format",
    ),
    download_to: Optional[Path] = typer.Option(
        None,
        "--download",
        "-d",
        help="Download path for generated image",
    ),
):
    """Generate an image using Imagen."""

    async def _generate():
        request = ImageGenerationRequest(
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            style=style,
            negative_prompt=negative_prompt,
            seed=seed,
        )

        async with FlowClient() as client:
            job = await client.generate_image(request)

            if output == OutputFormat.JSON:
                rprint(job.model_dump_json(indent=2))
            else:
                console.print(f"\n[bold]Job ID:[/bold] {job.id}")
                console.print(f"[bold]Status:[/bold] {job.status.value}")
                console.print(f"[bold]Prompt:[/bold] {job.prompt}\n")

            if wait:
                console.print("[yellow]Waiting for generation to complete...[/yellow]")
                completed_job = await client.wait_for_job(job.id)

                if completed_job.asset_id and download_to:
                    await client.download_asset(completed_job.asset_id, download_to)

                if output == OutputFormat.JSON:
                    rprint(completed_job.model_dump_json(indent=2))

    asyncio.run(_generate())


@generate_app.command("video")
def generate_video(
    prompt: str = typer.Argument(..., help="Text prompt for video generation"),
    duration: int = typer.Option(
        5,
        "--duration",
        "-d",
        min=1,
        max=10,
        help="Video duration in seconds",
    ),
    aspect_ratio: AspectRatio = typer.Option(
        AspectRatio.LANDSCAPE,
        "--ratio",
        "-r",
        help="Video aspect ratio",
    ),
    camera_movement: Optional[CameraMovement] = typer.Option(
        None,
        "--camera",
        "-c",
        help="Camera movement type",
    ),
    from_image: Optional[Path] = typer.Option(
        None,
        "--from-image",
        "-i",
        help="Input image for image-to-video",
    ),
    seed: Optional[int] = typer.Option(
        None,
        "--seed",
        help="Random seed for reproducibility",
    ),
    wait: bool = typer.Option(
        True,
        "--wait/--no-wait",
        help="Wait for generation to complete",
    ),
    output: OutputFormat = typer.Option(
        OutputFormat.TEXT,
        "--output",
        "-o",
        help="Output format",
    ),
    download_to: Optional[Path] = typer.Option(
        None,
        "--download",
        help="Download path for generated video",
    ),
):
    """Generate a video using Veo."""

    async def _generate():
        request = VideoGenerationRequest(
            prompt=prompt,
            duration=duration,
            aspect_ratio=aspect_ratio,
            camera_movement=camera_movement,
            from_image=str(from_image) if from_image else None,
            seed=seed,
        )

        async with FlowClient() as client:
            job = await client.generate_video(request)

            if output == OutputFormat.JSON:
                rprint(job.model_dump_json(indent=2))
            else:
                console.print(f"\n[bold]Job ID:[/bold] {job.id}")
                console.print(f"[bold]Status:[/bold] {job.status.value}")
                console.print(f"[bold]Prompt:[/bold] {job.prompt}\n")

            if wait:
                console.print("[yellow]Waiting for generation to complete...[/yellow]")
                completed_job = await client.wait_for_job(job.id)

                if completed_job.asset_id and download_to:
                    await client.download_asset(completed_job.asset_id, download_to)

                if output == OutputFormat.JSON:
                    rprint(completed_job.model_dump_json(indent=2))

    asyncio.run(_generate())


# ==========================================
# Asset Management Commands
# ==========================================


@app.command("list")
def list_assets(
    asset_type: Optional[AssetType] = typer.Option(
        None,
        "--type",
        "-t",
        help="Filter by asset type",
    ),
    limit: int = typer.Option(
        50,
        "--limit",
        "-l",
        help="Maximum number of assets",
    ),
    output: OutputFormat = typer.Option(
        OutputFormat.TEXT,
        "--output",
        "-o",
        help="Output format",
    ),
):
    """List your Flow assets."""

    async def _list():
        async with FlowClient() as client:
            assets = await client.list_assets(asset_type=asset_type, limit=limit)

            if output == OutputFormat.JSON:
                data = [a.model_dump() for a in assets]
                rprint(json.dumps(data, indent=2))
            else:
                if not assets:
                    console.print("[yellow]No assets found[/yellow]")
                    return

                table = Table(title=f"Flow Assets ({len(assets)})")
                table.add_column("ID", style="cyan", no_wrap=True)
                table.add_column("Type", style="magenta")
                table.add_column("Prompt", style="white")
                table.add_column("Status", style="green")
                table.add_column("Created", style="dim")

                for asset in assets:
                    table.add_row(
                        asset.id[:12] + "...",
                        asset.type.value,
                        asset.prompt[:50] + ("..." if len(asset.prompt) > 50 else ""),
                        asset.status.value,
                        asset.created_at[:10],
                    )

                console.print(table)

    asyncio.run(_list())


@app.command()
def download(
    asset_id: str = typer.Argument(..., help="Asset ID to download"),
    output_path: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path",
    ),
):
    """Download an asset."""

    async def _download():
        async with FlowClient() as client:
            # Get asset to determine type
            asset = await client.get_asset(asset_id)

            # Generate default filename if not provided
            if output_path is None:
                ext = "mp4" if asset.type == AssetType.VIDEO else "png"
                path = Path(f"{asset_id}.{ext}")
            else:
                path = output_path

            await client.download_asset(asset_id, path)

    asyncio.run(_download())


@app.command()
def delete(
    asset_id: str = typer.Argument(..., help="Asset ID to delete"),
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Skip confirmation",
    ),
):
    """Delete an asset."""

    async def _delete():
        if not yes:
            confirm = typer.confirm(f"Delete asset {asset_id}?")
            if not confirm:
                console.print("[yellow]Cancelled[/yellow]")
                return

        async with FlowClient() as client:
            await client.delete_asset(asset_id)

    asyncio.run(_delete())


@app.command()
def status(
    job_id: str = typer.Argument(..., help="Job ID to check"),
    output: OutputFormat = typer.Option(
        OutputFormat.TEXT,
        "--output",
        "-o",
        help="Output format",
    ),
):
    """Check job status."""

    async def _status():
        async with FlowClient() as client:
            job = await client.get_job(job_id)

            if output == OutputFormat.JSON:
                rprint(job.model_dump_json(indent=2))
            else:
                console.print(f"\n[bold]Job ID:[/bold] {job.id}")
                console.print(f"[bold]Type:[/bold] {job.type.value}")
                console.print(f"[bold]Status:[/bold] {job.status.value}")
                console.print(f"[bold]Progress:[/bold] {job.progress:.1f}%")
                console.print(f"[bold]Prompt:[/bold] {job.prompt}")

                if job.asset_id:
                    console.print(f"[bold]Asset ID:[/bold] {job.asset_id}")

                if job.error:
                    console.print(f"[bold red]Error:[/bold red] {job.error}")

                console.print()

    asyncio.run(_status())


# ==========================================
# Utility Commands
# ==========================================


@app.command()
def config_show():
    """Show current configuration."""
    config = Config()
    data = config.get_config()
    rprint(json.dumps(data, indent=2))


@app.command()
def version():
    """Show version information."""
    from . import __version__

    console.print(f"Flow CLI version {__version__}")


if __name__ == "__main__":
    app()
