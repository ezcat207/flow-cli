"""MCP Server for Flow CLI integration."""

import asyncio
import json
from typing import Any, Optional
from pathlib import Path

try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    Server = None
    Tool = None
    TextContent = None

from .client import FlowClient
from .models import (
    ImageGenerationRequest,
    VideoGenerationRequest,
    AspectRatio,
    CameraMovement,
    AssetType,
)


# MCP Server instance
app = Server("flow-cli") if MCP_AVAILABLE else None


def create_mcp_server():
    """Create and configure MCP server."""
    if not MCP_AVAILABLE:
        raise ImportError(
            "MCP library not installed. Install with: pip install 'flow-cli[mcp]'"
        )

    @app.list_tools()
    async def list_tools() -> list[Tool]:
        """List available tools."""
        return [
            Tool(
                name="generate_image",
                description="Generate an image using Google Flow's Imagen model",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "Text prompt for image generation",
                        },
                        "aspect_ratio": {
                            "type": "string",
                            "enum": ["1:1", "9:16", "16:9", "21:9"],
                            "description": "Image aspect ratio",
                            "default": "1:1",
                        },
                        "style": {
                            "type": "string",
                            "description": "Style preset (e.g., photorealistic, artistic)",
                        },
                        "wait": {
                            "type": "boolean",
                            "description": "Wait for generation to complete",
                            "default": True,
                        },
                    },
                    "required": ["prompt"],
                },
            ),
            Tool(
                name="generate_video",
                description="Generate a video using Google Flow's Veo model",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "Text prompt for video generation",
                        },
                        "duration": {
                            "type": "integer",
                            "description": "Video duration in seconds (1-10)",
                            "minimum": 1,
                            "maximum": 10,
                            "default": 5,
                        },
                        "aspect_ratio": {
                            "type": "string",
                            "enum": ["1:1", "9:16", "16:9", "21:9"],
                            "description": "Video aspect ratio",
                            "default": "16:9",
                        },
                        "camera_movement": {
                            "type": "string",
                            "enum": [
                                "static",
                                "pan_left",
                                "pan_right",
                                "tilt_up",
                                "tilt_down",
                                "zoom_in",
                                "zoom_out",
                                "dolly_in",
                                "dolly_out",
                                "orbit",
                            ],
                            "description": "Camera movement type",
                        },
                        "wait": {
                            "type": "boolean",
                            "description": "Wait for generation to complete",
                            "default": True,
                        },
                    },
                    "required": ["prompt"],
                },
            ),
            Tool(
                name="list_assets",
                description="List Flow assets (images and videos)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "asset_type": {
                            "type": "string",
                            "enum": ["image", "video"],
                            "description": "Filter by asset type",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of assets to return",
                            "default": 50,
                        },
                    },
                },
            ),
            Tool(
                name="get_asset",
                description="Get details of a specific Flow asset",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "asset_id": {
                            "type": "string",
                            "description": "Asset ID",
                        },
                    },
                    "required": ["asset_id"],
                },
            ),
            Tool(
                name="download_asset",
                description="Download a Flow asset (image or video)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "asset_id": {
                            "type": "string",
                            "description": "Asset ID",
                        },
                        "output_path": {
                            "type": "string",
                            "description": "Output file path (optional)",
                        },
                    },
                    "required": ["asset_id"],
                },
            ),
            Tool(
                name="get_job_status",
                description="Check the status of a generation job",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "job_id": {
                            "type": "string",
                            "description": "Job ID",
                        },
                    },
                    "required": ["job_id"],
                },
            ),
        ]

    @app.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
        """Execute tool."""
        try:
            async with FlowClient() as client:
                if name == "generate_image":
                    return await _generate_image(client, arguments)
                elif name == "generate_video":
                    return await _generate_video(client, arguments)
                elif name == "list_assets":
                    return await _list_assets(client, arguments)
                elif name == "get_asset":
                    return await _get_asset(client, arguments)
                elif name == "download_asset":
                    return await _download_asset(client, arguments)
                elif name == "get_job_status":
                    return await _get_job_status(client, arguments)
                else:
                    return [TextContent(type="text", text=f"Unknown tool: {name}")]

        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    return app


# ==========================================
# Tool Implementations
# ==========================================


async def _generate_image(client: FlowClient, args: dict) -> list[TextContent]:
    """Generate image tool implementation."""
    request = ImageGenerationRequest(
        prompt=args["prompt"],
        aspect_ratio=AspectRatio(args.get("aspect_ratio", "1:1")),
        style=args.get("style"),
    )

    job = await client.generate_image(request)

    if args.get("wait", True):
        job = await client.wait_for_job(job.id)

        if job.asset_id:
            asset = await client.get_asset(job.asset_id)
            result = {
                "job_id": job.id,
                "status": job.status.value,
                "asset_id": asset.id,
                "url": asset.url,
                "thumbnail_url": asset.thumbnail_url,
                "prompt": asset.prompt,
            }
        else:
            result = {
                "job_id": job.id,
                "status": job.status.value,
                "error": job.error,
            }
    else:
        result = {
            "job_id": job.id,
            "status": job.status.value,
            "message": "Job submitted. Use get_job_status to check progress.",
        }

    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def _generate_video(client: FlowClient, args: dict) -> list[TextContent]:
    """Generate video tool implementation."""
    request = VideoGenerationRequest(
        prompt=args["prompt"],
        duration=args.get("duration", 5),
        aspect_ratio=AspectRatio(args.get("aspect_ratio", "16:9")),
        camera_movement=(
            CameraMovement(args["camera_movement"])
            if "camera_movement" in args
            else None
        ),
    )

    job = await client.generate_video(request)

    if args.get("wait", True):
        job = await client.wait_for_job(job.id)

        if job.asset_id:
            asset = await client.get_asset(job.asset_id)
            result = {
                "job_id": job.id,
                "status": job.status.value,
                "asset_id": asset.id,
                "url": asset.url,
                "thumbnail_url": asset.thumbnail_url,
                "prompt": asset.prompt,
            }
        else:
            result = {
                "job_id": job.id,
                "status": job.status.value,
                "error": job.error,
            }
    else:
        result = {
            "job_id": job.id,
            "status": job.status.value,
            "message": "Job submitted. Use get_job_status to check progress.",
        }

    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def _list_assets(client: FlowClient, args: dict) -> list[TextContent]:
    """List assets tool implementation."""
    asset_type = AssetType(args["asset_type"]) if "asset_type" in args else None
    limit = args.get("limit", 50)

    assets = await client.list_assets(asset_type=asset_type, limit=limit)

    result = {
        "count": len(assets),
        "assets": [
            {
                "id": a.id,
                "type": a.type.value,
                "prompt": a.prompt,
                "url": a.url,
                "thumbnail_url": a.thumbnail_url,
                "created_at": a.created_at,
                "status": a.status.value,
            }
            for a in assets
        ],
    }

    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def _get_asset(client: FlowClient, args: dict) -> list[TextContent]:
    """Get asset tool implementation."""
    asset = await client.get_asset(args["asset_id"])

    result = {
        "id": asset.id,
        "type": asset.type.value,
        "prompt": asset.prompt,
        "url": asset.url,
        "thumbnail_url": asset.thumbnail_url,
        "created_at": asset.created_at,
        "status": asset.status.value,
        "metadata": asset.metadata,
    }

    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def _download_asset(client: FlowClient, args: dict) -> list[TextContent]:
    """Download asset tool implementation."""
    asset_id = args["asset_id"]
    output_path = args.get("output_path")

    # Get asset to determine type
    asset = await client.get_asset(asset_id)

    # Generate default filename if not provided
    if output_path is None:
        ext = "mp4" if asset.type == AssetType.VIDEO else "png"
        path = Path(f"{asset_id}.{ext}")
    else:
        path = Path(output_path)

    downloaded_path = await client.download_asset(asset_id, path)

    result = {
        "asset_id": asset_id,
        "type": asset.type.value,
        "path": str(downloaded_path),
        "size_bytes": downloaded_path.stat().st_size,
    }

    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def _get_job_status(client: FlowClient, args: dict) -> list[TextContent]:
    """Get job status tool implementation."""
    job = await client.get_job(args["job_id"])

    result = {
        "job_id": job.id,
        "type": job.type.value,
        "status": job.status.value,
        "progress": job.progress,
        "prompt": job.prompt,
        "asset_id": job.asset_id,
        "error": job.error,
        "created_at": job.created_at,
        "updated_at": job.updated_at,
    }

    return [TextContent(type="text", text=json.dumps(result, indent=2))]


def main():
    """Run MCP server."""
    if not MCP_AVAILABLE:
        print("Error: MCP library not installed")
        print("Install with: pip install 'flow-cli[mcp]'")
        return

    import mcp.server.stdio

    server = create_mcp_server()
    mcp.server.stdio.run(server)


if __name__ == "__main__":
    main()
