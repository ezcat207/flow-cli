#!/usr/bin/env python3
"""
Google Flow 视频生成 - Ingredients 模式

使用参考图 + 动作描述生成视频（区别于 Frames 模式的首尾帧）

完整流程：
1. 检查/切换到 Video 模式
2. 点击加号按钮打开媒体选择器
3. 切换到 Images 标签
4. 点击参考图片（自动添加到 prompt）
5. 输入动作描述（明确说明角色物种）
6. 提交生成

使用方法:
    python3 flow_video_ingredients.py

前置条件:
    - Chrome 已启动（调试端口 9222）
    - 已登录 Google 账号
    - 已打开 Flow 项目页面
"""

import asyncio
from playwright.async_api import async_playwright

# === 配置 ===
PROJECT_URL = "https://labs.google/fx/tools/flow/project/4f24835c-c783-4646-96dc-a0b8c03c34fc"
CDP_URL = "http://127.0.0.1:9222"

# 参考图片名称
REFERENCE_IMAGE = "Luna Wayne at West Lake"

# 动作描述 - 必须明确说明角色是什么动物！
# ⚠️ 重要：必须单行，不能有换行
MOTION_PROMPT = "Luna 是一只白色兔子，Wayne 是一只猫，他们在美国大峡谷国家公园开心地玩耍探险，背景是壮观的红色峡谷和科罗拉多河"


async def connect_to_chrome():
    """连接到 Chrome"""
    print(f"连接到 Chrome (CDP: {CDP_URL})...\n")
    try:
        p = await async_playwright().start()
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]

        # 获取 Flow 页面
        page = None
        for pg in context.pages:
            if 'flow/project' in pg.url:
                page = pg
                break

        if not page:
            if len(context.pages) > 0:
                page = context.pages[0]
            else:
                raise Exception("没有可用的页面")

        print(f"✅ 已连接: {page.url}\n")
        return p, browser, page

    except Exception as e:
        print(f"❌ 连接失败: {e}\n")
        raise


async def step1_ensure_video_mode(page):
    """步骤1: 确保在 Video 模式"""
    print("=" * 70)
    print("步骤 1: 检查/切换到 Video 模式")
    print("=" * 70 + "\n")

    try:
        # 先检查是否已经在 Video 模式（查找 Video 标签页）
        video_tab = page.locator('button[role="tab"]:has-text("Video")')
        count = await video_tab.count()

        if count > 0:
            print("✅ 已在 Video 模式\n")
            return

        # 如果没在 Video 模式，尝试点击 Nano Banana
        print("尝试点击 Nano Banana 切换到 Video 模式...\n")
        nano_btn = page.locator('button:has-text("Nano Banana")').first
        await nano_btn.click()
        await asyncio.sleep(2)

        # 点击 Video 标签
        video_tab = page.locator('button[role="tab"]:has-text("Video")').first
        await video_tab.click()
        await asyncio.sleep(2)
        print("✅ 已切换到 Video 模式\n")

    except Exception as e:
        print(f"⚠️ 无法切换模式: {e}")
        print("假设已经在 Video 模式，继续执行...\n")


async def step2_open_media_picker(page):
    """步骤2: 点击加号打开媒体选择器"""
    print("=" * 70)
    print("步骤 2: 点击加号打开媒体选择器")
    print("=" * 70 + "\n")

    try:
        # 点击加号按钮（坐标方式）
        await page.mouse.click(230, 327)
        await asyncio.sleep(3)
        print("✅ 媒体选择器已打开\n")
    except Exception as e:
        print(f"❌ 失败: {e}\n")
        raise


async def step3_switch_to_images(page):
    """步骤3: 切换到 Images 标签"""
    print("=" * 70)
    print("步骤 3: 切换到 Images 标签")
    print("=" * 70 + "\n")

    try:
        images_tab = page.locator('button[role="tab"]:has-text("Images")').first
        await images_tab.click()
        await asyncio.sleep(2)
        print("✅ 已切换到 Images\n")
    except Exception as e:
        print(f"❌ 失败: {e}\n")
        raise


async def step4_select_reference_image(page):
    """步骤4: 选择参考图片"""
    print("=" * 70)
    print("步骤 4: 选择参考图片")
    print("=" * 70 + "\n")

    print(f"查找图片: {REFERENCE_IMAGE}\n")

    try:
        # 方式1: 使用 role="option"
        target = page.locator(f'[role="option"]:has-text("{REFERENCE_IMAGE}")').first
        await target.click()
        await asyncio.sleep(2)
        print("✅ 图片已选择并自动添加到 prompt\n")

    except Exception as e:
        print(f"⚠️ 方式1失败: {e}\n")
        try:
            # 方式2: 直接文本匹配
            target = page.locator(f'text="{REFERENCE_IMAGE}"').first
            await target.click()
            await asyncio.sleep(2)
            print("✅ 图片已选择并自动添加到 prompt（方式2）\n")
        except Exception as e2:
            print(f"❌ 方式2也失败: {e2}\n")
            raise

    print("💡 提示: 在 Ingredients 模式下，点击图片会自动添加，")
    print("   不需要额外点击 'Add to Prompt' 按钮\n")


async def step5_input_motion_prompt(page):
    """步骤5: 输入动作描述"""
    print("=" * 70)
    print("步骤 5: 输入动作描述")
    print("=" * 70 + "\n")

    print("⚠️ 关键：必须明确说明每个角色是什么动物\n")
    print(f"Prompt: {MOTION_PROMPT}\n")

    # 聚焦输入框
    input_box = page.locator('[contenteditable="true"]').first
    await input_box.click()
    await asyncio.sleep(1)

    # 输入 prompt（慢速输入）
    await page.keyboard.type(MOTION_PROMPT, delay=30)
    await asyncio.sleep(2)

    # 验证
    text = await input_box.inner_text()
    if 'Luna' in text and 'Wayne' in text:
        print("✅ Prompt 已输入\n")
        print(f"内容: {text[:100]}...\n")
    else:
        print(f"⚠️ 验证失败: {text[:100]}\n")


async def step6_submit(page):
    """步骤6: 提交生成"""
    print("=" * 70)
    print("步骤 6: 提交视频生成")
    print("=" * 70 + "\n")

    try:
        # 按回车提交
        await page.keyboard.press('Enter')
        await asyncio.sleep(3)
        print("✅ 视频生成已提交\n")
    except Exception as e:
        print(f"❌ 提交失败: {e}\n")
        raise

    # 截图确认
    await page.screenshot(path='/tmp/video_ingredients_submitted.png', full_page=True)
    print("📸 截图: /tmp/video_ingredients_submitted.png\n")


async def main():
    """主流程"""
    print("\n" + "=" * 70)
    print("Google Flow 视频生成 - Ingredients 模式")
    print("=" * 70 + "\n")

    p = None
    browser = None

    try:
        # 连接
        p, browser, page = await connect_to_chrome()

        # 执行流程
        await step1_ensure_video_mode(page)
        await step2_open_media_picker(page)
        await step3_switch_to_images(page)
        await step4_select_reference_image(page)
        await step5_input_motion_prompt(page)
        await step6_submit(page)

        print("\n" + "=" * 70)
        print("✅ 成功！视频正在生成中...")
        print("=" * 70 + "\n")
        print("💡 Ingredients 模式 vs Frames 模式：")
        print("   - Ingredients: 参考图 + 动作描述")
        print("   - Frames: 首尾帧定义视频起止\n")

        return 0

    except Exception as e:
        print(f"\n❌ 流程失败: {e}\n")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        if browser:
            await browser.close()
        if p:
            await p.stop()


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        exit(exit_code)
    except KeyboardInterrupt:
        print("\n中断执行\n")
        exit(130)
    except Exception as e:
        print(f"\n❌ 错误: {e}\n")
        exit(1)
