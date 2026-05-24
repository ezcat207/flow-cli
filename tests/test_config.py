"""Tests for configuration management."""

import pytest
from pathlib import Path
from flow_cli.config import Config
from flow_cli.models import Profile


@pytest.fixture
def temp_config(tmp_path):
    """Create temporary config for testing."""
    return Config(config_dir=tmp_path / ".flow-cli")


def test_create_default_config(temp_config):
    """Test default config creation."""
    assert temp_config.config_file.exists()

    config = temp_config.get_config()
    assert "base_url" in config
    assert "timeout" in config


def test_save_and_get_profile(temp_config):
    """Test saving and retrieving profiles."""
    profile = Profile(
        email="test@example.com",
        cookies={"session": "abc123"},
        created_at="2026-05-15T10:00:00Z",
        last_used="2026-05-15T10:00:00Z",
    )

    temp_config.save_profile(profile)

    retrieved = temp_config.get_profile("test@example.com")
    assert retrieved is not None
    assert retrieved.email == "test@example.com"
    assert retrieved.cookies == {"session": "abc123"}


def test_list_profiles(temp_config):
    """Test listing profiles."""
    profiles = [
        Profile(
            email=f"test{i}@example.com",
            cookies={"session": f"abc{i}"},
            created_at="2026-05-15T10:00:00Z",
            last_used="2026-05-15T10:00:00Z",
        )
        for i in range(3)
    ]

    for profile in profiles:
        temp_config.save_profile(profile)

    listed = temp_config.list_profiles()
    assert len(listed) == 3


def test_delete_profile(temp_config):
    """Test deleting a profile."""
    profile = Profile(
        email="delete@example.com",
        cookies={"session": "xyz"},
        created_at="2026-05-15T10:00:00Z",
        last_used="2026-05-15T10:00:00Z",
    )

    temp_config.save_profile(profile)
    assert temp_config.get_profile("delete@example.com") is not None

    result = temp_config.delete_profile("delete@example.com")
    assert result is True
    assert temp_config.get_profile("delete@example.com") is None


def test_default_profile(temp_config):
    """Test default profile management."""
    profile1 = Profile(
        email="first@example.com",
        cookies={"session": "1"},
        created_at="2026-05-15T10:00:00Z",
        last_used="2026-05-15T10:00:00Z",
    )

    profile2 = Profile(
        email="second@example.com",
        cookies={"session": "2"},
        created_at="2026-05-15T10:00:00Z",
        last_used="2026-05-15T10:00:00Z",
    )

    # First profile should become default
    temp_config.save_profile(profile1)
    assert temp_config.get_profile().email == "first@example.com"

    # Add second profile
    temp_config.save_profile(profile2)

    # Set second as default
    temp_config.set_default_profile("second@example.com")
    assert temp_config.get_profile().email == "second@example.com"
