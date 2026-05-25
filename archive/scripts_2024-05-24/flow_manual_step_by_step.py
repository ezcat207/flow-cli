#!/usr/bin/env python3
"""
手动操作 - 一步步执行并确认（无需交互）
"""

import asyncio
from playwright.async_api import async_playwright

CDP_URL = "http://127.0.0.1:9222"


async def main():
    print("\n=== 手动操作流程 ===\n")

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

        # ===== 步骤 0: 确保 Nano Banana 对话框已打开 =====
        print("\n【步骤 0】打开 Nano Banana 对话框\n")

        # 清理环境
        for _ in range(5):
            await page.keyboard.press('Escape')
            await asyncio.sleep(0.3)

        await asyncio.sleep(1)

        # 检查是否已经打开
        video_tab = page.locator('button[role="tab"]:has-text("Video")')
        count = await video_tab.count()

        if count == 0:
            # 需要点击 Nano Banana
            print("Nano Banana 未打开，点击按钮...\n")
            nano_btn = page.locator('button:has-text("Nano Banana")').first
            await nano_btn.click()
            await asyncio.sleep(2)
            print("✅ Nano Banana 已打开\n")
        else:
            print("✅ Nano Banana 已经打开\n")

        # 确保在 Video 模式
        print("切换到 Video 模式...\n")
        video_tab = page.locator('button[role="tab"]:has-text("Video")').first
        await video_tab.click()
        await asyncio.sleep(2)
        await page.screenshot(path='/tmp/step0_video_mode.png', full_page=True)
        print("✅ Video 模式")
        print("📸 截图: /tmp/step0_video_mode.png\n")

        # ===== 步骤 1: 点击加号 =====
        print("\n【步骤 1】点击加号（添加素材）\n")

        await page.mouse.click(230, 327)
        await asyncio.sleep(3)
        await page.screenshot(path='/tmp/step1_click_plus.png', full_page=True)
        print("✅ 已点击加号")
        print("📸 截图: /tmp/step1_click_plus.png\n")

        # ===== 步骤 2: 点击 Image 标签 =====
        print("\n【步骤 2】点击 Image 标签\n")

        # 查找 Image 标签
        image_tab = page.locator('button[role="tab"]:has-text("Images")')
        count = await image_tab.count()
        print(f"找到 {count} 个 Images 标签\n")

        if count > 0:
            await image_tab.first.click()
            await asyncio.sleep(2)
            await page.screenshot(path='/tmp/step2_click_images.png', full_page=True)
            print("✅ 已点击 Images 标签")
            print("📸 截图: /tmp/step2_click_images.png\n")
        else:
            print("❌ 未找到 Images 标签！\n")
            return

        # ===== 步骤 3: 搜索并选择图片 =====
        print("\n【步骤 3】搜索 'West Lake' 并选择图片\n")

        # 在搜索框输入
        search_box = page.locator('#quick-search-input')
        await search_box.click()
        await asyncio.sleep(1)
        await search_box.fill('')
        await search_box.type("West Lake", delay=100)
        print("✅ 已输入搜索关键词: West Lake\n")

        # 等待搜索结果
        await asyncio.sleep(4)
        await page.screenshot(path='/tmp/step3_search_results.png', full_page=True)
        print("📸 搜索结果截图: /tmp/step3_search_results.png\n")

        # 查看搜索结果
        options = page.locator('[role="option"]')
        option_count = await options.count()
        print(f"找到 {option_count} 个搜索结果\n")

        if option_count > 0:
            # 显示前几个结果
            for i in range(min(5, option_count)):
                try:
                    text = await options.nth(i).inner_text()
                    print(f"  [{i}] {text[:60]}\n")
                except:
                    pass

            # 选择第一个
            print("选择第一个结果...\n")
            await options.first.click()
            await asyncio.sleep(2)
            await page.screenshot(path='/tmp/step3_selected_image.png', full_page=True)
            print("✅ 已选择图片")
            print("📸 截图: /tmp/step3_selected_image.png\n")

            # 点击 Add to Prompt
            print("点击 Add to Prompt...\n")
            try:
                add_btn = page.locator('button:has-text("Add to Prompt")').first
                await add_btn.click()
                await asyncio.sleep(3)
                print("✅ 已添加到 Prompt\n")
            except:
                print("⚠️ Add to Prompt 可能已自动添加\n")
                await asyncio.sleep(2)
        else:
            print("❌ 没有找到搜索结果！\n")
            return

        # ===== 步骤 4: 写 Prompt =====
        print("\n【步骤 4】输入 Prompt\n")

        # 关闭搜索对话框
        await page.keyboard.press('Escape')
        await asyncio.sleep(1)

        # 聚焦输入框
        input_box = page.locator('[contenteditable="true"]').first
        await input_box.click()
        await asyncio.sleep(1)

        # 输入 Prompt
        prompt = "Wayne 是猫，Luna 是兔子，他们在西湖岸边开心地跳舞，背景是柳树和湖水，日式平面风格温暖明亮"
        print(f"输入 Prompt:\n{prompt}\n")

        await page.keyboard.type(prompt, delay=50)
        await asyncio.sleep(5)

        # 验证
        input_text = await input_box.inner_text()
        if 'Wayne' in input_text and 'Luna' in input_text and '跳舞' in input_text:
            print("✅ Prompt 验证通过\n")
            print(f"内容预览: {input_text[:150]}...\n")
        else:
            print(f"⚠️ Prompt 内容:\n{input_text[:200]}\n")

        await asyncio.sleep(3)
        await page.screenshot(path='/tmp/step4_final_prompt.png', full_page=True)
        print("📸 最终截图: /tmp/step4_final_prompt.png\n")

        # ===== 步骤 5: 提交生成 =====
        print("\n【步骤 5】提交生成\n")

        try:
            create_btn = page.locator('button:has(i:text("arrow_forward"))').first
            await create_btn.click()
            await asyncio.sleep(3)
            print("✅ 已提交生成！\n")
            await page.screenshot(path='/tmp/step5_submitted.png', full_page=True)
            print("📸 提交后截图: /tmp/step5_submitted.png\n")
        except Exception as e:
            print(f"❌ 提交失败: {e}\n")

        # ===== 完成 =====
        print("\n【完成】所有步骤已执行完毕！\n")
        print("请查看截图确认每一步是否成功\n")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())

