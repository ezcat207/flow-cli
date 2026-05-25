#!/usr/bin/env python3
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]

        page = None
        for pg in context.pages:
            if 'flow/project' in pg.url:
                page = pg
                break

        if not page:
            page = context.pages[0]

        print(f"当前URL: {page.url}\n")

        # 清理
        for _ in range(5):
            await page.keyboard.press('Escape')
            await asyncio.sleep(0.3)

        await asyncio.sleep(2)

        # 截图
        await page.screenshot(path='/tmp/current_page.png', full_page=True)
        print("📸 当前页面: /tmp/current_page.png\n")

        # 查找所有按钮
        buttons = page.locator('button')
        count = await buttons.count()
        print(f"找到 {count} 个按钮\n")

        # 查找加号相关
        plus_buttons = page.locator('button:has-text("+")')
        plus_count = await plus_buttons.count()
        print(f"找到 {plus_count} 个包含 + 的按钮\n")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
