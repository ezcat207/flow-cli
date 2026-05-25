#!/usr/bin/env python3
"""
Google Flow 视频生成 - @ 方式添加角色

使用 @ 方式添加角色来生成视频，不需要参考图片

使用方法:
    python3 flow_video_at_method.py

前置条件:
    - Chrome 已启动（调试端口 9222）
    - 已登录 Google 账号
    - 已打开 Flow 项目页面
"""

import asyncio
import re
from playwright.async_api import async_playwright

# === 配置 ===
PROJECT_URL = "https://labs.google/fx/tools/flow/project/4f24835c-c783-4646-96dc-a0b8c03c34fc"
CDP_URL = "http://127.0.0.1:9222"

# 角色名称（使用 @ 方式添加）
CHARACTERS = [
    "luna",
    "wayne"
]

# 视频描述 Prompt
# ⚠️ 重要：必须单行，不能有换行！
# 必须明确说明角色物种
MOTION_PROMPT = "Luna 是一只白色兔子，Wayne 是一只猫，他们在美国大峡谷国家公园开心地探险玩耍，背景是壮观的红色峡谷和科罗拉多河，日式动漫风格"


async def ensure_video_mode(page):
    """确保在 Video 模式"""
    print("=" * 70)
    print("步骤 0: 确保在 Video 模式")
    print("=" * 70 + "\n")

    try:
        # 检查是否有 Video 标签页（说明已经在创建模式）
        video_tab = page.locator('button[role="tab"]:has-text("Video")')
        count = await video_tab.count()

        if count > 0:
            # 已经在创建模式，点击 Video 标签
            print("已在创建模式，切换到 Video 标签...\n")
            await video_tab.first.click()
            await asyncio.sleep(2)
            print("✅ 已在 Video 模式\n")
            return

        # 不在创建模式，需要点击 Nano Banana
        print("点击 Nano Banana 进入创建模式...\n")
        nano_btn = page.get_by_role("button", name=re.compile("Nano Banana", re.IGNORECASE))
        await nano_btn.click()
        await asyncio.sleep(2)

        # 切换到 Video 标签
        print("切换到 Video 标签...\n")
        video_tab = page.locator('button[role="tab"]:has-text("Video")').first
        await video_tab.click()
        await asyncio.sleep(2)

        print("✅ 已切换到 Video 模式\n")

    except Exception as e:
        print(f"⚠️ 模式切换失败: {e}")
        print("尝试继续执行...\n")


async def add_characters(page):
    """使用 @ 方式添加角色"""
    print("=" * 70)
    print("步骤 1: 添加角色（@ 方式）")
    print("=" * 70 + "\n")

    # 聚焦输入框
    print("聚焦输入框\n")
    input_box = page.locator('[contenteditable="true"]').first
    await input_box.click()
    await asyncio.sleep(1)

    # 清空
    await page.keyboard.press('Meta+A')
    await page.keyboard.press('Backspace')
    await asyncio.sleep(0.5)

    # 添加角色
    for idx, character in enumerate(CHARACTERS, 1):
        print(f"添加 {character}...\n")

        # 输入 @
        await page.keyboard.type('@')
        await asyncio.sleep(2)

        # 点击 Characters 标签
        try:
            characters_tab = page.get_by_role("tab", name=re.compile("Characters", re.IGNORECASE))
            await characters_tab.click()
            await asyncio.sleep(2)
        except Exception as e:
            print(f"⚠️  切换 Characters 失败: {e}\n")

        # 选择角色
        try:
            character_option = page.get_by_role("option").get_by_text(character, exact=False)
            await character_option.first.click()
            await asyncio.sleep(2)
        except Exception as e:
            print(f"❌ 选择 {character} 失败: {e}\n")
            raise

        # 点击 "Add to Prompt"（仅第一个角色）
        if idx == 1:
            try:
                add_btn = page.locator('button:has-text("Add to Prompt")').first
                await add_btn.click()
                await asyncio.sleep(3)
                print(f"✅ {character} 已添加\n")
            except Exception as e:
                print(f"⚠️ Add to Prompt: {e}（可能自动添加）\n")
                await asyncio.sleep(2)
        else:
            # 第二个角色自动添加
            await asyncio.sleep(3)
            print(f"✅ {character} 已自动添加\n")

    # 验证
    input_text = await input_box.inner_text()
    print(f"当前输入框内容: {input_text[:100]}...\n")


async def input_motion_prompt(page):
    """输入视频描述"""
    print("=" * 70)
    print("步骤 2: 输入视频描述")
    print("=" * 70 + "\n")

    print(f"Prompt: '{MOTION_PROMPT}'\n")

    # 聚焦输入框
    input_box = page.locator('[contenteditable="true"]').first
    await input_box.click()
    await asyncio.sleep(1)

    # 移动到末尾
    await page.keyboard.press('End')
    await asyncio.sleep(0.5)

    # 输入逗号和空格
    await page.keyboard.type(', ')
    await asyncio.sleep(0.5)

    # 输入视频描述（慢速）
    await page.keyboard.type(MOTION_PROMPT, delay=30)

    # 等待输入完成
    print("\n等待输入完成（5秒）...\n")
    await asyncio.sleep(5)

    # 验证
    input_text = await input_box.inner_text()
    if MOTION_PROMPT[:20] in input_text:
        print("✅ Prompt 已输入\n")
    else:
        print(f"⚠️ 验证: {input_text[:200]}\n")

    # 最后确认
    print("最后确认（3秒）...\n")
    await asyncio.sleep(3)


async def submit(page):
    """提交生成"""
    print("=" * 70)
    print("步骤 3: 提交视频生成")
    print("=" * 70 + "\n")

    try:
        # 按回车提交
        await page.keyboard.press('Enter')
        await asyncio.sleep(3)
        print("✅ 视频生成已提交\n")
    except Exception as e:
        print(f"❌ 提交失败: {e}\n")
        raise

    # 截图
    await page.screenshot(path='/tmp/video_at_method_submitted.png', full_page=True)
    print("📸 截图: /tmp/video_at_method_submitted.png\n")


async def main():
    print("\n" + "=" * 70)
    print("Google Flow 视频生成 - @ 方式")
    print("=" * 70 + "\n")

    async with async_playwright() as p:
        # 连接到 Chrome
        print(f"连接到 Chrome (CDP: {CDP_URL})...\n")
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]

        # 获取 Flow 页面
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

        # 执行流程
        await ensure_video_mode(page)
        await add_characters(page)
        await input_motion_prompt(page)
        await submit(page)

        print("\n" + "=" * 70)
        print("✅ 完成！视频正在生成中...")
        print("=" * 70 + "\n")
        print("💡 提示：")
        print("   - 视频生成需要约 2 分钟")
        print("   - 生成完成后运行: python3 scripts/download_video.py\n")

        await browser.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n中断执行\n")
    except Exception as e:
        print(f"\n❌ 错误: {e}\n")
        import traceback
        traceback.print_exc()
