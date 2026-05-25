#!/usr/bin/env python3
"""
Debug script - 查看 Video 模式下的媒体选择器内容
"""

import asyncio
from playwright.async_api import async_playwright

CDP_URL = "http://127.0.0.1:9222"


async def main():
    print("\n调试：查看 Video 模式下 + Add 打开的内容\n")

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

        # 清理
        for _ in range(5):
            await page.keyboard.press('Escape')
            await asyncio.sleep(0.3)

        # 1. 点击 Nano Banana
        print("1. 点击 Nano Banana\n")
        nano_btn = page.locator('button:has-text("Nano Banana")').first
        await nano_btn.click()
        await asyncio.sleep(2)

        # 2. 切换到 Video
        print("2. 切换到 Video\n")
        video_tab = page.locator('button[role="tab"]:has-text("Video")').first
        await video_tab.click()
        await asyncio.sleep(2)

        # 3. 点击加号
        print("3. 点击 + Add\n")
        await page.mouse.click(230, 327)
        await asyncio.sleep(3)

        # 4. 截图看看有什么
        print("4. 截图查看媒体选择器\n")
        await page.screenshot(path='/tmp/video_media_selector.png', full_page=True)
        print("📸 截图: /tmp/video_media_selector.png\n")

        # 5. 查看所有标签页
        print("5. 查看可用的标签页\n")
        tabs = page.locator('button[role="tab"]')
        tab_count = await tabs.count()
        print(f"找到 {tab_count} 个标签页：\n")
        for i in range(tab_count):
            try:
                text = await tabs.nth(i).inner_text()
                print(f"  - {text}\n")
            except:
                pass

        # 6. 查看所有选项（options）
        print("\n6. 查看媒体选择器中的选项\n")
        options = page.locator('[role="option"]')
        option_count = await options.count()
        print(f"找到 {option_count} 个选项：\n")
        for i in range(min(10, option_count)):  # 只显示前10个
            try:
                text = await options.nth(i).inner_text()
                print(f"  [{i}] {text[:60]}\n")
            except:
                pass

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
