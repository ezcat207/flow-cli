#!/usr/bin/env python3
"""
检查底部面板状态 - 是 video 还是 nano banner
"""
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

        # 清理并返回主页面
        print("清理并返回主页面...\n")
        for _ in range(10):
            await page.keyboard.press('Escape')
            await asyncio.sleep(0.3)

        await asyncio.sleep(2)
        await page.screenshot(path='/tmp/main_page.png', full_page=True)
        print("📸 主页面: /tmp/main_page.png\n")

        # 查找底部面板的文字
        print("检查底部面板状态：\n")

        # 检查是否有 "Video" 文字
        video_text = page.locator('text="Video"')
        video_count = await video_text.count()
        print(f"- 找到 {video_count} 个 'Video' 文字\n")

        # 检查是否有 "Nano Banana" 文字
        nano_text = page.locator('text="Nano Banana"')
        nano_count = await nano_text.count()
        print(f"- 找到 {nano_count} 个 'Nano Banana' 文字\n")

        if video_count > 0:
            print("✅ 底部显示 Video - 已经在 Video 模式！\n")
        elif nano_count > 0:
            print("⚠️ 底部显示 Nano Banana - 需要切换到 Video 模式\n")
        else:
            print("❓ 未找到 Video 或 Nano Banana\n")

        # 查找所有包含加号图标的按钮
        print("\n查找加号按钮：\n")

        # 尝试多种选择器
        selectors = [
            'button:has-text("+")',
            'button:has(i:text("add"))',
            'button[aria-label*="add"]',
            'button[aria-label*="Add"]',
        ]

        for selector in selectors:
            btns = page.locator(selector)
            count = await btns.count()
            if count > 0:
                print(f"  - '{selector}': 找到 {count} 个\n")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
