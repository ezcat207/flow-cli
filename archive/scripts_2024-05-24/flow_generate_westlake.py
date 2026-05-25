#!/usr/bin/env python3
"""Flow 自动化 - Luna & Wayne @ 杭州西湖"""
import asyncio
from playwright.async_api import async_playwright

PROJECT_URL = "https://labs.google/fx/tools/flow/project/4f24835c-c783-4646-96dc-a0b8c03c34fc"
CDP_URL = "http://127.0.0.1:9222"
CHARACTERS = ["luna", "wayne"]

PROMPT_TEXT = """\
杭州西湖，日式插画风格，柔和梦幻的色调
Luna 站在小船上，微风吹动发梢和裙摆，眺望远方，开心享受的表情
Wayne 坐在船头船桨放下，侧身看向Luna，露出温柔微笑
湖面波光粼粼，远处有断桥、雷峰塔和连绵群山
画面纯净，没有任何文字和标志"""

async def main():
    print("=" * 60)
    print("Flow - Luna & Wayne @ 杭州西湖")
    print("=" * 60)

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = await context.new_page()

        # Fresh navigation to clear state
        print("\n[0] 加载项目页面...")
        await page.goto(PROJECT_URL)
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)
        print("    页面已加载")

        # Aggressive cleanup
        print("[cleanup] 关闭对话框...")
        for _ in range(10):
            await page.keyboard.press('Escape')
            await asyncio.sleep(0.2)

        # Step 1: Focus and clear input
        print("\n[1] 清空输入框...")
        input_box = page.locator('[contenteditable="true"]').first
        await input_box.click()
        await asyncio.sleep(0.5)
        await page.keyboard.press('Control+A')
        await asyncio.sleep(0.3)
        await page.keyboard.press('Backspace')
        await asyncio.sleep(0.5)
        text = await input_box.inner_text()
        print(f"    输入框: [{text.strip() or '空'}]")

        # Step 2: Add characters via @
        print("\n[2] 添加角色...")
        for idx, character in enumerate(CHARACTERS):
            print(f"  → @{character}")

            await page.keyboard.type('@')
            await asyncio.sleep(2)

            try:
                tab = page.locator('button[role="tab"]:has-text("Characters")').first
                await tab.wait_for(state="visible", timeout=5000)
                await tab.click()
                await asyncio.sleep(1.5)
            except Exception:
                pass

            try:
                opt = page.locator('[role="option"]').filter(has_text=character).first
                await opt.wait_for(state="visible", timeout=5000)
                await opt.click()
                await asyncio.sleep(1.5)

                if idx == 0:
                    btn = page.locator('button:has-text("Add to Prompt")').first
                    await btn.click()
                    await asyncio.sleep(1)
                    print(f"    ✅ {character} 已添加")
                else:
                    print(f"    ✅ {character} 已自动添加")
            except Exception as e:
                print(f"    ❌ 失败: {e}")

            for _ in range(5):
                await page.keyboard.press('Escape')
                await asyncio.sleep(0.2)
            await asyncio.sleep(0.5)

        # Step 3: Input prompt
        print("\n[3] 输入 Prompt...")
        await page.locator('[contenteditable="true"]').first.click()
        await asyncio.sleep(0.3)
        await page.keyboard.type(PROMPT_TEXT, delay=5)
        await asyncio.sleep(1)
        content = await page.locator('[contenteditable="true"]').first.inner_text()
        print(f"    已输入 {len(content)} 字符")

        # Step 4: Submit
        print("\n[4] 提交生成...")
        create_btn = page.locator('button:has(i:text("arrow_forward"))').first
        await create_btn.wait_for(state="visible", timeout=10000)
        await asyncio.sleep(0.5)
        await create_btn.click()
        await asyncio.sleep(3)
        print("    ✅ 已提交生成！")

        await page.screenshot(path='/tmp/flow_westlake_result.png', full_page=True)
        print("📸 截图: /tmp/flow_westlake_result.png")
        print("请在浏览器中查看生成进度！")

        await page.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
