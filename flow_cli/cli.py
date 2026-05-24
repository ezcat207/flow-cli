#!/usr/bin/env python3
"""Flow CLI - Command line interface for Google Flow automation"""

import argparse
import asyncio
import sys
from pathlib import Path
from typing import List, Optional

from flow_cli.config import Config
from flow_cli.automation import FlowAutomation
from flow_cli.chrome import start_chrome, stop_chrome


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Flow CLI - Google Flow automation tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # 生成图片（使用配置文件的项目）
  flow generate -i Luna_on_mars.png -i Wayne_on_earth.png -p "他们在中国杭州玩"

  # 设置项目 URL
  flow config --set-project https://labs.google/fx/tools/flow/project/YOUR_ID

  # 启动 Chrome
  flow start-chrome

  # 查看配置
  flow config --show
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # generate 命令
    generate_parser = subparsers.add_parser('generate', help='生成图片')
    generate_parser.add_argument('-i', '--image', action='append', dest='images',
                                 required=True, help='参考图文件名（可多次使用）')
    generate_parser.add_argument('-p', '--prompt', required=True,
                                help='生成描述 Prompt')
    generate_parser.add_argument('--project', help='项目 URL（覆盖配置）')
    generate_parser.add_argument('--no-screenshot', action='store_true',
                                help='不保存截图')

    # config 命令
    config_parser = subparsers.add_parser('config', help='配置管理')
    config_parser.add_argument('--show', action='store_true',
                              help='显示当前配置')
    config_parser.add_argument('--set-project', metavar='URL',
                              help='设置项目 URL')
    config_parser.add_argument('--set-cdp-url', metavar='URL',
                              help='设置 CDP URL')
    config_parser.add_argument('--set-screenshot-dir', metavar='PATH',
                              help='设置截图保存目录')

    # start-chrome 命令
    chrome_parser = subparsers.add_parser('start-chrome', help='启动 Chrome')
    chrome_parser.add_argument('--port', type=int, default=9222,
                              help='调试端口（默认: 9222）')
    chrome_parser.add_argument('--profile', help='Chrome profile 目录')

    # stop-chrome 命令
    subparsers.add_parser('stop-chrome', help='停止 Chrome')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # 执行命令
    if args.command == 'generate':
        return cmd_generate(args)
    elif args.command == 'config':
        return cmd_config(args)
    elif args.command == 'start-chrome':
        return cmd_start_chrome(args)
    elif args.command == 'stop-chrome':
        return cmd_stop_chrome()

    return 0


def cmd_generate(args):
    """执行生成命令"""
    config = Config()

    # 获取项目 URL
    project_url = args.project or config.get_project_url()
    if not project_url:
        print("❌ 错误: 未设置项目 URL")
        print("请使用以下命令设置:")
        print("  flow config --set-project https://labs.google/fx/tools/flow/project/YOUR_ID")
        return 1

    print("=" * 70)
    print("Flow CLI - 生成图片")
    print("=" * 70 + "\n")

    print(f"项目: {project_url}")
    print(f"参考图: {', '.join(args.images)}")
    print(f"Prompt: {args.prompt}\n")

    # 运行自动化
    try:
        asyncio.run(_run_generate(
            config=config,
            project_url=project_url,
            images=args.images,
            prompt=args.prompt,
            screenshot=not args.no_screenshot
        ))

        print("=" * 70)
        print("✅ 完成！图片正在生成中...")
        print("=" * 70 + "\n")
        print("提示: 请在 Flow 界面查看生成进度\n")

        return 0

    except KeyboardInterrupt:
        print("\n\n中断执行\n")
        return 130
    except Exception as e:
        print(f"\n❌ 错误: {e}\n")
        import traceback
        traceback.print_exc()
        return 1


async def _run_generate(config: Config, project_url: str, images: List[str],
                       prompt: str, screenshot: bool):
    """运行生成流程"""
    automation = FlowAutomation(
        cdp_url=config.get_cdp_url(),
        project_url=project_url,
        screenshot_dir=config.get_screenshot_dir()
    )

    try:
        await automation.connect()
        await automation.generate(images, prompt, screenshot=screenshot)
    finally:
        await automation.close()


def cmd_config(args):
    """配置管理命令"""
    config = Config()

    if args.show:
        print("=" * 70)
        print("Flow CLI 配置")
        print("=" * 70 + "\n")
        print(f"配置文件: {config.config_path}\n")
        print(f"CDP URL:        {config.get_cdp_url()}")
        print(f"项目 URL:       {config.get_project_url() or '(未设置)'}")
        print(f"Chrome Profile: {config.get_chrome_profile()}")
        print(f"截图目录:       {config.get_screenshot_dir()}\n")
        return 0

    changed = False

    if args.set_project:
        config.set_project_url(args.set_project)
        print(f"✅ 已设置项目 URL: {args.set_project}")
        changed = True

    if args.set_cdp_url:
        config.set("cdp_url", args.set_cdp_url)
        print(f"✅ 已设置 CDP URL: {args.set_cdp_url}")
        changed = True

    if args.set_screenshot_dir:
        config.set("screenshot_dir", args.set_screenshot_dir)
        print(f"✅ 已设置截图目录: {args.set_screenshot_dir}")
        changed = True

    if changed:
        config.save()
        print(f"\n配置已保存到: {config.config_path}\n")
    else:
        print("没有修改配置。使用 --show 查看当前配置。")

    return 0


def cmd_start_chrome(args):
    """启动 Chrome 命令"""
    config = Config()
    profile = args.profile or config.get_chrome_profile()

    print("=" * 70)
    print("启动 Chrome")
    print("=" * 70 + "\n")

    success = start_chrome(port=args.port, profile=profile)

    if success:
        print(f"\n✅ Chrome 已启动")
        print(f"   调试端口: {args.port}")
        print(f"   Profile: {profile}\n")
        return 0
    else:
        print(f"\n❌ Chrome 启动失败\n")
        return 1


def cmd_stop_chrome():
    """停止 Chrome 命令"""
    print("=" * 70)
    print("停止 Chrome")
    print("=" * 70 + "\n")

    success = stop_chrome()

    if success:
        print("✅ Chrome 已停止\n")
        return 0
    else:
        print("❌ 停止 Chrome 失败\n")
        return 1


if __name__ == '__main__':
    sys.exit(main())
