#!/usr/bin/env python3
"""
生成视频并自动下载
"""
import asyncio
import os
from datetime import datetime
from playwright.async_api import async_playwright

PROJECT_URL = "https://labs.google/fx/tools/flow/project/4f24835c-c783-4646-96dc-a0b8c03c34fc"
CDP_URL = "http://127.0.0.1:9222"
DOWNLOAD_DIR = "./downloads"

# 配置
CHARACTERS = ["luna", "wayne"]
PROMPT = "Luna 是一只白色兔子，Wayne 是一只猫，他们在美国大峡谷国家公园开心地玩耍探险，日式动漫风格，温暖明亮的色调"

async def generate_video(page):
    """生成视频"""
    print("=" * 70)
    print("步骤 1: 生成视频")
    print("=" * 70 + "\n")

    # 清理
    for _ in range(5):
        await page.keyboard.press('Escape')
        await asyncio.sleep(0.3)

    # 添加角色（@ 方式）
    input_box = page.locator('[contenteditable="true"]').first
    await input_box.click()
    await asyncio.sleep(1)

    # 清空
    await page.keyboard.press('Meta+A')
    await page.keyboard.press('Backspace')
    await asyncio.sleep(0.5)

    for idx, character in enumerate(CHARACTERS, 1):
        print(f"{idx}. 添加 {character}...\n")

        # 输入 @
        await page.keyboard.type('@')
        await asyncio.sleep(2)

        # 点击 Characters 标签
        characters_tab = page.locator('button[role="tab"]:has-text("Characters")').first
        await characters_tab.click()
        await asyncio.sleep(2)

        # 选择角色
        character_option = page.locator('[role="option"]').filter(has_text=character).first
        await character_option.click()
        await asyncio.sleep(2)

        # 第一个角色点击 Add to Prompt
        if idx == 1:
            add_btn = page.locator('button:has-text("Add to Prompt")').first
            await add_btn.click()
            await asyncio.sleep(2)
            print(f"✅ {character} 已添加\n")
        else:
            # 第二个角色自动添加
            await asyncio.sleep(2)
            print(f"✅ {character} 已自动添加\n")

    # 输入 Prompt
    print("2. 输入场景描述...\n")
    await page.keyboard.type(PROMPT, delay=30)
    await asyncio.sleep(3)
    print(f"✅ Prompt: {PROMPT[:60]}...\n")

    # 提交
    print("3. 提交生成...\n")
    await page.keyboard.press('Enter')
    await asyncio.sleep(3)

    print("✅ 视频生成已提交！\n")


async def wait_and_download(page):
    """等待生成完成并下载"""
    print("=" * 70)
    print("步骤 2: 等待生成完成")
    print("=" * 70 + "\n")

    print("等待 2 分钟让视频生成...\n")

    # 等待 2 分钟
    for i in range(120, 0, -10):
        print(f"剩余 {i} 秒...")
        await asyncio.sleep(10)

    print("\n生成应该完成了，开始下载...\n")

    print("=" * 70)
    print("步骤 3: 下载视频")
    print("=" * 70 + "\n")

    # 创建下载目录
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    try:
        # 点击生成的视频
        print("1. 点击生成的视频...\n")
        video_link = page.get_by_role("link", name="Generated image").first
        await video_link.click()
        await asyncio.sleep(2)

        # 点击下载按钮
        print("2. 点击下载按钮...\n")
        download_btn = page.get_by_role("button", name="download Download")
        await download_btn.click()
        await asyncio.sleep(1)

        # 选择原始尺寸并下载
        print("3. 下载原始尺寸...\n")
        async with page.expect_download() as download_info:
            await page.get_by_role("menuitem", name="1K Original size").click()

        download = await download_info.value

        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"grand_canyon_video_{timestamp}.mp4"
        filepath = os.path.join(DOWNLOAD_DIR, filename)

        # 保存文件
        await download.save_as(filepath)

        print(f"✅ 视频已下载: {filepath}\n")
        print(f"📁 文件大小: {os.path.getsize(filepath)} bytes\n")

    except Exception as e:
        print(f"❌ 下载失败: {e}\n")
        print("可能需要手动下载或调整等待时间\n")


async def main():
    print("\n" + "=" * 70)
    print("大峡谷视频生成 + 自动下载")
    print("=" * 70 + "\n")

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]

        # 获取页面
        page = None
        for pg in context.pages:
            if 'flow/project' in pg.url and '/edit/' not in pg.url:
                page = pg
                break

        if not page:
            page = context.pages[0]
            await page.goto(PROJECT_URL)
            await page.wait_for_load_state('networkidle')

        print(f"当前页面: {page.url}\n")

        # 生成视频
        await generate_video(page)

        # 等待并下载
        await wait_and_download(page)

        print("=" * 70)
        print("✅ 完成！")
        print("=" * 70 + "\n")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
