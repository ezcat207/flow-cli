#!/usr/bin/env python3
"""
尝试点击底部面板上的控件
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

        # 清理
        for _ in range(5):
            await page.keyboard.press('Escape')
            await asyncio.sleep(0.3)

        await asyncio.sleep(2)

        print("【尝试 1】点击底部面板的加号位置 (230, 327)\n")
        await page.mouse.click(230, 327)
        await asyncio.sleep(3)
        await page.screenshot(path='/tmp/try1_click_plus.png', full_page=True)
        print("📸 截图: /tmp/try1_click_plus.png\n")

        # 看看有什么标签
        tabs = page.locator('button[role="tab"]')
        count = await tabs.count()
        print(f"找到 {count} 个标签页：\n")
        for i in range(min(10, count)):
            try:
                text = await tabs.nth(i).inner_text()
                is_selected = await tabs.nth(i).get_attribute('aria-selected')
                print(f"  [{i}] {text} (selected: {is_selected})\n")
            except:
                pass

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
