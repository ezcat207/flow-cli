#!/usr/bin/env python3
"""
手动完整流程 - 一步步截图记录
"""

import asyncio
from playwright.async_api import async_playwright

CDP_URL = "http://127.0.0.1:9222"


async def main():
    print("\n手动完整流程测试\n")

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

        # 步骤1: 点击 Nano Banana
        print(f"\n{'='*70}")
        print("步骤 1: 点击 Nano Banana")
        print(f"{'='*70}\n")
        try:
            nano_btn = page.locator('button:has-text("Nano Banana")').first
            await nano_btn.click()
            await asyncio.sleep(2)
            await page.screenshot(path='/tmp/flow_step_1_nano.png', full_page=True)
            print("✅ 完成 - 截图: /tmp/flow_step_1_nano.png\n")
        except Exception as e:
            print(f"❌ 失败: {e}\n")

        # 步骤2: 切换到 Video
        print(f"\n{'='*70}")
        print("步骤 2: 切换到 Video")
        print(f"{'='*70}\n")
        try:
            video_tab = page.locator('button[role="tab"]:has-text("Video")').first
            await video_tab.click()
            await asyncio.sleep(2)
            await page.screenshot(path='/tmp/flow_step_2_video.png', full_page=True)
            print("✅ 完成 - 截图: /tmp/flow_step_2_video.png\n")
        except Exception as e:
            print(f"❌ 失败: {e}\n")

        # 步骤3: 查看有什么选项
        print(f"\n{'='*70}")
        print("步骤 3: 查看 Video 模式下的选项")
        print(f"{'='*70}\n")
        tabs = page.locator('button[role="tab"]')
        tab_count = await tabs.count()
        print(f"找到 {tab_count} 个标签页：\n")
        for i in range(tab_count):
            try:
                text = await tabs.nth(i).inner_text()
                print(f"  [{i}] {text}\n")
            except:
                pass

        # 尝试点击 Ingredients
        try:
            ingredients_tab = page.locator('button[role="tab"]:has-text("Ingredients")')
            count = await ingredients_tab.count()
            if count > 0:
                print(f"\n找到 Ingredients 标签，点击它\n")
                await ingredients_tab.first.click()
                await asyncio.sleep(2)
                await page.screenshot(path='/tmp/flow_step_3_ingredients.png', full_page=True)
                print("✅ 已切换到 Ingredients - 截图: /tmp/flow_step_3_ingredients.png\n")
            else:
                print("\n未找到 Ingredients 标签\n")
        except Exception as e:
            print(f"❌ 切换 Ingredients 失败: {e}\n")

        # 步骤4: 点击加号
        print(f"\n{'='*70}")
        print("步骤 4: 点击加号")
        print(f"{'='*70}\n")
        try:
            await page.mouse.click(230, 327)
            await asyncio.sleep(3)
            await page.screenshot(path='/tmp/flow_step_4_plus.png', full_page=True)
            print("✅ 完成 - 截图: /tmp/flow_step_4_plus.png\n")
        except Exception as e:
            print(f"❌ 失败: {e}\n")

        # 步骤5: 查看媒体选择器
        print(f"\n{'='*70}")
        print("步骤 5: 查看媒体选择器")
        print(f"{'='*70}\n")

        # 查找标签
        tabs2 = page.locator('button[role="tab"]')
        tab_count2 = await tabs2.count()
        print(f"找到 {tab_count2} 个标签页：\n")
        for i in range(min(15, tab_count2)):
            try:
                text = await tabs2.nth(i).inner_text()
                is_selected = await tabs2.nth(i).get_attribute('aria-selected')
                print(f"  [{i}] {text} (selected: {is_selected})\n")
            except:
                pass

        # 查找搜索框
        print("\n查找搜索框：\n")
        search_inputs = page.locator('input')
        input_count = await search_inputs.count()
        print(f"找到 {input_count} 个输入框：\n")
        for i in range(input_count):
            try:
                input_type = await search_inputs.nth(i).get_attribute('type')
                input_id = await search_inputs.nth(i).get_attribute('id')
                placeholder = await search_inputs.nth(i).get_attribute('placeholder')
                print(f"  [{i}] type={input_type}, id={input_id}, placeholder={placeholder}\n")
            except:
                pass

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
