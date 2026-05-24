"""Configuration management for Flow CLI."""

import json
from pathlib import Path
from typing import Optional
from datetime import datetime
from .models import Profile


class Config:
    """Configuration manager for Flow CLI."""

    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize configuration manager.

        Args:
            config_dir: Configuration directory. Defaults to ~/.flow-cli
        """
        self.config_dir = config_dir or Path.home() / ".flow-cli"
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.profiles_file = self.config_dir / "profiles.json"
        self.config_file = self.config_dir / "config.json"

        # Create default config if not exists
        if not self.config_file.exists():
            self._create_default_config()

    def _create_default_config(self) -> None:
        """Create default configuration file."""
        default_config = {
            "default_profile": None,
            "base_url": "https://labs.google.com/fx/tools/flow",
            "api_base_url": "https://labs.google.com/api/flow/v1",  # Placeholder - needs reverse engineering
            "timeout": 300,
            "max_retries": 3,
        }
        self.config_file.write_text(json.dumps(default_config, indent=2))

    def get_config(self) -> dict:
        """Get configuration."""
        return json.loads(self.config_file.read_text())

    def update_config(self, **kwargs) -> None:
        """Update configuration."""
        config = self.get_config()
        config.update(kwargs)
        self.config_file.write_text(json.dumps(config, indent=2))

    def list_profiles(self) -> list[Profile]:
        """List all profiles."""
        if not self.profiles_file.exists():
            return []

        data = json.loads(self.profiles_file.read_text())
        return [Profile(**profile) for profile in data.get("profiles", [])]

    def get_profile(self, email: Optional[str] = None) -> Optional[Profile]:
        """Get profile by email or default profile.

        Args:
            email: Profile email. If None, returns default profile.

        Returns:
            Profile if found, None otherwise.
        """
        profiles = self.list_profiles()

        if not profiles:
            return None

        if email:
            for profile in profiles:
                if profile.email == email:
                    return profile
            return None

        # Get default profile
        config = self.get_config()
        default_email = config.get("default_profile")

        if default_email:
            for profile in profiles:
                if profile.email == default_email:
                    return profile

        # Return first profile if no default
        return profiles[0] if profiles else None

    def save_profile(self, profile: Profile) -> None:
        """Save or update profile.

        Args:
            profile: Profile to save.
        """
        profiles = self.list_profiles()

        # Update existing or add new
        found = False
        for i, p in enumerate(profiles):
            if p.email == profile.email:
                profiles[i] = profile
                found = True
                break

        if not found:
            profiles.append(profile)

        # Save to file
        data = {"profiles": [p.model_dump() for p in profiles]}
        self.profiles_file.write_text(json.dumps(data, indent=2))

        # Set as default if first profile
        config = self.get_config()
        if config.get("default_profile") is None:
            self.update_config(default_profile=profile.email)

    def delete_profile(self, email: str) -> bool:
        """Delete profile.

        Args:
            email: Profile email.

        Returns:
            True if deleted, False if not found.
        """
        profiles = self.list_profiles()

        new_profiles = [p for p in profiles if p.email != email]

        if len(new_profiles) == len(profiles):
            return False

        # Save updated list
        data = {"profiles": [p.model_dump() for p in new_profiles]}
        self.profiles_file.write_text(json.dumps(data, indent=2))

        # Update default if deleted
        config = self.get_config()
        if config.get("default_profile") == email:
            new_default = new_profiles[0].email if new_profiles else None
            self.update_config(default_profile=new_default)

        return True

    def set_default_profile(self, email: str) -> bool:
        """Set default profile.

        Args:
            email: Profile email.

        Returns:
            True if set, False if profile not found.
        """
        profile = self.get_profile(email)
        if not profile:
            return False

        self.update_config(default_profile=email)
        return True
