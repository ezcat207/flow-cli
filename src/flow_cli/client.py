"""Flow API client."""

import asyncio
import time
from typing import Optional, AsyncIterator
from pathlib import Path
import httpx
from rich.console import Console

from .config import Config
from .models import (
    ImageGenerationRequest,
    VideoGenerationRequest,
    Asset,
    Job,
    JobStatus,
    AssetType,
    Profile,
)


console = Console()


class FlowClient:
    """Client for Google Flow API.

    This client uses reverse-engineered endpoints from Flow's web interface.
    Endpoints may change without notice.
    """

    def __init__(
        self,
        profile: Optional[Profile] = None,
        config: Optional[Config] = None,
    ):
        """Initialize Flow client.

        Args:
            profile: Authentication profile. If None, uses default profile.
            config: Configuration manager. Creates new if None.
        """
        self.config = config or Config()

        if profile is None:
            profile = self.config.get_profile()
            if profile is None:
                raise ValueError(
                    "No authenticated profile found. Please run 'flow login' first."
                )

        self.profile = profile
        self.config_data = self.config.get_config()
        self.base_url = self.config_data.get("api_base_url", "")

        # HTTP client with cookies
        self.client = httpx.AsyncClient(
            cookies=profile.cookies,
            timeout=self.config_data.get("timeout", 300),
            follow_redirects=True,
        )

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()

    # ==========================================
    # Image Generation
    # ==========================================

    async def generate_image(
        self,
        request: ImageGenerationRequest,
    ) -> Job:
        """Generate an image.

        Args:
            request: Image generation request.

        Returns:
            Job tracking the generation.

        Note:
            This endpoint needs to be reverse-engineered from Flow's web interface.
            Update the URL and request format based on actual API.
        """
        # TODO: Update this endpoint after reverse engineering
        url = f"{self.base_url}/images/generate"

        payload = {
            "prompt": request.prompt,
            "aspectRatio": request.aspect_ratio.value,
            "style": request.style,
            "negativePrompt": request.negative_prompt,
            "seed": request.seed,
        }

        console.print(f"[yellow]Generating image: {request.prompt[:50]}...[/yellow]")

        try:
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()

            # Parse response - update based on actual API response
            job = Job(
                id=data.get("jobId", ""),
                type=AssetType.IMAGE,
                status=JobStatus.PENDING,
                prompt=request.prompt,
                created_at=data.get("createdAt", ""),
                updated_at=data.get("updatedAt", ""),
            )

            console.print(f"[green]✓ Job created: {job.id}[/green]")
            return job

        except httpx.HTTPStatusError as e:
            console.print(f"[red]✗ HTTP error: {e.response.status_code}[/red]")
            raise
        except Exception as e:
            console.print(f"[red]✗ Error: {e}[/red]")
            raise

    # ==========================================
    # Video Generation
    # ==========================================

    async def generate_video(
        self,
        request: VideoGenerationRequest,
    ) -> Job:
        """Generate a video.

        Args:
            request: Video generation request.

        Returns:
            Job tracking the generation.
        """
        # TODO: Update this endpoint after reverse engineering
        url = f"{self.base_url}/videos/generate"

        payload = {
            "prompt": request.prompt,
            "duration": request.duration,
            "aspectRatio": request.aspect_ratio.value,
            "cameraMovement": request.camera_movement.value if request.camera_movement else None,
            "seed": request.seed,
        }

        # Handle image-to-video
        if request.from_image:
            image_path = Path(request.from_image)
            if not image_path.exists():
                raise FileNotFoundError(f"Image not found: {request.from_image}")

            # Upload image first (endpoint TBD)
            image_url = await self._upload_image(image_path)
            payload["inputImage"] = image_url

        console.print(f"[yellow]Generating video: {request.prompt[:50]}...[/yellow]")

        try:
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()

            job = Job(
                id=data.get("jobId", ""),
                type=AssetType.VIDEO,
                status=JobStatus.PENDING,
                prompt=request.prompt,
                created_at=data.get("createdAt", ""),
                updated_at=data.get("updatedAt", ""),
            )

            console.print(f"[green]✓ Job created: {job.id}[/green]")
            return job

        except httpx.HTTPStatusError as e:
            console.print(f"[red]✗ HTTP error: {e.response.status_code}[/red]")
            raise
        except Exception as e:
            console.print(f"[red]✗ Error: {e}[/red]")
            raise

    async def _upload_image(self, image_path: Path) -> str:
        """Upload an image.

        Args:
            image_path: Path to image file.

        Returns:
            Uploaded image URL.
        """
        # TODO: Implement image upload endpoint
        url = f"{self.base_url}/images/upload"

        with image_path.open("rb") as f:
            files = {"file": f}
            response = await self.client.post(url, files=files)
            response.raise_for_status()
            data = response.json()
            return data.get("url", "")

    # ==========================================
    # Job Management
    # ==========================================

    async def get_job(self, job_id: str) -> Job:
        """Get job status.

        Args:
            job_id: Job ID.

        Returns:
            Job with current status.
        """
        # TODO: Update endpoint
        url = f"{self.base_url}/jobs/{job_id}"

        response = await self.client.get(url)
        response.raise_for_status()
        data = response.json()

        return Job(
            id=data.get("id", job_id),
            type=AssetType(data.get("type", "image")),
            status=JobStatus(data.get("status", "pending")),
            prompt=data.get("prompt", ""),
            progress=data.get("progress", 0.0),
            asset_id=data.get("assetId"),
            error=data.get("error"),
            created_at=data.get("createdAt", ""),
            updated_at=data.get("updatedAt", ""),
        )

    async def wait_for_job(
        self,
        job_id: str,
        poll_interval: float = 2.0,
        timeout: float = 300.0,
    ) -> Job:
        """Wait for job to complete.

        Args:
            job_id: Job ID.
            poll_interval: Polling interval in seconds.
            timeout: Maximum wait time in seconds.

        Returns:
            Completed job.

        Raises:
            TimeoutError: If job doesn't complete within timeout.
        """
        start_time = time.time()

        while True:
            job = await self.get_job(job_id)

            if job.status == JobStatus.COMPLETED:
                console.print(f"[green]✓ Job completed: {job_id}[/green]")
                return job

            if job.status == JobStatus.FAILED:
                error_msg = job.error or "Unknown error"
                console.print(f"[red]✗ Job failed: {error_msg}[/red]")
                raise Exception(f"Job failed: {error_msg}")

            elapsed = time.time() - start_time
            if elapsed > timeout:
                raise TimeoutError(f"Job {job_id} did not complete within {timeout}s")

            # Show progress
            console.print(
                f"[dim]Job {job_id}: {job.status.value} ({job.progress:.1f}%)[/dim]",
                end="\r",
            )

            await asyncio.sleep(poll_interval)

    # ==========================================
    # Asset Management
    # ==========================================

    async def list_assets(
        self,
        asset_type: Optional[AssetType] = None,
        limit: int = 50,
    ) -> list[Asset]:
        """List assets.

        Args:
            asset_type: Filter by asset type.
            limit: Maximum number of assets to return.

        Returns:
            List of assets.
        """
        # TODO: Update endpoint
        url = f"{self.base_url}/assets"

        params = {"limit": limit}
        if asset_type:
            params["type"] = asset_type.value

        response = await self.client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        assets = []
        for item in data.get("assets", []):
            asset = Asset(
                id=item.get("id", ""),
                type=AssetType(item.get("type", "image")),
                prompt=item.get("prompt", ""),
                url=item.get("url"),
                thumbnail_url=item.get("thumbnailUrl"),
                created_at=item.get("createdAt", ""),
                status=JobStatus(item.get("status", "completed")),
                metadata=item.get("metadata", {}),
            )
            assets.append(asset)

        return assets

    async def get_asset(self, asset_id: str) -> Asset:
        """Get asset by ID.

        Args:
            asset_id: Asset ID.

        Returns:
            Asset.
        """
        # TODO: Update endpoint
        url = f"{self.base_url}/assets/{asset_id}"

        response = await self.client.get(url)
        response.raise_for_status()
        data = response.json()

        return Asset(
            id=data.get("id", asset_id),
            type=AssetType(data.get("type", "image")),
            prompt=data.get("prompt", ""),
            url=data.get("url"),
            thumbnail_url=data.get("thumbnailUrl"),
            created_at=data.get("createdAt", ""),
            status=JobStatus(data.get("status", "completed")),
            metadata=data.get("metadata", {}),
        )

    async def download_asset(
        self,
        asset_id: str,
        output_path: Path,
    ) -> Path:
        """Download asset.

        Args:
            asset_id: Asset ID.
            output_path: Output file path.

        Returns:
            Path to downloaded file.
        """
        asset = await self.get_asset(asset_id)

        if not asset.url:
            raise ValueError(f"Asset {asset_id} has no download URL")

        console.print(f"[yellow]Downloading {asset.type.value}: {asset_id}[/yellow]")

        # Download file
        async with self.client.stream("GET", asset.url) as response:
            response.raise_for_status()

            output_path.parent.mkdir(parents=True, exist_ok=True)

            with output_path.open("wb") as f:
                async for chunk in response.aiter_bytes():
                    f.write(chunk)

        console.print(f"[green]✓ Downloaded to: {output_path}[/green]")
        return output_path

    async def delete_asset(self, asset_id: str) -> bool:
        """Delete asset.

        Args:
            asset_id: Asset ID.

        Returns:
            True if deleted successfully.
        """
        # TODO: Update endpoint
        url = f"{self.base_url}/assets/{asset_id}"

        response = await self.client.delete(url)
        response.raise_for_status()

        console.print(f"[green]✓ Deleted asset: {asset_id}[/green]")
        return True
