#!/usr/bin/env python3
"""
Google Flow 视频生成自动化脚本

完整流程：
1. 使用 @ 方式添加角色（Luna 和 Wayne）
2. 切换到 Video 模式
3. 切换到 Frames 模式
4. 选择首帧（Start frame）
5. 选择尾帧（End frame）
6. 输入运动描述
7. 提交视频生成

使用方法:
    python3 flow_automation_video.py

前置条件:
    - Chrome 已启动（调试端口 9222）
    - 已登录 Google 账号
    - 已打开 Flow 项目页面
    - 已有可选的图片作为首尾帧
"""

import asyncio
from playwright.async_api import async_playwright

# === 配置 ===
PROJECT_URL = "https://labs.google/fx/tools/flow/project/4f24835c-c783-4646-96dc-a0b8c03c34fc"
CDP_URL = "http://127.0.0.1:9222"

# 角色名称
CHARACTERS = ["luna", "wayne"]

# ⚠️ 运动描述 - 必须是单行，不能有换行！
MOTION_PROMPT = "Luna 和 Wayne 从西湖岸边走向游船，轻快地跳上船，船在湖面轻轻摇晃，镜头平滑跟随他们的动作从岸边推进到船上，背景西湖美景和远山保持稳定，日式平面风格明亮温暖"

# 首帧和尾帧的标识（通过图片名称或索引）
START_FRAME_NAME = "Luna Wayne at West Lake"  # 岸边场景
END_FRAME_NAME = "Luna Wayne jumping"  # 跳船场景


async def add_characters(page):
    """步骤1：使用 @ 方式添加角色"""
    print("\n" + "=" * 70)
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
            characters_tab = page.locator('button[role="tab"]:has-text("Characters")').first
            await characters_tab.click()
            await asyncio.sleep(2)
        except Exception as e:
            print(f"⚠️  切换 Characters 失败: {e}\n")

        # 选择角色
        try:
            character_option = page.locator('[role="option"]').filter(has_text=character).first
            await character_option.click()
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
                print(f"❌ Add to Prompt 失败: {e}\n")
                raise
        else:
            # 第二个角色自动添加
            await asyncio.sleep(3)
            print(f"✅ {character} 已自动添加\n")

    # 验证
    input_text = await input_box.inner_text()
    if 'luna' in input_text.lower() and 'wayne' in input_text.lower():
        print("✅ 角色验证通过\n")
    else:
        print(f"⚠️  验证警告: {input_text[:100]}\n")


async def switch_to_video_frames(page):
    """步骤2：切换到 Video → Frames 模式"""
    print("\n" + "=" * 70)
    print("步骤 2: 切换到 Video Frames 模式")
    print("=" * 70 + "\n")

    # 切换到 Video
    print("切换到 Video 模式\n")
    try:
        video_tab = page.locator('button:has-text("Video")').first
        await video_tab.click()
        await asyncio.sleep(2)
        print("✅ Video 模式\n")
    except Exception as e:
        print(f"❌ 切换 Video 失败: {e}\n")
        raise

    # 切换到 Frames
    print("切换到 Frames 模式\n")
    try:
        frames_tab = page.locator('button:has-text("Frames")').first
        await frames_tab.click()
        await asyncio.sleep(2)
        print("✅ Frames 模式\n")
    except Exception as e:
        print(f"❌ 切换 Frames 失败: {e}\n")
        raise


async def select_start_frame(page):
    """步骤3：选择首帧"""
    print("\n" + "=" * 70)
    print("步骤 3: 选择首帧（Start Frame）")
    print("=" * 70 + "\n")

    # 点击 Start 按钮
    print("点击 Start 按钮\n")
    try:
        start_btn = page.locator('text=Start').first
        await start_btn.click()
        await asyncio.sleep(2)
        print("✅ Start 按钮已点击\n")
    except Exception as e:
        print(f"❌ 点击 Start 失败: {e}\n")
        raise

    # 选择图片
    print(f"选择首帧图片: {START_FRAME_NAME}\n")
    await asyncio.sleep(1)

    try:
        # 查找包含指定名称的图片，选择第二个（岸边场景）
        lake_images = page.locator(f'text="{START_FRAME_NAME}"')
        count = await lake_images.count()
        print(f"找到 {count} 个匹配的图片\n")

        if count >= 2:
            # 选择第二个（通常是岸边场景）
            await lake_images.nth(1).click()
            print("✅ 选择了第二个图片（岸边）\n")
        else:
            # 只有一个就选第一个
            await lake_images.first.click()
            print("✅ 选择了第一个图片\n")

        await asyncio.sleep(2)
    except Exception as e:
        print(f"❌ 选择首帧图片失败: {e}\n")
        raise

    # 点击 Add to Prompt
    print("点击 Add to Prompt\n")
    try:
        add_btn = page.locator('button:has-text("Add to Prompt")').first
        await add_btn.click()
        await asyncio.sleep(3)
        print("✅ 首帧已添加\n")
    except Exception as e:
        print(f"❌ Add to Prompt 失败: {e}\n")
        raise


async def select_end_frame(page):
    """步骤4：选择尾帧"""
    print("\n" + "=" * 70)
    print("步骤 4: 选择尾帧（End Frame）")
    print("=" * 70 + "\n")

    # 点击 End 标签
    print("点击 End 标签\n")
    try:
        end_tab = page.locator('text=End').first
        await end_tab.click()
        await asyncio.sleep(2)
        print("✅ End 标签已点击\n")
    except Exception as e:
        print(f"❌ 点击 End 失败: {e}\n")
        raise

    # 选择图片
    print(f"选择尾帧图片: {END_FRAME_NAME}\n")
    await asyncio.sleep(1)

    try:
        # 先尝试精确匹配跳船场景
        jumping_images = page.locator(f'text*="{END_FRAME_NAME}"')
        count = await jumping_images.count()

        if count > 0:
            print(f"找到 {count} 个跳船图片\n")
            # 选择第一个跳船图片
            await jumping_images.first.click()
            print("✅ 选择了跳船场景\n")
        else:
            print("未找到跳船图片，选择第一个 West Lake 图片\n")
            # 如果找不到，选择第一个 West Lake 图片
            lake_images = page.locator('text="Luna Wayne at West Lake"')
            await lake_images.first.click()
            print("✅ 选择了备用图片\n")

        await asyncio.sleep(2)
    except Exception as e:
        print(f"❌ 选择尾帧图片失败: {e}\n")
        raise

    # 点击 Add to Prompt
    print("点击 Add to Prompt\n")
    try:
        add_btn = page.locator('button:has-text("Add to Prompt")').first
        await add_btn.click()
        await asyncio.sleep(3)
        print("✅ 尾帧已添加\n")
    except Exception as e:
        print(f"❌ Add to Prompt 失败: {e}\n")
        raise


async def input_motion_description(page):
    """步骤5：输入运动描述"""
    print("\n" + "=" * 70)
    print("步骤 5: 输入运动描述")
    print("=" * 70 + "\n")

    # 查找输入框
    input_box = page.locator('[contenteditable="true"]').first
    await input_box.click()
    await asyncio.sleep(1)

    # 清空现有内容（只清除非角色部分）
    # 不清空，直接在后面追加
    print(f"输入运动描述:\n{MOTION_PROMPT}\n")

    # ⚠️ 使用延迟，单行输入
    await page.keyboard.type(MOTION_PROMPT, delay=20)

    # 等待输入完成
    print("等待输入完成（5秒）...\n")
    await asyncio.sleep(5)

    # 验证
    input_text = await input_box.inner_text()
    if '西湖' in input_text and '船' in input_text:
        print("✅ 运动描述验证通过\n")
        print(f"内容预览: {input_text[:150]}...\n")
    else:
        print(f"⚠️  验证警告: {input_text[:200]}\n")

    # 最后确认
    print("最后确认（3秒）...\n")
    await asyncio.sleep(3)


async def submit_video(page):
    """步骤6：提交视频生成"""
    print("\n" + "=" * 70)
    print("步骤 6: 提交视频生成")
    print("=" * 70 + "\n")

    try:
        create_btn = page.locator('button:has(i:text("arrow_forward"))').first
        await create_btn.click()
        await asyncio.sleep(3)
        print("✅ 视频生成已提交\n")
    except Exception as e:
        print(f"❌ 提交失败: {e}\n")
        raise

    # 截图确认
    await page.screenshot(path='/tmp/video_generation_result.png', full_page=True)
    print("📸 截图: /tmp/video_generation_result.png\n")


async def main():
    """主流程"""
    print("=" * 70)
    print("Google Flow 视频生成 - 完整流程")
    print("=" * 70 + "\n")

    async with async_playwright() as p:
        # 连接到 Chrome
        print(f"连接到 Chrome (CDP: {CDP_URL})...\n")
        try:
            browser = await p.chromium.connect_over_cdp(CDP_URL)
        except Exception as e:
            print(f"❌ 连接 Chrome 失败: {e}\n")
            print("请确保 Chrome 已用以下命令启动：\n")
            print("  killall 'Google Chrome'\n")
            print("  /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome \\")
            print("    --remote-debugging-port=9222 \\")
            print("    --user-data-dir=/tmp/flow_chrome_debug \\")
            print(f"    '{PROJECT_URL}' > /dev/null 2>&1 &\n")
            return 1

        context = browser.contexts[0]

        # 获取 Flow 页面
        page = None
        for pg in context.pages:
            if 'flow/project' in pg.url:
                page = pg
                break

        if not page:
            print("未找到 Flow 项目页面\n")
            if len(context.pages) > 0:
                page = context.pages[0]
                print(f"使用第一个标签页: {page.url}\n")
            else:
                print("❌ 没有可用的页面\n")
                await browser.close()
                return 1

        print(f"当前页面: {page.url}\n")

        # 清理环境
        print("清理环境...\n")
        for _ in range(5):
            await page.keyboard.press('Escape')
            await asyncio.sleep(0.3)

        try:
            # 执行完整流程
            await add_characters(page)
            await switch_to_video_frames(page)
            await select_start_frame(page)
            await select_end_frame(page)
            await input_motion_description(page)
            await submit_video(page)

            print("\n" + "=" * 70)
            print("✅ 完成！视频正在生成中...")
            print("=" * 70 + "\n")
            print("提示: 请在 Flow 界面查看生成进度\n")

        except Exception as e:
            print(f"\n❌ 流程执行失败: {e}\n")
            import traceback
            traceback.print_exc()
            await page.screenshot(path='/tmp/video_error.png', full_page=True)
            print("📸 错误截图: /tmp/video_error.png\n")
            await browser.close()
            return 1

        await browser.close()
        return 0


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n中断执行\n")
        exit(130)
    except Exception as e:
        print(f"\n❌ 错误: {e}\n")
        import traceback
        traceback.print_exc()
        exit(1)
