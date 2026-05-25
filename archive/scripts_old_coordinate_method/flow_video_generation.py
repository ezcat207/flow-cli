#!/usr/bin/env python3
"""
Google Flow 视频生成 - 端到端自动化脚本

⚠️ 关键顺序（必须严格遵守）：
1. 点击 Nano Banana 按钮（打开创建界面）
2. 切换到 Video 模式
3. 切换到 Frames 模式
4. 选择 Start 帧
5. 选择 End 帧
6. @ 添加角色（Luna, Wayne）
7. 输入运动描述（单行，无换行！）
8. 提交

为什么必须这个顺序？
- 必须先进入 Video Frames 模式，界面才会正确初始化
- 必须先选择首尾帧，再添加角色，否则界面状态会混乱
- 角色必须在 prompt 之前添加，这是 Flow 的设计
- Prompt 必须单行，换行会触发提前提交

使用方法:
    python3 flow_video_generation.py

配置:
    修改脚本中的 START_FRAME_INDEX, END_FRAME_INDEX, MOTION_PROMPT
"""

import asyncio
from playwright.async_api import async_playwright

# === 配置 ===
PROJECT_URL = "https://labs.google/fx/tools/flow/project/4f24835c-c783-4646-96dc-a0b8c03c34fc"
CDP_URL = "http://127.0.0.1:9222"

# 角色名称
CHARACTERS = ["luna", "wayne"]

# 首尾帧选择
START_FRAME_KEYWORD = "Luna Wayne at West Lake"  # 岸边场景
START_FRAME_INDEX = 1  # 选择第几个（0-based）
END_FRAME_KEYWORD = "Luna Wayne jumping"  # 跳船场景
END_FRAME_INDEX = 0  # 选择第几个（0-based）

# ⚠️ 运动描述 - 必须单行，不能有换行！
# 换行会导致提前提交，生成大量废片
MOTION_PROMPT = "Luna 和 Wayne 从西湖岸边走向游船，轻快地跳上船，船在湖面轻轻摇晃，镜头平滑跟随他们的动作从岸边推进到船上，背景西湖美景和远山保持稳定，日式平面风格明亮温暖"


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


async def step1_open_nano_banana(page):
    """步骤1: 点击 Nano Banana 按钮打开创建界面"""
    print("=" * 70)
    print("步骤 1: 点击 Nano Banana 按钮")
    print("=" * 70)
    print("\n为什么: 这是打开创建界面的唯一入口\n")

    try:
        nano_btn = page.locator('button:has-text("Nano Banana")').first
        await nano_btn.click()
        await asyncio.sleep(2)
        print("✅ Nano Banana 已打开\n")
    except Exception as e:
        print(f"❌ 失败: {e}\n")
        raise


async def step2_switch_to_video(page):
    """步骤2: 切换到 Video 模式"""
    print("=" * 70)
    print("步骤 2: 切换到 Video 模式")
    print("=" * 70)
    print("\n为什么: 必须先切换到 Video，才能看到 Frames 选项\n")

    try:
        video_tab = page.locator('button[role="tab"]:has-text("Video")').first
        await video_tab.click()
        await asyncio.sleep(2)
        print("✅ Video 模式\n")
    except Exception as e:
        print(f"❌ 失败: {e}\n")
        raise


async def step3_switch_to_frames(page):
    """步骤3: 切换到 Frames 模式"""
    print("=" * 70)
    print("步骤 3: 切换到 Frames 模式")
    print("=" * 70)
    print("\n为什么: Frames 模式才能选择首尾帧\n")

    try:
        frames_tab = page.locator('button[role="tab"]:has-text("Frames")').first
        await frames_tab.click()
        await asyncio.sleep(2)
        print("✅ Frames 模式\n")
    except Exception as e:
        print(f"❌ 失败: {e}\n")
        raise


async def step4_select_start_frame(page):
    """步骤4: 选择 Start 帧"""
    print("=" * 70)
    print("步骤 4: 选择 Start 帧（首帧）")
    print("=" * 70)
    print("\n为什么: 首帧是视频的开始画面，必须先选\n")

    # 点击 Start 按钮
    try:
        start_tab = page.locator('text=Start').first
        await start_tab.click()
        await asyncio.sleep(2)
        print("✅ Start 对话框已打开\n")
    except Exception as e:
        print(f"❌ 打开 Start 失败: {e}\n")
        raise

    # 选择图片
    try:
        images = page.locator(f'text="{START_FRAME_KEYWORD}"')
        count = await images.count()
        print(f"找到 {count} 个匹配的图片\n")

        if count > START_FRAME_INDEX:
            await images.nth(START_FRAME_INDEX).click()
            print(f"✅ 选择了第 {START_FRAME_INDEX + 1} 个图片\n")
        else:
            await images.first.click()
            print("✅ 选择了第一个图片\n")

        await asyncio.sleep(2)
    except Exception as e:
        print(f"❌ 选择图片失败: {e}\n")
        raise

    # 点击 Add to Prompt
    try:
        add_btn = page.locator('button:has-text("Add to Prompt")').first
        await add_btn.click()
        await asyncio.sleep(3)
        print("✅ Start 帧已添加\n")
    except Exception as e:
        print(f"⚠️  Add to Prompt: {e}（可能自动添加）\n")


async def step5_select_end_frame(page):
    """步骤5: 选择 End 帧"""
    print("=" * 70)
    print("步骤 5: 选择 End 帧（尾帧）")
    print("=" * 70)
    print("\n为什么: 尾帧是视频的结束画面\n")

    # 点击 End 按钮
    try:
        end_tab = page.locator('text=End').first
        await end_tab.click()
        await asyncio.sleep(2)
        print("✅ End 对话框已打开\n")
    except Exception as e:
        print(f"❌ 打开 End 失败: {e}\n")
        raise

    # 选择图片
    try:
        # 查找所有选项
        all_options = page.locator('[role="option"]')
        count = await all_options.count()
        print(f"找到 {count} 个选项\n")

        # 打印前几个选项
        for i in range(min(5, count)):
            try:
                text = await all_options.nth(i).inner_text()
                print(f"  选项 {i}: {text[:50]}\n")
            except:
                pass

        # 选择第一个（通常是跳船场景）
        if count > END_FRAME_INDEX:
            await all_options.nth(END_FRAME_INDEX).click()
            print(f"✅ 选择了第 {END_FRAME_INDEX + 1} 个选项\n")
        else:
            await all_options.first.click()
            print("✅ 选择了第一个选项\n")

        await asyncio.sleep(2)
    except Exception as e:
        print(f"❌ 选择图片失败: {e}\n")
        raise

    # 关闭对话框（按 Escape）
    await page.keyboard.press('Escape')
    await asyncio.sleep(1)
    print("✅ End 帧已添加\n")


async def step6_add_characters(page):
    """步骤6: @ 添加角色"""
    print("=" * 70)
    print("步骤 6: @ 添加角色")
    print("=" * 70)
    print("\n为什么: 必须在 prompt 之前添加角色，这是 Flow 的设计\n")
    print("为什么用 @: Character 模式包含声音和外观，视频需要\n")

    # 清理界面
    for _ in range(3):
        await page.keyboard.press('Escape')
        await asyncio.sleep(0.3)

    # 聚焦输入框
    input_box = page.locator('[contenteditable="true"]').first
    await input_box.click()
    await asyncio.sleep(1)

    # 添加每个角色
    for idx, character in enumerate(CHARACTERS, 1):
        print(f"\n添加 {character}...\n")

        # 输入 @
        await page.keyboard.type('@')
        await asyncio.sleep(2)

        # 点击 Characters 标签
        try:
            characters_tab = page.locator('button[role="tab"]:has-text("Characters")').first
            await characters_tab.click()
            await asyncio.sleep(2)
        except:
            pass

        # 选择角色
        try:
            option = page.locator('[role="option"]').filter(has_text=character).first
            await option.click()
            await asyncio.sleep(2)
        except Exception as e:
            print(f"❌ 选择 {character} 失败: {e}\n")
            raise

        # 第一个角色需要点击 Add to Prompt，第二个自动添加
        if idx == 1:
            try:
                add_btn = page.locator('button:has-text("Add to Prompt")').first
                await add_btn.click()
                await asyncio.sleep(3)
                print(f"✅ {character} 已添加\n")
            except:
                await asyncio.sleep(3)
                print(f"✅ {character} 已添加（自动）\n")
        else:
            await asyncio.sleep(3)
            print(f"✅ {character} 已自动添加\n")

    # 验证
    input_text = await input_box.inner_text()
    if all(char in input_text.lower() for char in CHARACTERS):
        print("✅ 角色验证通过\n")
    else:
        print(f"⚠️  验证警告: {input_text[:100]}\n")


async def step7_input_prompt(page):
    """步骤7: 输入运动描述 prompt"""
    print("=" * 70)
    print("步骤 7: 输入运动描述 Prompt")
    print("=" * 70)
    print("\n⚠️ 为什么必须单行: 换行键会触发提前提交！\n")
    print("后果: 生成大量不完整的废片，只有最后一行被生成\n")

    input_box = page.locator('[contenteditable="true"]').first
    await input_box.click()
    await asyncio.sleep(1)

    print(f"Prompt:\n{MOTION_PROMPT}\n")

    # 使用延迟输入（每个字符 20ms）
    await page.keyboard.type(MOTION_PROMPT, delay=20)

    # ⚠️ 关键：等待输入完成
    print("\n等待输入完成（5秒）...\n")
    print("为什么等待: keyboard.type() 是异步的，需要确保所有字符都输入完\n")
    await asyncio.sleep(5)

    # 验证
    input_text = await input_box.inner_text()
    if '西湖' in input_text and '船' in input_text:
        print("✅ Prompt 验证通过\n")
    else:
        print(f"⚠️  内容: {input_text[:300]}\n")

    # 最后确认
    print("最后确认（3秒）...\n")
    print("为什么再等: 双重保险，确保万无一失\n")
    await asyncio.sleep(3)


async def step8_submit(page):
    """步骤8: 提交视频生成"""
    print("=" * 70)
    print("步骤 8: 提交视频生成")
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
    await page.screenshot(path='/tmp/video_submitted.png', full_page=True)
    print("📸 截图: /tmp/video_submitted.png\n")


async def main():
    """主流程"""
    print("\n" + "=" * 70)
    print("Google Flow 视频生成 - 端到端自动化")
    print("=" * 70 + "\n")

    p = None
    browser = None

    try:
        # 连接
        p, browser, page = await connect_to_chrome()

        # 执行完整流程
        await step1_open_nano_banana(page)
        await step2_switch_to_video(page)
        await step3_switch_to_frames(page)
        await step4_select_start_frame(page)
        await step5_select_end_frame(page)
        await step6_add_characters(page)
        await step7_input_prompt(page)
        await step8_submit(page)

        print("\n" + "=" * 70)
        print("✅ 成功！视频正在生成中...")
        print("=" * 70 + "\n")

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
