#!/usr/bin/env python3
"""
简单检查当前页面状态
"""

import asyncio
from playwright.async_api import async_playwright

CDP_URL = "http://127.0.0.1:9222"


async def main():
    print("\n检查页面状态\n")

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]

        page = None
        for pg in context.pages:
            if 'flow/project' in pg.url:
                page = pg
                break

        if not page:
            page = context.pages[0]

        print(f"当前页面: {page.url}\n")

        # 直接截图
        await page.screenshot(path='/tmp/flow_current_state.png', full_page=True)
        print("📸 截图: /tmp/flow_current_state.png\n")

        # 关闭所有对话框
        print("按 Escape 清理对话框...\n")
        for _ in range(10):
            await page.keyboard.press('Escape')
            await asyncio.sleep(0.3)

        await asyncio.sleep(2)

        # 再次截图
        await page.screenshot(path='/tmp/flow_cleaned_state.png', full_page=True)
        print("📸 清理后截图: /tmp/flow_cleaned_state.png\n")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
