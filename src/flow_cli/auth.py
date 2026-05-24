"""Authentication module for Flow CLI."""

import asyncio
from datetime import datetime
from typing import Optional
from playwright.async_api import async_playwright, Browser, Page
from rich.console import Console
from .config import Config
from .models import Profile


console = Console()


class FlowAuthenticator:
    """Handles authentication with Google Flow."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize authenticator.

        Args:
            config: Configuration manager. Creates new if None.
        """
        self.config = config or Config()
        self.base_url = self.config.get_config()["base_url"]

    async def login(self, profile_name: Optional[str] = None, headless: bool = False) -> Profile:
        """Authenticate with Flow via browser.

        Opens browser, navigates to Flow, waits for user to login,
        then captures and saves authentication cookies.

        Args:
            profile_name: Optional profile name/email to use.
            headless: Run browser in headless mode.

        Returns:
            Profile with authentication cookies.

        Raises:
            Exception: If authentication fails.
        """
        console.print("\n[bold cyan]Flow CLI Authentication[/bold cyan]")
        console.print("Opening browser to authenticate with Google Flow...")
        console.print("Please log in to your Google account when prompted.\n")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=headless)
            context = await browser.new_context()
            page = await context.new_page()

            try:
                # Navigate to Flow
                await page.goto(self.base_url)

                console.print(f"[yellow]Navigated to: {self.base_url}[/yellow]")
                console.print("[yellow]Waiting for you to log in...[/yellow]")
                console.print("[dim]The browser will close automatically once authenticated.[/dim]\n")

                # Wait for authentication - look for Flow-specific elements
                # These selectors need to be updated based on actual Flow UI
                await page.wait_for_selector(
                    'text="My projects", text="Create", text="Generate"',
                    timeout=300000,  # 5 minutes
                )

                # Wait a bit more to ensure cookies are set
                await asyncio.sleep(2)

                # Extract cookies
                cookies = await context.cookies()

                # Get user email from page or cookies
                email = await self._extract_email(page, cookies)

                if not email:
                    raise Exception("Could not determine user email")

                # Convert cookies to dict
                cookie_dict = {c["name"]: c["value"] for c in cookies}

                # Create profile
                now = datetime.now().isoformat()
                profile = Profile(
                    email=email,
                    cookies=cookie_dict,
                    created_at=now,
                    last_used=now,
                )

                # Save profile
                self.config.save_profile(profile)

                console.print(f"\n[bold green]✓ Successfully authenticated as: {email}[/bold green]")
                console.print(f"[dim]Profile saved to: {self.config.profiles_file}[/dim]\n")

                return profile

            finally:
                await browser.close()

    async def _extract_email(self, page: Page, cookies: list[dict]) -> Optional[str]:
        """Extract user email from page or cookies.

        Args:
            page: Playwright page.
            cookies: Browser cookies.

        Returns:
            User email if found, None otherwise.
        """
        # Try to find email in page
        try:
            # Look for email in user menu (adjust selector based on actual UI)
            email_element = await page.wait_for_selector(
                '[data-testid="user-email"], .user-email, [aria-label*="email"]',
                timeout=5000,
            )
            if email_element:
                email = await email_element.inner_text()
                if "@" in email:
                    return email.strip()
        except:
            pass

        # Try to extract from cookies
        for cookie in cookies:
            if "email" in cookie["name"].lower() or "user" in cookie["name"].lower():
                value = cookie["value"]
                if "@" in value:
                    return value

        # Fallback: ask user
        from rich.prompt import Prompt
        email = Prompt.ask("Please enter your Google account email")
        return email

    def logout(self, email: Optional[str] = None) -> bool:
        """Remove authentication profile.

        Args:
            email: Profile email to remove. If None, removes default profile.

        Returns:
            True if profile was removed, False otherwise.
        """
        if email:
            return self.config.delete_profile(email)

        # Remove default profile
        profile = self.config.get_profile()
        if profile:
            return self.config.delete_profile(profile.email)

        return False

    def get_authenticated_profile(self, email: Optional[str] = None) -> Optional[Profile]:
        """Get authenticated profile.

        Args:
            email: Profile email. If None, returns default profile.

        Returns:
            Profile if authenticated, None otherwise.
        """
        return self.config.get_profile(email)
