#!/usr/bin/env python3
"""
手动一步一步执行，每步截图
"""
import asyncio
from playwright.async_api import async_playwright

CDP_URL = "http://127.0.0.1:9222"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = context.pages[0]

        print(f"当前页面: {page.url}")

        # 截图看当前状态
        await page.screenshot(path='/tmp/step0_current.png', full_page=True)
        print("📸 当前状态: /tmp/step0_current.png")

        # 步骤1: 点击加号
        print("\n步骤1: 点击加号...")
        try:
            await page.mouse.click(230, 327)
            await asyncio.sleep(3)
            await page.screenshot(path='/tmp/step1_after_plus.png', full_page=True)
            print("✅ 步骤1完成: /tmp/step1_after_plus.png")
        except Exception as e:
            print(f"❌ 步骤1失败: {e}")
            await browser.close()
            return

        # 步骤2: 切换到 Images
        print("\n步骤2: 切换到 Images...")
        try:
            # 尝试找到 Images 标签
            images_tab = page.locator('button:has-text("Images")').first
            await images_tab.click()
            await asyncio.sleep(2)
            await page.screenshot(path='/tmp/step2_images_tab.png', full_page=True)
            print("✅ 步骤2完成: /tmp/step2_images_tab.png")
        except Exception as e:
            print(f"⚠️ 步骤2失败: {e}")
            print("尝试查找所有可能的标签...")
            await page.screenshot(path='/tmp/step2_error.png', full_page=True)

        # 步骤3: 找到 Luna Wayne at West Lake
        print("\n步骤3: 找到 Luna Wayne at West Lake...")
        try:
            # 尝试找到图片
            target = page.locator('text="Luna Wayne at West Lake"').first
            await target.click()
            await asyncio.sleep(2)
            await page.screenshot(path='/tmp/step3_selected.png', full_page=True)
            print("✅ 步骤3完成: /tmp/step3_selected.png")
        except Exception as e:
            print(f"⚠️ 步骤3失败: {e}")
            print("尝试使用搜索...")
            await page.screenshot(path='/tmp/step3_error.png', full_page=True)

        # 步骤4: 点击 Add to Prompt
        print("\n步骤4: 点击 Add to Prompt...")
        try:
            add_btn = page.locator('button:has-text("Add to Prompt")').first
            await add_btn.click()
            await asyncio.sleep(2)
            await page.screenshot(path='/tmp/step4_added.png', full_page=True)
            print("✅ 步骤4完成: /tmp/step4_added.png")
        except Exception as e:
            print(f"❌ 步骤4失败: {e}")
            await page.screenshot(path='/tmp/step4_error.png', full_page=True)

        print("\n✅ 所有步骤完成！检查截图:")
        print("  /tmp/step0_current.png")
        print("  /tmp/step1_after_plus.png")
        print("  /tmp/step2_images_tab.png")
        print("  /tmp/step3_selected.png")
        print("  /tmp/step4_added.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
