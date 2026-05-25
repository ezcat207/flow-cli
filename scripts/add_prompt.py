#!/usr/bin/env python3
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = context.pages[0]

        # Prompt 内容
        PROMPT = "Luna 是一只白色兔子，Wayne 是一只黄色柯基犬，他们在西湖岸边欢快地跳舞"

        print("1. 找到输入框...")
        input_box = page.locator('[contenteditable="true"]').first
        await input_box.click()
        await asyncio.sleep(1)

        print("2. 输入 Prompt...")
        print(f"   内容: {PROMPT}")

        # 输入 prompt（慢速输入）
        await page.keyboard.type(PROMPT, delay=30)
        await asyncio.sleep(2)

        print("✅ Prompt 已输入")

        print("\n3. 验证内容...")
        text = await input_box.inner_text()
        print(f"   当前内容: {text[:100]}...")

        print("\n4. 按回车提交...")
        await page.keyboard.press('Enter')
        await asyncio.sleep(2)

        print("✅ 已提交！视频正在生成...")

        await browser.close()

asyncio.run(main())
