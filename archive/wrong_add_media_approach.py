#!/usr/bin/env python3
"""
通过CDP连接到已登录的Chrome，添加参考图并生成
"""

import asyncio
from playwright.async_api import async_playwright

async def main():
    print("=" * 70)
    print("🎯 连接到您的Chrome并自动化操作")
    print("=" * 70 + "\n")

    async with async_playwright() as p:
        # 连接到已打开的Chrome
        print("🔗 连接到Chrome (端口9222)...\n")
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else await context.new_page()

        print(f"✅ 已连接\n")
        print(f"📍 当前页面: {page.url}\n")

        # 等待页面稳定
        await asyncio.sleep(2)

        # 添加参考图
        images = ["Luna_on_mars.png", "Wayne_on_earth.png"]

        for idx, img_name in enumerate(images, 1):
            print("=" * 70)
            print(f"第 {idx}/2 步 - 添加 {img_name}")
            print("=" * 70 + "\n")

            # 1. 打开Media库
            print("  1. 打开 Media 库...")
            try:
                await page.click('button:has-text("Add Media")', timeout=5000)
                await asyncio.sleep(3)
                print("     ✓ Media 库已打开\n")
            except Exception as e:
                print(f"     ❌ 失败: {e}\n")
                continue

            # 2. 点击Uploads标签
            print("  2. 切换到 Uploads...")
            uploads_buttons = page.locator('button:has-text("Uploads")')
            uploads_count = await uploads_buttons.count()

            for i in range(uploads_count):
                try:
                    await uploads_buttons.nth(i).click(force=True)
                    await asyncio.sleep(3)

                    # 检查是否出现文件
                    if await page.locator(f'text="{img_name}"').first.is_visible(timeout=2000):
                        print("     ✓ Uploads 已选择\n")
                        break
                except:
                    continue

            # 3. 选择图片
            print(f"  3. 选择 {img_name}...")
            try:
                await page.locator(f'text="{img_name}"').first.click(timeout=5000)
                await asyncio.sleep(4)
                print(f"     ✓ {img_name} 已选中\n")
            except Exception as e:
                print(f"     ❌ 失败: {e}\n")
                await page.keyboard.press("Escape")
                continue

            # 截图当前状态
            await page.screenshot(path=f'/tmp/cdp_selected_{idx}.png', full_page=True)
            print(f"     📸 截图: /tmp/cdp_selected_{idx}.png\n")

            # 4. 点击 Add to Prompt
            print("  4. 点击 Add to Prompt...")

            added = False
            methods = [
                ("text locator", lambda: page.locator('text="Add to Prompt"').first.click(timeout=3000)),
                ("getByText", lambda: page.get_by_text("Add to Prompt", exact=True).click(timeout=3000)),
                ("getByRole", lambda: page.get_by_role("button", name="Add to Prompt").click(timeout=3000)),
            ]

            for method_name, method_func in methods:
                try:
                    await method_func()
                    added = True
                    print(f"     ✅ 已添加 (方法: {method_name})\n")
                    break
                except:
                    continue

            # 最后尝试坐标点击
            if not added:
                print("     尝试坐标点击...")
                viewport = page.viewport_size
                if viewport:
                    x = viewport['width'] // 2
                    y = viewport['height'] - 150
                    await page.mouse.click(x, y)
                    print(f"     ✓ 已点击坐标 ({x}, {y})\n")
                    added = True

            if not added:
                print("     ⚠️  未能添加\n")

            await asyncio.sleep(2)

            # 5. 关闭Media库
            print("  5. 关闭 Media 库...")
            await page.keyboard.press("Escape")
            await asyncio.sleep(2)
            print("     ✓ 已关闭\n")

        # 输入Prompt并生成
        print("=" * 70)
        print("输入 Prompt 并生成")
        print("=" * 70 + "\n")

        prompt = "Luna and Wayne at Disneyland entrance, beautiful sunny day, vibrant colors, joyful atmosphere, high quality"
        print(f"⌨️  Prompt: {prompt}\n")

        # 查找输入框（排除recaptcha）
        all_textareas = page.locator('textarea')
        count = await all_textareas.count()

        textarea = None
        for i in range(count):
            ta = all_textareas.nth(i)

            if not await ta.is_visible():
                continue

            id_attr = await ta.get_attribute('id') or ''
            name_attr = await ta.get_attribute('name') or ''

            if 'recaptcha' not in id_attr.lower() and 'recaptcha' not in name_attr.lower():
                textarea = ta
                print(f"✓ 找到输入框 (#{i})\n")
                break

        if not textarea:
            # 尝试contenteditable
            editable = page.locator('[contenteditable="true"]').first
            if await editable.is_visible(timeout=3000):
                textarea = editable
                print("✓ 找到 contenteditable 输入框\n")

        if textarea:
            await textarea.click()
            await asyncio.sleep(0.5)
            await textarea.fill(prompt)
            await asyncio.sleep(1)
            print("✅ Prompt 已输入\n")

            # 截图
            await page.screenshot(path='/tmp/cdp_prompt_entered.png', full_page=True)
            print("📸 截图: /tmp/cdp_prompt_entered.png\n")

            # 查找Create按钮
            print("查找 Create 按钮...\n")

            all_buttons = page.locator('button')
            btn_count = await all_buttons.count()

            create_btn = None
            for i in range(btn_count):
                btn = all_buttons.nth(i)

                if not await btn.is_visible():
                    continue

                text = await btn.inner_text()
                aria_disabled = await btn.get_attribute('aria-disabled') or ''

                if 'create' in text.lower() and 'arrow' in text.lower():
                    if aria_disabled == 'false':
                        create_btn = btn
                        print(f"✓ 找到 Create 按钮 (#{i}), disabled: {aria_disabled}\n")
                        break

            if create_btn:
                print("🎨 点击 Create 生成...\n")
                await create_btn.click()
                await asyncio.sleep(3)

                print("✅ 生成已开始\n")

                print("⏳ 等待生成完成（3 分钟）...\n")

                for i in range(36):
                    await asyncio.sleep(5)

                    if (i + 1) % 6 == 0:
                        print(f"   {(i+1)*5}秒...")

                print()

                # 最终截图
                await page.screenshot(path='/tmp/cdp_final_result.png', full_page=True)
                print("📸 最终结果: /tmp/cdp_final_result.png\n")

            else:
                print("❌ 未找到 Create 按钮\n")

        else:
            print("❌ 未找到输入框\n")

        print("=" * 70)
        print("✅ 完成！")
        print("=" * 70 + "\n")

        print("您可以在Chrome中查看结果\n")
        print("浏览器保持连接，按 Ctrl+C 结束\n")

        # 保持连接，让用户查看
        await asyncio.sleep(120)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
