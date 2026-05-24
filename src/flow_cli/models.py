"""Data models for Flow CLI."""

from enum import Enum
from typing import Optional, Literal
from pydantic import BaseModel, Field


class AspectRatio(str, Enum):
    """Supported aspect ratios."""
    SQUARE = "1:1"
    PORTRAIT = "9:16"
    LANDSCAPE = "16:9"
    WIDE = "21:9"


class CameraMovement(str, Enum):
    """Camera movement types for video generation."""
    STATIC = "static"
    PAN_LEFT = "pan_left"
    PAN_RIGHT = "pan_right"
    TILT_UP = "tilt_up"
    TILT_DOWN = "tilt_down"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"
    DOLLY_IN = "dolly_in"
    DOLLY_OUT = "dolly_out"
    ORBIT = "orbit"


class AssetType(str, Enum):
    """Asset types in Flow."""
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"


class JobStatus(str, Enum):
    """Job status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ImageGenerationRequest(BaseModel):
    """Request for image generation."""
    prompt: str = Field(..., description="Text prompt for image generation")
    aspect_ratio: AspectRatio = Field(default=AspectRatio.SQUARE, description="Image aspect ratio")
    style: Optional[str] = Field(None, description="Style preset (e.g., 'photorealistic', 'artistic')")
    negative_prompt: Optional[str] = Field(None, description="What to avoid in the generation")
    seed: Optional[int] = Field(None, description="Random seed for reproducibility")


class VideoGenerationRequest(BaseModel):
    """Request for video generation."""
    prompt: str = Field(..., description="Text prompt for video generation")
    duration: int = Field(default=5, description="Video duration in seconds", ge=1, le=10)
    aspect_ratio: AspectRatio = Field(default=AspectRatio.LANDSCAPE, description="Video aspect ratio")
    camera_movement: Optional[CameraMovement] = Field(None, description="Camera movement type")
    from_image: Optional[str] = Field(None, description="Path to input image for image-to-video")
    seed: Optional[int] = Field(None, description="Random seed for reproducibility")


class Asset(BaseModel):
    """Flow asset."""
    id: str
    type: AssetType
    prompt: str
    url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    created_at: str
    status: JobStatus
    metadata: dict = Field(default_factory=dict)


class Job(BaseModel):
    """Generation job."""
    id: str
    type: AssetType
    status: JobStatus
    prompt: str
    progress: float = Field(default=0.0, ge=0.0, le=100.0)
    asset_id: Optional[str] = None
    error: Optional[str] = None
    created_at: str
    updated_at: str


class Profile(BaseModel):
    """User profile with authentication."""
    email: str
    cookies: dict[str, str]
    created_at: str
    last_used: str
