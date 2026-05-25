#!/usr/bin/env python3
"""
下载最新生成的视频
"""
import asyncio
import os
from datetime import datetime
from playwright.async_api import async_playwright

CDP_URL = "http://127.0.0.1:9222"
DOWNLOAD_DIR = "./downloads"

async def main():
    print("下载最新生成的视频...\n")

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = context.pages[0]

        # 创建下载目录
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)

        try:
            # 点击生成的内容
            print("1. 点击生成的内容...\n")
            generated_link = page.get_by_role("link", name="Generated image").first
            await generated_link.click()
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
            suggested_name = download.suggested_filename
            ext = os.path.splitext(suggested_name)[1] if suggested_name else ".mp4"
            filename = f"flow_download_{timestamp}{ext}"
            filepath = os.path.join(DOWNLOAD_DIR, filename)

            # 保存文件
            await download.save_as(filepath)

            print(f"\n✅ 已下载: {filepath}")
            print(f"📁 文件大小: {os.path.getsize(filepath)} bytes\n")

        except Exception as e:
            print(f"\n❌ 下载失败: {e}\n")
            print("确保：")
            print("1. 视频已经生成完成")
            print("2. 在 Flow 项目页面")
            print("3. 可以看到生成的内容\n")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
