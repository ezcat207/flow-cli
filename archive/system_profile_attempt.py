#!/usr/bin/env python3
"""
使用系统Chrome的Flow自动化（避免SIGTRAP）
"""

import asyncio
from playwright.async_api import async_playwright

PROJECT_ID = "4f24835c-c783-4646-96dc-a0b8c03c34fc"
PROJECT_URL = f"https://labs.google/fx/tools/flow/project/{PROJECT_ID}"
PROFILE_DIR = '/tmp/flow_chrome_profile'  # 新的profile目录

async def main():
    print("=" * 70)
    print("🎨 Flow自动化 - 使用系统Chrome")
    print("=" * 70 + "\n")

    async with async_playwright() as p:
        # 使用系统Chrome（不是Playwright的Chrome for Testing）
        print("🚀 启动系统Chrome...\n")

        context = await p.chromium.launch_persistent_context(
            PROFILE_DIR,
            headless=False,
            executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",  # 关键：使用系统Chrome
            args=['--start-maximized'],
            viewport={'width': 1920, 'height': 1080},
        )

        page = context.pages[0] if context.pages else await context.new_page()

        print("✅ 系统Chrome已启动\n")

        # 导航到项目
        print(f"📍 导航到项目...\n")
        await page.goto(PROJECT_URL)
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(3)

        # 检查是否需要登录
        if 'accounts.google.com' in page.url or 'signin' in page.url:
            print("⚠️  需要登录Google账号")
            print("请在浏览器中完成登录，登录后按Enter继续...")
            input()

            await page.goto(PROJECT_URL)
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(3)

        print(f"✅ 已进入项目页面\n")

        # 添加参考图
        images = ["Luna_on_mars.png", "Wayne_on_earth.png"]

        for idx, img_name in enumerate(images, 1):
            print("=" * 70)
            print(f"添加第 {idx}/2 个参考图: {img_name}")
            print("=" * 70 + "\n")

            # 打开Media库
            try:
                await page.click('button:has-text("Add Media")', timeout=5000)
                await asyncio.sleep(3)
                print("  ✓ Media 库已打开\n")
            except:
                print("  ❌ 未找到 Add Media 按钮\n")
                continue

            # 点击Uploads标签
            uploads_buttons = page.locator('button:has-text("Uploads")')
            for i in range(await uploads_buttons.count()):
                await uploads_buttons.nth(i).click(force=True)
                await asyncio.sleep(3)

                if await page.locator(f'text="{img_name}"').first.is_visible(timeout=2000):
                    print("  ✓ Uploads 已选择\n")
                    break

            # 选择图片
            try:
                await page.locator(f'text="{img_name}"').first.click(timeout=5000)
                await asyncio.sleep(4)
                print(f"  ✓ {img_name} 已选中\n")
            except:
                print(f"  ❌ 未找到 {img_name}\n")
                await page.keyboard.press("Escape")
                continue

            # 点击 Add to Prompt（多种方法）
            print("  尝试点击 Add to Prompt...\n")

            added = False
            for method in [
                lambda: page.locator('text="Add to Prompt"').first.click(timeout=3000),
                lambda: page.get_by_text("Add to Prompt").click(timeout=3000),
                lambda: page.get_by_role("button", name="Add to Prompt").click(timeout=3000),
            ]:
                try:
                    await method()
                    added = True
                    print("  ✅ 已添加\n")
                    break
                except:
                    continue

            if not added:
                # 坐标点击作为最后手段
                viewport = page.viewport_size
                if viewport:
                    await page.mouse.click(viewport['width'] // 2, viewport['height'] - 150)
                    print("  ✓ 已点击（坐标方式）\n")

            await asyncio.sleep(2)
            await page.keyboard.press("Escape")
            await asyncio.sleep(2)

        # 输入Prompt并生成
        print("=" * 70)
        print("输入Prompt并生成")
        print("=" * 70 + "\n")

        prompt = "Luna and Wayne at Disneyland entrance, beautiful sunny day, vibrant colors, joyful atmosphere, high quality"

        textarea = page.locator('textarea').first
        await textarea.click()
        await textarea.fill(prompt)
        await asyncio.sleep(1)

        print(f"✓ Prompt已输入: {prompt}\n")

        # 点击Create
        create_btn = page.locator('button').filter(has_text="Create").filter(has_text="arrow").first
        await create_btn.click()

        print("🎨 生成中...\n")

        # 等待3分钟
        for i in range(36):
            await asyncio.sleep(5)
            if (i + 1) % 6 == 0:
                print(f"  {(i+1)*5}秒...")

        # 截图
        await page.screenshot(path='/tmp/final_chrome_result.png', full_page=True)
        print(f"\n✅ 完成！截图: /tmp/final_chrome_result.png\n")

        print("浏览器保持打开2分钟...\n")
        await asyncio.sleep(120)

        await context.close()


if __name__ == "__main__":
    asyncio.run(main())
