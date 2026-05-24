"""Core automation functions for Flow"""

import asyncio
from pathlib import Path
from typing import List, Optional
from playwright.async_api import async_playwright, Page


class FlowAutomation:
    """Google Flow automation"""

    def __init__(self, cdp_url: str, project_url: str, screenshot_dir: str = "/tmp"):
        self.cdp_url = cdp_url
        self.project_url = project_url
        self.screenshot_dir = Path(screenshot_dir)
        self.page: Optional[Page] = None

    async def connect(self):
        """Connect to Chrome via CDP"""
        print(f"连接到 Chrome (CDP: {self.cdp_url})...\n")

        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.connect_over_cdp(self.cdp_url)
        self.context = self.browser.contexts[0]

        # 找到 Flow 项目页面
        for page in self.context.pages:
            if 'flow/project' in page.url:
                self.page = page
                break

        if not self.page:
            print("未找到 Flow 项目页面，导航到项目...\n")
            self.page = await self.context.new_page()
            await self.page.goto(self.project_url)
            await self.page.wait_for_load_state('networkidle')

        print(f"当前页面: {self.page.url}\n")

        # 清理环境
        await self._cleanup()

    async def _cleanup(self):
        """清理对话框"""
        for _ in range(3):
            await self.page.keyboard.press('Escape')
            await asyncio.sleep(0.5)

    async def add_reference_image(self, image_name: str):
        """添加参考图"""
        print(f"  1. 打开媒体选择器")

        try:
            # 检查是否已打开
            await self.page.locator(f'text=/{image_name}/i').first.is_visible(timeout=2000)
            print(f"  媒体选择器已打开\n")
        except:
            # 点击加号按钮打开
            await self.page.mouse.click(230, 327)
            await asyncio.sleep(2)
            print(f"  媒体选择器已打开\n")

        # 选择文件
        print(f"  2. 选择 {image_name}")
        file_item = self.page.locator(f'text=/{image_name}/i').first
        await file_item.click()
        await asyncio.sleep(1)

        # 点击 Add to Prompt
        print(f"  3. 添加到 Prompt")
        add_btn = self.page.locator('button:has-text("Add to Prompt")').first
        await add_btn.click()
        await asyncio.sleep(2)

        print(f"✅ {image_name} 已添加\n")

    async def add_reference_images(self, images: List[str]):
        """添加多张参考图"""
        for idx, img_name in enumerate(images, 1):
            print("=" * 70)
            print(f"步骤 {idx}: 添加参考图 {img_name}")
            print("=" * 70 + "\n")

            await self.add_reference_image(img_name)

    async def input_prompt(self, prompt: str):
        """输入生成 Prompt"""
        print("=" * 70)
        print("输入生成 Prompt")
        print("=" * 70 + "\n")

        print(f"Prompt: '{prompt}'\n")

        # 查找输入框
        input_box = self.page.locator('[contenteditable="true"], textarea').first
        await input_box.click()
        await asyncio.sleep(0.5)
        await input_box.fill(prompt)
        await asyncio.sleep(1)

        print("✅ Prompt 已输入\n")

    async def submit_generation(self, screenshot: bool = True):
        """提交生成请求"""
        print("=" * 70)
        print("提交生成请求")
        print("=" * 70 + "\n")

        # 点击带箭头的 Create 按钮
        create_btn = self.page.locator('button:has(i:text("arrow_forward"))').first
        await create_btn.click()
        await asyncio.sleep(3)

        print("✅ 生成请求已提交\n")

        # 截图
        if screenshot:
            screenshot_path = self.screenshot_dir / "flow_generation_started.png"
            await self.page.screenshot(path=str(screenshot_path), full_page=True)
            print(f"📸 截图已保存: {screenshot_path}\n")

    async def generate(self, images: List[str], prompt: str, screenshot: bool = True):
        """完整的生成流程：添加图片 + 输入 Prompt + 提交"""
        await self.add_reference_images(images)
        await self.input_prompt(prompt)
        await self.submit_generation(screenshot=screenshot)

    async def close(self):
        """关闭连接"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
