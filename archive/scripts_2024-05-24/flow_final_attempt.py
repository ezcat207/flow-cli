#!/usr/bin/env python3
"""
最终尝试 - 点击底部面板的 + Agent 按钮
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

        print("=== 开始操作 ===\n")

        # 步骤 1: 点击底部面板的 + Agent 按钮
        print("【步骤 1】点击底部面板的 + Agent 按钮\n")

        add_buttons = page.locator('button:has(i:text("add"))')
        count = await add_buttons.count()
        print(f"找到 {count} 个 add 按钮\n")

        if count >= 2:
            # 点击第二个（底部的）
            print("点击第2个（底部面板的 add 按钮）...\n")
            await add_buttons.nth(1).click()
            await asyncio.sleep(3)
            await page.screenshot(path='/tmp/final_step1.png', full_page=True)
            print("✅ 已点击\n")
            print("📸 截图: /tmp/final_step1.png\n")
        else:
            print("❌ 找不到足够的 add 按钮\n")
            await browser.close()
            return

        # 步骤 2: 查看是否打开了媒体选择器
        print("【步骤 2】查看是否打开了媒体选择器\n")

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
        search_box = page.locator('#quick-search-input')
        search_count = await search_box.count()
        print(f"\n找到 {search_count} 个搜索框\n")

        if tab_count > 0 and search_count > 0:
            print("✅ 媒体选择器已打开！\n")

            # 步骤 3: 点击 Images 标签
            print("【步骤 3】点击 Images 标签\n")
            images_tab = page.locator('button[role="tab"]:has-text("Images")').first
            await images_tab.click()
            await asyncio.sleep(2)
            print("✅ 已切换到 Images\n")

            # 步骤 4: 搜索图片
            print("【步骤 4】搜索 West Lake\n")
            await search_box.click()
            await asyncio.sleep(1)
            await search_box.fill("")
            await search_box.type("West Lake", delay=100)
            await asyncio.sleep(4)
            await page.screenshot(path='/tmp/final_step4_search.png', full_page=True)
            print("✅ 已搜索\n")
            print("📸 截图: /tmp/final_step4_search.png\n")

            # 查看搜索结果
            options = page.locator('[role="option"]')
            option_count = await options.count()
            print(f"找到 {option_count} 个搜索结果\n")

            if option_count > 0:
                # 显示前几个
                for i in range(min(3, option_count)):
                    try:
                        text = await options.nth(i).inner_text()
                        print(f"  [{i}] {text[:60]}\n")
                    except:
                        pass

                # 选择第一个
                print("\n【步骤 5】选择第一个结果\n")
                await options.first.click()
                await asyncio.sleep(2)
                print("✅ 已选择图片\n")

                # 点击 Add to Prompt
                try:
                    add_btn = page.locator('button:has-text("Add to Prompt")').first
                    await add_btn.click()
                    await asyncio.sleep(3)
                    print("✅ 已添加到 Prompt\n")
                except:
                    print("⚠️ 可能已自动添加\n")
                    await asyncio.sleep(2)

                # 关闭对话框
                await page.keyboard.press('Escape')
                await asyncio.sleep(1)

                # 步骤 6: 输入 Prompt
                print("\n【步骤 6】输入 Prompt\n")
                input_box = page.locator('[contenteditable="true"]').first
                await input_box.click()
                await asyncio.sleep(1)

                prompt = "Wayne 是猫，Luna 是兔子，他们在西湖岸边开心地跳舞，背景是柳树和湖水，日式平面风格温暖明亮"
                print(f"Prompt: {prompt}\n")

                await page.keyboard.type(prompt, delay=50)
                await asyncio.sleep(5)

                # 验证
                input_text = await input_box.inner_text()
                if 'Wayne' in input_text and 'Luna' in input_text:
                    print("✅ Prompt 验证通过\n")
                else:
                    print(f"⚠️ 内容: {input_text[:200]}\n")

                await asyncio.sleep(3)
                await page.screenshot(path='/tmp/final_step6_prompt.png', full_page=True)
                print("📸 截图: /tmp/final_step6_prompt.png\n")

                # 步骤 7: 提交
                print("\n【步骤 7】提交生成\n")
                try:
                    create_btn = page.locator('button:has(i:text("arrow_forward"))').first
                    await create_btn.click()
                    await asyncio.sleep(3)
                    print("✅ 已提交！\n")
                    await page.screenshot(path='/tmp/final_submitted.png', full_page=True)
                    print("📸 截图: /tmp/final_submitted.png\n")
                except Exception as e:
                    print(f"❌ 提交失败: {e}\n")

                print("\n=== 完成 ===\n")
            else:
                print("❌ 没有找到搜索结果\n")
        else:
            print("❌ 媒体选择器未打开\n")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
