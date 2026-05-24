"""Configuration management for Flow CLI"""

import json
import os
from pathlib import Path
from typing import Optional, List

DEFAULT_CONFIG_PATH = Path.home() / ".config" / "flow-cli" / "config.json"
DEFAULT_CDP_URL = "http://127.0.0.1:9222"
DEFAULT_CHROME_PROFILE = "/tmp/flow_chrome_debug"


class Config:
    """Flow CLI configuration"""

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or DEFAULT_CONFIG_PATH
        self.data = self._load_config()

    def _load_config(self) -> dict:
        """Load configuration from file"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return self._default_config()

    def _default_config(self) -> dict:
        """Default configuration"""
        return {
            "cdp_url": DEFAULT_CDP_URL,
            "chrome_profile": DEFAULT_CHROME_PROFILE,
            "project_url": "",
            "screenshot_dir": "/tmp",
        }

    def save(self):
        """Save configuration to file"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.data, f, indent=2)

    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.data.get(key, default)

    def set(self, key: str, value):
        """Set configuration value"""
        self.data[key] = value

    def get_project_url(self) -> str:
        """Get project URL"""
        return self.data.get("project_url", "")

    def set_project_url(self, url: str):
        """Set project URL"""
        self.data["project_url"] = url

    def get_cdp_url(self) -> str:
        """Get CDP URL"""
        return self.data.get("cdp_url", DEFAULT_CDP_URL)

    def get_chrome_profile(self) -> str:
        """Get Chrome profile path"""
        return self.data.get("chrome_profile", DEFAULT_CHROME_PROFILE)

    def get_screenshot_dir(self) -> str:
        """Get screenshot directory"""
        return self.data.get("screenshot_dir", "/tmp")
