#!/usr/bin/env python3
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = context.pages[0]

        # 步骤1: 找到并点击图片
        print("1. 查找 'Luna Wayne at West Lake'...")
        try:
            # 尝试多种选择器
            target = page.locator('[role="option"]:has-text("Luna Wayne at West Lake")').first
            await target.click()
            await asyncio.sleep(2)
            print("✅ 已选择图片")
        except Exception as e:
            print(f"⚠️ 方法1失败: {e}")
            try:
                # 尝试直接文本匹配
                target = page.locator('text="Luna Wayne at West Lake"').first
                await target.click()
                await asyncio.sleep(2)
                print("✅ 已选择图片（方法2）")
            except Exception as e2:
                print(f"❌ 方法2也失败: {e2}")
                await browser.close()
                return

        # 步骤2: 点击 Add to Prompt
        print("\n2. 点击 'Add to Prompt'...")
        try:
            add_btn = page.locator('button:has-text("Add to Prompt")').first
            await add_btn.click()
            await asyncio.sleep(2)
            print("✅ 已点击 Add to Prompt")
        except Exception as e:
            print(f"❌ 失败: {e}")

        await browser.close()

asyncio.run(main())
