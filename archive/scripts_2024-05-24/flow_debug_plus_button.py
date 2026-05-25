#!/usr/bin/env python3
"""
调试：查看点击加号后打开的界面
"""

import asyncio
from playwright.async_api import async_playwright

CDP_URL = "http://127.0.0.1:9222"


async def main():
    print("\n调试：Video 模式点击加号\n")

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
        print("清理对话框...\n")
        for _ in range(10):
            await page.keyboard.press('Escape')
            await asyncio.sleep(0.3)

        await asyncio.sleep(2)

        # 检查 Video 标签是否存在
        print("检查 Video 标签...\n")
        video_tab = page.locator('button[role="tab"]:has-text("Video")')
        count = await video_tab.count()

        if count > 0:
            print(f"✅ 找到 {count} 个 Video 标签\n")

            # 点击 Video 标签
            await video_tab.first.click()
            await asyncio.sleep(2)
            print("✅ 已点击 Video 标签\n")

            # 截图
            await page.screenshot(path='/tmp/flow_video_mode.png', full_page=True)
            print("📸 Video 模式截图: /tmp/flow_video_mode.png\n")
        else:
            # 可能需要先点击 Nano Banana
            print("未找到 Video 标签，尝试点击 Nano Banana\n")
            nano_btn = page.locator('button:has-text("Nano Banana")').first
            await nano_btn.click()
            await asyncio.sleep(2)

            # 再点击 Video
            video_tab = page.locator('button[role="tab"]:has-text("Video")').first
            await video_tab.click()
            await asyncio.sleep(2)
            print("✅ 已切换到 Video 模式\n")

            # 截图
            await page.screenshot(path='/tmp/flow_video_mode.png', full_page=True)
            print("📸 Video 模式截图: /tmp/flow_video_mode.png\n")

        # 点击加号
        print("点击加号按钮 (230, 327)\n")
        await page.mouse.click(230, 327)
        await asyncio.sleep(3)

        # 截图
        await page.screenshot(path='/tmp/flow_after_plus.png', full_page=True)
        print("📸 点击加号后截图: /tmp/flow_after_plus.png\n")

        # 查看有什么元素
        print("查看页面元素：\n")

        # 查找所有标签页
        tabs = page.locator('button[role="tab"]')
        tab_count = await tabs.count()
        print(f"找到 {tab_count} 个标签页\n")
        for i in range(min(10, tab_count)):
            try:
                text = await tabs.nth(i).inner_text()
                is_selected = await tabs.nth(i).get_attribute('aria-selected')
                print(f"  [{i}] {text} (selected: {is_selected})\n")
            except:
                pass

        # 查找搜索框
        print("\n查找搜索框：\n")
        search_boxes = page.locator('input[type="text"]')
        search_count = await search_boxes.count()
        print(f"找到 {search_count} 个文本输入框\n")
        for i in range(search_count):
            try:
                placeholder = await search_boxes.nth(i).get_attribute('placeholder')
                input_id = await search_boxes.nth(i).get_attribute('id')
                print(f"  [{i}] id={input_id}, placeholder={placeholder}\n")
            except:
                pass

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
