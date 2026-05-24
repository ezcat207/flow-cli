"""Tests for data models."""

import pytest
from flow_cli.models import (
    ImageGenerationRequest,
    VideoGenerationRequest,
    AspectRatio,
    CameraMovement,
    Asset,
    Job,
    JobStatus,
    AssetType,
    Profile,
)


def test_image_generation_request():
    """Test image generation request model."""
    request = ImageGenerationRequest(
        prompt="a beautiful sunset",
        aspect_ratio=AspectRatio.LANDSCAPE,
        style="photorealistic",
    )

    assert request.prompt == "a beautiful sunset"
    assert request.aspect_ratio == AspectRatio.LANDSCAPE
    assert request.style == "photorealistic"
    assert request.negative_prompt is None
    assert request.seed is None


def test_video_generation_request():
    """Test video generation request model."""
    request = VideoGenerationRequest(
        prompt="a flying drone",
        duration=5,
        aspect_ratio=AspectRatio.LANDSCAPE,
        camera_movement=CameraMovement.ZOOM_IN,
    )

    assert request.prompt == "a flying drone"
    assert request.duration == 5
    assert request.aspect_ratio == AspectRatio.LANDSCAPE
    assert request.camera_movement == CameraMovement.ZOOM_IN


def test_video_duration_validation():
    """Test video duration validation."""
    with pytest.raises(ValueError):
        VideoGenerationRequest(prompt="test", duration=0)

    with pytest.raises(ValueError):
        VideoGenerationRequest(prompt="test", duration=11)


def test_asset():
    """Test asset model."""
    asset = Asset(
        id="asset_123",
        type=AssetType.IMAGE,
        prompt="test image",
        url="https://example.com/image.png",
        created_at="2026-05-15T10:00:00Z",
        status=JobStatus.COMPLETED,
    )

    assert asset.id == "asset_123"
    assert asset.type == AssetType.IMAGE
    assert asset.status == JobStatus.COMPLETED


def test_job():
    """Test job model."""
    job = Job(
        id="job_456",
        type=AssetType.VIDEO,
        status=JobStatus.PROCESSING,
        prompt="test video",
        progress=50.0,
        created_at="2026-05-15T10:00:00Z",
        updated_at="2026-05-15T10:01:00Z",
    )

    assert job.id == "job_456"
    assert job.type == AssetType.VIDEO
    assert job.status == JobStatus.PROCESSING
    assert job.progress == 50.0


def test_profile():
    """Test profile model."""
    profile = Profile(
        email="test@example.com",
        cookies={"session": "abc123"},
        created_at="2026-05-15T10:00:00Z",
        last_used="2026-05-15T10:00:00Z",
    )

    assert profile.email == "test@example.com"
    assert "session" in profile.cookies
