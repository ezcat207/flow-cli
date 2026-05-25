#!/usr/bin/env python3
"""
启动 Playwright Inspector 来录制操作
"""
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        print("连接到 Chrome...")
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')

        print("✅ 已连接")
        print("\n现在可以在 Chrome 中操作了，Playwright Inspector 会录制所有操作")
        print("操作完成后，复制生成的代码给我\n")

        page = browser.contexts[0].pages[0]

        # 打开 Inspector
        await page.pause()

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
