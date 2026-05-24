#!/usr/bin/env python3
"""
Google Flow 自动化脚本
通过 Playwright 自动化浏览器操作实现 Flow 图片和视频生成

用法:
    python flow_automation.py image "A cute cat" --model banana2 --ratio 16:9 --count 2
    python flow_automation.py video "Drone shot of city" --duration 5
"""

import asyncio
from pathlib import Path
from typing import List, Optional, Literal
from playwright.async_api import async_playwright, Page, BrowserContext
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()
app = typer.Typer()


class FlowAutomation:
    """Google Flow 浏览器自动化"""

    FLOW_URL = "https://labs.google/fx/tools/flow"
    USER_DATA_DIR = "/tmp/flow_browser_profile"

    # 关键选择器
    SELECTORS = {
        "new_project_btn": 'button:has-text("New project")',
        "input_container": "#__next > div > div:nth-of-type(5) > div > div > div > div",
        "editable_input": "[contenteditable='true']",
        "create_btn": "#__next > div > div:nth-of-type(5) > div > div > div > div > div:nth-of-type(2) > div:nth-of-type(2) > button:nth-of-type(2)",
        "model_btn": 'button:has-text("Nano Banana")',
        "image_type": 'button:has-text("Image")',
        "video_type": 'button:has-text("Video")',
        "generated_image": 'img[alt="Generated image"]',
        "upload_btn": "#__next > div > div:nth-of-type(5) > div > div > div > div > div:nth-of-type(2) > div > div > button",
        "uploads_tab": 'button:has-text("Uploads")',
        "add_to_prompt_btn": 'button:has-text("Add to Prompt")',
    }

    def __init__(self, headless: bool = False):
        self.headless = headless
        self.playwright = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.current_project_id: Optional[str] = None

    async def start(self):
        """启动浏览器并初始化"""
        console.print("🚀 启动浏览器...", style="bold blue")

        self.playwright = await async_playwright().start()

        self.context = await self.playwright.chromium.launch_persistent_context(
            self.USER_DATA_DIR,
            headless=self.headless,
            args=["--start-maximized"],
            viewport={"width": 1920, "height": 1080},
        )

        if self.context.pages:
            self.page = self.context.pages[0]
        else:
            self.page = await self.context.new_page()

        console.print("✅ 浏览器已启动\n", style="green")

    async def close(self):
        """关闭浏览器"""
        if self.context:
            await self.context.close()
        if self.playwright:
            await self.playwright.stop()

    async def navigate_to_flow(self):
        """导航到 Flow 主页"""
        console.print(f"🌐 导航到 {self.FLOW_URL}...", style="cyan")
        await self.page.goto(self.FLOW_URL)
        await self.page.wait_for_load_state("networkidle")
        await asyncio.sleep(2)
        console.print("✅ 页面加载完成\n", style="green")

    async def create_project(self) -> str:
        """创建新项目并返回 project ID"""
        console.print("📁 创建新项目...", style="bold yellow")

        # 确保在主页
        if "/project/" not in self.page.url:
            await self.navigate_to_flow()

        # 点击 New project 按钮
        new_project_btn = self.page.locator(self.SELECTORS["new_project_btn"]).first

        if not await new_project_btn.is_visible(timeout=5000):
            raise Exception("未找到 'New project' 按钮")

        await new_project_btn.click()
        console.print("   点击 'New project'...", style="dim")

        # 等待跳转到项目页面
        await asyncio.sleep(5)
        await self.page.wait_for_load_state("networkidle")

        # 提取 project ID
        url = self.page.url
        if "/project/" in url:
            project_id = url.split("/project/")[-1].split("?")[0].split("/")[0]
            self.current_project_id = project_id
            console.print(f"✅ 项目已创建: {project_id}\n", style="green")
            return project_id
        else:
            raise Exception(f"创建项目失败，当前 URL: {url}")

    async def configure_generation(
        self,
        generation_type: Literal["image", "video"] = "image",
        aspect_ratio: str = "16:9",
        count: int = 1,
    ):
        """配置生成参数"""
        console.print("⚙️  配置生成选项...", style="cyan")

        # 点击模型/配置按钮打开菜单
        model_btn = self.page.locator(self.SELECTORS["model_btn"]).first

        if await model_btn.is_visible(timeout=3000):
            await model_btn.click()
            await asyncio.sleep(1)
            console.print(f"   打开配置菜单", style="dim")

            # 选择类型
            type_selector = (
                self.SELECTORS["image_type"]
                if generation_type == "image"
                else self.SELECTORS["video_type"]
            )
            type_btn = self.page.locator(type_selector).first

            if await type_btn.is_visible(timeout=2000):
                await type_btn.click()
                await asyncio.sleep(0.5)
                console.print(f"   选择类型: {generation_type}", style="dim")

            # TODO: 选择宽高比和数量
            # 这需要更具体的选择器，目前先跳过

            # 关闭菜单（点击其他地方）
            await self.page.mouse.click(800, 400)
            await asyncio.sleep(0.5)

        console.print("✅ 配置完成\n", style="green")

    async def input_prompt(self, prompt: str):
        """在输入框中输入 prompt"""
        console.print(f"⌨️  输入 prompt: {prompt}", style="cyan")

        # 定位输入容器
        input_container = self.page.locator(self.SELECTORS["input_container"])

        if not await input_container.is_visible(timeout=5000):
            raise Exception("未找到输入框容器")

        # 点击容器激活
        await input_container.click()
        await asyncio.sleep(0.5)

        # 查找可编辑元素
        editable = input_container.locator(self.SELECTORS["editable_input"]).first

        if not await editable.is_visible(timeout=3000):
            raise Exception("未找到可编辑输入框")

        # 输入文本
        await editable.fill(prompt)
        await asyncio.sleep(1)

        console.print("✅ Prompt 已输入\n", style="green")

    async def click_create(self):
        """点击 Create 按钮触发生成"""
        console.print("🖱️  点击 Create 按钮...", style="cyan")

        create_btn = self.page.locator(self.SELECTORS["create_btn"])

        if not await create_btn.is_visible(timeout=5000):
            raise Exception("未找到 Create 按钮")

        # 检查按钮是否启用
        disabled = await create_btn.get_attribute("aria-disabled")

        if disabled == "true":
            raise Exception("Create 按钮被禁用，请检查配置")

        await create_btn.click()
        console.print("✅ 已触发生成\n", style="green")

    async def add_reference_images(self, image_names: List[str], project_id: str):
        """
        添加参考图到 Prompt

        重要：每个参考图都需要单独打开 Media 库来添加
        流程：打开 Media → 选图 → Add to Prompt → 关闭 → 重复

        Args:
            image_names: 图片文件名列表，如 ["Luna_on_mars.png", "Wayne_on_earth.png"]
            project_id: 项目 ID（需要先上传图片到该项目的 Media 库）

        注意：图片需要提前上传到项目的 Media 库中
        """
        console.print(f"📷 添加 {len(image_names)} 个参考图（分 {len(image_names)} 次）...", style="cyan")

        # 导航到项目（如果不在）
        if project_id not in self.page.url:
            await self.page.goto(f"{self.FLOW_URL}/project/{project_id}")
            await self.page.wait_for_load_state("networkidle")
            await asyncio.sleep(2)

        # 逐个添加参考图（每次都要重新打开 Media 库）
        for idx, img_name in enumerate(image_names, 1):
            console.print(f"\n   [{idx}/{len(image_names)}] 添加 {img_name}...", style="dim")

            # 打开 Media 库
            upload_btn = self.page.locator(self.SELECTORS["upload_btn"]).first

            if not await upload_btn.is_visible(timeout=5000):
                raise Exception(f"未找到参考图上传按钮（添加第 {idx} 个图片时）")

            await upload_btn.click()
            await asyncio.sleep(3)
            console.print(f"      Media 库已打开 (第 {idx} 次)", style="dim")

            # 点击 Uploads 标签（找到Media库对话框中的Uploads）
            # 尝试所有Uploads按钮，通过检查是否出现文件列表来判断是否正确
            all_uploads = self.page.locator('button:has-text("Uploads")')
            uploads_count = await all_uploads.count()

            uploads_clicked = False
            for i in range(uploads_count):
                btn = all_uploads.nth(i)
                if await btn.is_visible(timeout=1000):
                    await btn.click(force=True)
                    await asyncio.sleep(3)

                    # 检查是否出现了文件列表
                    file_check = self.page.locator(f'text="{img_name}"').first
                    if await file_check.is_visible(timeout=2000):
                        console.print(f"      Uploads 标签已点击", style="dim")
                        uploads_clicked = True
                        break

            if not uploads_clicked:
                console.print("      ⚠️  未找到Media库中的Uploads标签", style="yellow")
                await self.page.keyboard.press("Escape")
                await asyncio.sleep(1)
                continue

            # 选择图片
            img_item = self.page.locator(f'text="{img_name}"').first

            if not await img_item.is_visible(timeout=5000):
                console.print(f"      ❌ 未找到 {img_name}", style="red")
                await self.page.keyboard.press("Escape")
                await asyncio.sleep(1)
                continue

            # 点击选中图片
            await img_item.click()
            await asyncio.sleep(3)  # 增加等待时间
            console.print(f"      图片已选中", style="dim")

            # 点击 "Add to Prompt" 按钮
            # 使用多种选择器尝试
            add_btn = None
            selectors = [
                'button:has-text("Add to Prompt")',
                'text="Add to Prompt"',
                '[role="button"]:has-text("Add to Prompt")',
            ]

            for selector in selectors:
                try:
                    btn = self.page.locator(selector).first
                    if await btn.is_visible(timeout=3000):
                        add_btn = btn
                        console.print(f"      找到 Add to Prompt 按钮 (选择器: {selector[:30]}...)", style="dim")
                        break
                except:
                    continue

            if not add_btn:
                console.print(f"      ❌ 未找到 'Add to Prompt' 按钮", style="red")
                # 截图调试
                await self.page.screenshot(path=f'/tmp/debug_{img_name}_no_add_btn.png', full_page=True)
                console.print(f"      📸 调试截图: /tmp/debug_{img_name}_no_add_btn.png", style="yellow")
                await self.page.keyboard.press("Escape")
                await asyncio.sleep(1)
                continue

            await add_btn.click()
            await asyncio.sleep(2)
            console.print(f"      ✅ {img_name} 已添加到 Prompt", style="green")

            # 关闭 Media 库（为下一个图片做准备）
            await self.page.keyboard.press("Escape")
            await asyncio.sleep(2)

        console.print("\n✅ 所有参考图添加完成\n", style="bold green")

    async def click_create_with_refs(self):
        """
        点击正确的 Create 按钮（用于有参考图的情况）

        注意：当添加了参考图后，需要使用 prompt 区域的按钮索引来定位正确的 Create 按钮
        """
        console.print("🖱️  点击 Create 按钮（参考图模式）...", style="cyan")

        # 使用 prompt 区域的所有按钮，找到正确的 Create 按钮
        prompt_area = self.page.locator("#__next > div > div:nth-of-type(5)")
        buttons = prompt_area.locator("button")

        # 查找文本包含 "Create" 且 aria-disabled='false' 的按钮
        count = await buttons.count()

        for i in range(count):
            btn = buttons.nth(i)

            if await btn.is_visible(timeout=500):
                text = await btn.inner_text()
                aria_disabled = await btn.get_attribute("aria-disabled") or ""

                # 查找包含 "arrow_forward" 和 "Create" 的按钮（正确的生成按钮）
                if "create" in text.lower() and "arrow_forward" in text.lower():
                    if aria_disabled != "true":
                        console.print(f"   找到正确的 Create 按钮 (索引 {i})", style="dim")
                        await btn.click()
                        console.print("✅ 已触发生成\n", style="green")
                        return

        raise Exception("未找到可用的 Create 按钮")

    async def wait_for_generation(
        self, timeout: int = 180, generation_type: str = "image"
    ) -> List[str]:
        """等待生成完成并返回结果 URL 列表"""
        type_name = "图片" if generation_type == "image" else "视频"
        console.print(f"⏳ 等待{type_name}生成（最多 {timeout} 秒）...", style="yellow")

        results = []
        start_time = asyncio.get_event_loop().time()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(f"生成中...", total=None)

            while asyncio.get_event_loop().time() - start_time < timeout:
                await asyncio.sleep(5)

                # 检查是否有生成的图片
                images = self.page.locator(self.SELECTORS["generated_image"])
                count = await images.count()

                if count > len(results):
                    # 有新图片生成
                    for i in range(len(results), count):
                        img = images.nth(i)
                        src = await img.get_attribute("src")
                        if src:
                            results.append(src)
                            progress.update(task, description=f"已生成 {len(results)} 个")

                    # 如果有结果，再等待一会儿看是否还有更多
                    if results:
                        await asyncio.sleep(10)
                        new_count = await images.count()
                        if new_count == count:
                            # 数量不再增加，生成完成
                            break

        if results:
            console.print(f"✅ 成功生成 {len(results)} 个{type_name}\n", style="green bold")
        else:
            console.print(f"⚠️  超时：{timeout}秒内未检测到生成结果\n", style="yellow")

        return results

    async def generate_image(
        self,
        prompt: str,
        model: str = "banana2",
        aspect_ratio: str = "16:9",
        count: int = 2,
        project_id: Optional[str] = None,
    ) -> List[str]:
        """
        生成图片

        Args:
            prompt: 图片描述
            model: 模型选择 (imagen4, banana2, banana-pro)
            aspect_ratio: 宽高比 (16:9, 1:1, 4:3, 9:16, 3:4)
            count: 生成数量 (1-4)
            project_id: 项目 ID（可选，不提供则创建新项目）

        Returns:
            生成的图片 URL 列表
        """
        console.print("\n" + "=" * 70, style="bold")
        console.print("🎨 Flow 图片生成", style="bold magenta")
        console.print("=" * 70 + "\n", style="bold")

        # 创建或使用项目
        if not project_id:
            project_id = await self.create_project()
        else:
            await self.page.goto(f"{self.FLOW_URL}/project/{project_id}")
            await self.page.wait_for_load_state("networkidle")
            await asyncio.sleep(2)

        # 配置生成选项
        await self.configure_generation(
            generation_type="image", aspect_ratio=aspect_ratio, count=count
        )

        # 输入 prompt
        await self.input_prompt(prompt)

        # 触发生成
        await self.click_create()

        # 等待结果
        results = await self.wait_for_generation(timeout=180, generation_type="image")

        return results

    async def generate_video(
        self,
        prompt: str,
        duration: int = 5,
        aspect_ratio: str = "16:9",
        project_id: Optional[str] = None,
    ) -> List[str]:
        """
        生成视频

        Args:
            prompt: 视频描述
            duration: 时长（秒）
            aspect_ratio: 宽高比
            project_id: 项目 ID（可选）

        Returns:
            生成的视频 URL 列表
        """
        console.print("\n" + "=" * 70, style="bold")
        console.print("🎬 Flow 视频生成", style="bold magenta")
        console.print("=" * 70 + "\n", style="bold")

        # 创建或使用项目
        if not project_id:
            project_id = await self.create_project()
        else:
            await self.page.goto(f"{self.FLOW_URL}/project/{project_id}")
            await self.page.wait_for_load_state("networkidle")
            await asyncio.sleep(2)

        # 配置为视频模式
        await self.configure_generation(
            generation_type="video", aspect_ratio=aspect_ratio
        )

        # 输入 prompt
        await self.input_prompt(prompt)

        # 触发生成
        await self.click_create()

        # 等待结果（视频需要更长时间）
        results = await self.wait_for_generation(timeout=300, generation_type="video")

        return results


# ============================================
# CLI 命令
# ============================================


@app.command()
def image(
    prompt: str,
    model: str = typer.Option("banana2", help="模型: imagen4, banana2, banana-pro"),
    ratio: str = typer.Option("16:9", help="宽高比: 16:9, 1:1, 4:3, 9:16, 3:4"),
    count: int = typer.Option(2, help="生成数量: 1-4"),
    project_id: Optional[str] = typer.Option(None, help="使用已有项目 ID"),
):
    """生成图片"""

    async def run():
        flow = FlowAutomation()
        try:
            await flow.start()
            results = await flow.generate_image(
                prompt=prompt,
                model=model,
                aspect_ratio=ratio,
                count=count,
                project_id=project_id,
            )

            console.print("\n" + "=" * 70, style="bold green")
            console.print("📊 生成结果", style="bold green")
            console.print("=" * 70 + "\n", style="bold green")

            for i, url in enumerate(results, 1):
                console.print(f"{i}. {url}", style="cyan")

            console.print(f"\n✅ 共生成 {len(results)} 张图片", style="bold green")

        finally:
            await flow.close()

    asyncio.run(run())


@app.command()
def video(
    prompt: str,
    duration: int = typer.Option(5, help="时长（秒）"),
    ratio: str = typer.Option("16:9", help="宽高比"),
    project_id: Optional[str] = typer.Option(None, help="使用已有项目 ID"),
):
    """生成视频"""

    async def run():
        flow = FlowAutomation()
        try:
            await flow.start()
            results = await flow.generate_video(
                prompt=prompt,
                duration=duration,
                aspect_ratio=ratio,
                project_id=project_id,
            )

            console.print("\n" + "=" * 70, style="bold green")
            console.print("📊 生成结果", style="bold green")
            console.print("=" * 70 + "\n", style="bold green")

            for i, url in enumerate(results, 1):
                console.print(f"{i}. {url}", style="cyan")

            console.print(f"\n✅ 共生成 {len(results)} 个视频", style="bold green")

        finally:
            await flow.close()

    asyncio.run(run())


if __name__ == "__main__":
    app()
