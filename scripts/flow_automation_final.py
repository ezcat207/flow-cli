#!/usr/bin/env python3
"""
Google Flow 自动化脚本 - 添加参考图并生成图片

使用方法:
    python3 flow_automation_final.py

功能:
    1. 连接到已打开的 Chrome (CDP端口9222)
    2. 添加两张参考图：Luna_on_mars.png 和 Wayne_on_earth.png
    3. 输入生成 prompt
    4. 提交生成请求

前置条件:
    - Chrome 需要用以下命令启动:
      /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
        --remote-debugging-port=9222 \
        --user-data-dir="/tmp/flow_chrome_debug"
    - 已登录 Google 账号
    - 已打开 Flow 项目页面
"""

import asyncio
from playwright.async_api import async_playwright

# === 配置 ===
PROJECT_URL = "https://labs.google/fx/tools/flow/project/4f24835c-c783-4646-96dc-a0b8c03c34fc"
CDP_URL = "http://127.0.0.1:9222"

# 参考图文件名
REFERENCE_IMAGES = [
    "Luna_on_mars.png",
    "Wayne_on_earth.png"
]

# 生成 Prompt（可修改）
PROMPT = "他们在中国杭州玩"

# === 主函数 ===
async def main():
    print("=" * 70)
    print("Google Flow 自动化脚本")
    print("=" * 70 + "\n")
    
    async with async_playwright() as p:
        # 连接到 Chrome
        print(f"连接到 Chrome (CDP: {CDP_URL})...\n")
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        
        # 获取 Flow 项目页面
        page = None
        for p in context.pages:
            if 'flow/project' in p.url:
                page = p
                break
        
        if not page:
            print("未找到 Flow 项目页面，导航到项目...\n")
            page = await context.new_page()
            await page.goto(PROJECT_URL)
            await page.wait_for_load_state('networkidle')
        
        print(f"当前页面: {page.url}\n")
        
        # 清理环境
        print("清理对话框...\n")
        for _ in range(3):
            await page.keyboard.press('Escape')
            await asyncio.sleep(0.5)
        
        # === 步骤1 & 2: 添加参考图 ===
        for idx, img_name in enumerate(REFERENCE_IMAGES, 1):
            print("=" * 70)
            print(f"步骤 {idx}: 添加参考图 {img_name}")
            print("=" * 70 + "\n")
            
            # 打开媒体选择器（如果需要）
            # 从截图看，加号按钮位置约在 (230, 327)
            print(f"  1. 打开媒体选择器\n")
            try:
                # 尝试查找已存在的文件列表
                await page.locator(f'text=/{img_name}/i').first.is_visible(timeout=2000)
                print(f"  媒体选择器已打开\n")
            except:
                # 需要点击加号打开
                await page.mouse.click(230, 327)
                await asyncio.sleep(2)
                print(f"  媒体选择器已打开\n")
            
            # 选择文件
            print(f"  2. 选择 {img_name}\n")
            file_item = page.locator(f'text=/{img_name}/i').first
            await file_item.click()
            await asyncio.sleep(1)
            
            # 点击 Add to Prompt
            print(f"  3. 添加到 Prompt\n")
            add_btn = page.locator('button:has-text("Add to Prompt")').first
            await add_btn.click()
            await asyncio.sleep(2)
            
            print(f"✅ {img_name} 已添加\n")
        
        # === 步骤3: 输入 Prompt ===
        print("=" * 70)
        print("步骤 3: 输入生成 Prompt")
        print("=" * 70 + "\n")
        
        print(f"Prompt: '{PROMPT}'\n")
        
        # 查找输入框
        input_box = page.locator('[contenteditable="true"], textarea').first
        await input_box.click()
        await asyncio.sleep(0.5)
        await input_box.fill(PROMPT)
        await asyncio.sleep(1)
        
        print("✅ Prompt 已输入\n")
        
        # === 步骤4: 提交生成 ===
        print("=" * 70)
        print("步骤 4: 提交生成请求")
        print("=" * 70 + "\n")
        
        # 点击带箭头的 Create 按钮
        create_btn = page.locator('button:has(i:text("arrow_forward"))').first
        await create_btn.click()
        await asyncio.sleep(3)
        
        print("✅ 生成请求已提交\n")
        
        # 截图确认
        await page.screenshot(path='/tmp/flow_generation_started.png', full_page=True)
        print("📸 截图已保存: /tmp/flow_generation_started.png\n")
        
        print("=" * 70)
        print("✅ 完成！图片正在生成中...")
        print("=" * 70 + "\n")
        print("提示: 请在 Flow 界面查看生成进度\n")
        
        await browser.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n中断执行\n")
    except Exception as e:
        print(f"\n❌ 错误: {e}\n")
        import traceback
        traceback.print_exc()
