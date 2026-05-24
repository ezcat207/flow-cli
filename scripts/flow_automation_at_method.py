#!/usr/bin/env python3
"""
Google Flow 自动化脚本 - 使用 @ 方式添加角色

使用方法:
    python3 flow_automation_at_method.py

功能:
    1. 连接到已打开的 Chrome (CDP端口9222)
    2. 使用 @ 方式添加角色
    3. 输入生成 prompt
    4. 提交生成请求

前置条件:
    - Chrome 需要用以下命令启动:
      ./scripts/start_chrome.sh
    - 已登录 Google 账号
    - 已打开 Flow 项目页面

优势:
    - 比加号方式更简单直接
    - 不需要处理媒体选择器
    - 支持搜索角色名称
"""

import asyncio
from playwright.async_api import async_playwright

# === 配置 ===
PROJECT_URL = "https://labs.google/fx/tools/flow/project/4f24835c-c783-4646-96dc-a0b8c03c34fc"
CDP_URL = "http://127.0.0.1:9222"

# 角色名称（使用 @ 方式添加）
CHARACTERS = [
    "luna",
    "wayne"
]

# 生成 Prompt（可修改）
PROMPT = "Luna和Wayne在美国黄石国家公园旅游探险，看到间歇泉、野牛、壮丽山景，四格漫画，日式平面风格，温馨欢乐的旅行氛围"

# === 主函数 ===
async def main():
    print("=" * 70)
    print("Google Flow 自动化脚本 - @ 方式")
    print("=" * 70 + "\n")

    async with async_playwright() as p:
        # 连接到 Chrome
        print(f"连接到 Chrome (CDP: {CDP_URL})...\n")
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]

        # 获取 Flow 项目页面
        page = None
        for pg in context.pages:
            if 'flow/project' in pg.url:
                page = pg
                break

        if not page:
            print("未找到 Flow 项目页面，导航到项目...\n")
            page = await context.new_page()
            await page.goto(PROJECT_URL)
            await page.wait_for_load_state('networkidle')

        print(f"当前页面: {page.url}\n")

        # 清理环境
        print("清理对话框...\n")
        for _ in range(5):
            await page.keyboard.press('Escape')
            await asyncio.sleep(0.5)

        # === 步骤1: 点击输入框 ===
        print("=" * 70)
        print("步骤 1: 聚焦输入框")
        print("=" * 70 + "\n")

        try:
            input_box = page.locator('[contenteditable="true"]').first
            await input_box.click()
            await asyncio.sleep(1)
            print("✅ 输入框已聚焦\n")
        except Exception as e:
            print(f"❌ 点击输入框失败: {e}\n")
            await browser.close()
            return

        # 清空输入框
        await page.keyboard.press('Control+A')
        await page.keyboard.press('Backspace')
        await asyncio.sleep(0.5)

        # === 步骤2: 使用 @ 方式添加角色 ===
        for idx, character in enumerate(CHARACTERS, 1):
            print("=" * 70)
            print(f"步骤 {idx + 1}: 添加角色 {character}")
            print("=" * 70 + "\n")

            # 输入 @ 触发搜索
            print(f"  1. 输入 @ 触发搜索\n")
            await page.keyboard.type('@')
            await asyncio.sleep(2)

            # 点击 Characters 标签页（关键步骤！）
            print(f"  2. 点击 Characters 标签页\n")
            try:
                # 使用 role="tab" 选择器，找到 Characters 标签
                characters_tab = page.locator('button[role="tab"]:has-text("Characters")').first
                await characters_tab.click()
                await asyncio.sleep(2)
                print("✅ 已切换到 Characters 标签页\n")
            except Exception as e:
                print(f"⚠️  切换到 Characters 失败: {e}\n")

            # 在 Characters 列表中选择角色
            print(f"  3. 点击 {character} 角色\n")
            try:
                # 在 Characters 视图中查找角色选项
                character_option = page.locator('[role="option"]').filter(has_text=character).first
                await character_option.click()
                await asyncio.sleep(2)
                print(f"✅ {character} 已选中\n")
            except Exception as e:
                print(f"❌ 选择 {character} 失败: {e}\n")
                continue

            # 点击 "Add to Prompt" 按钮
            print(f"  4. 点击 Add to Prompt\n")
            try:
                add_btn = page.locator('button:has-text("Add to Prompt")').first
                await add_btn.click()
                await asyncio.sleep(2)
                print(f"✅ {character} 已添加到 Prompt\n")
            except Exception as e:
                print(f"❌ 点击 Add to Prompt 失败: {e}\n")
                continue

            # 验证：检查输入框中是否显示角色名
            print(f"  5. 验证 {character} 是否正确添加\n")
            try:
                input_text = await page.locator('[contenteditable="true"]').first.inner_text()
                if character.lower() in input_text.lower():
                    print(f"✅ 验证成功：输入框中包含 '{character}'\n")
                else:
                    print(f"⚠️  警告：输入框中未找到 '{character}'")
                    print(f"    当前内容: {input_text}\n")
            except Exception as e:
                print(f"⚠️  验证时出错: {e}\n")

        # === 步骤3: 输入 Prompt ===
        print("=" * 70)
        print(f"步骤 {len(CHARACTERS) + 2}: 输入生成 Prompt")
        print("=" * 70 + "\n")

        print(f"Prompt: '{PROMPT}'\n")

        # 输入 prompt（直接在输入框输入）
        await page.keyboard.type(PROMPT)
        await asyncio.sleep(1)

        print("✅ Prompt 已输入\n")

        # === 步骤4: 提交生成 ===
        print("=" * 70)
        print(f"步骤 {len(CHARACTERS) + 3}: 提交生成请求")
        print("=" * 70 + "\n")

        # 点击带箭头的 Create 按钮
        try:
            create_btn = page.locator('button:has(i:text("arrow_forward"))').first
            await create_btn.click()
            await asyncio.sleep(3)
            print("✅ 生成请求已提交\n")
        except Exception as e:
            print(f"❌ 点击生成按钮失败: {e}\n")
            await browser.close()
            return

        # 截图确认
        await page.screenshot(path='/tmp/flow_at_method_result.png', full_page=True)
        print("📸 截图已保存: /tmp/flow_at_method_result.png\n")

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
