#!/usr/bin/env python3
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = context.pages[0]

        print("点击 Images 标签...")
        try:
            images_tab = page.locator('button[role="tab"]:has-text("Images")').first
            await images_tab.click()
            await asyncio.sleep(1)
            print("✅ 已点击 Images 标签")
        except Exception as e:
            print(f"❌ 失败: {e}")

        await browser.close()

asyncio.run(main())
