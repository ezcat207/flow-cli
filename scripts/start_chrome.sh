#!/bin/bash
# 关闭现有Chrome
killall "Google Chrome" 2>/dev/null

sleep 2

# 启动Chrome（带远程调试）
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/Library/Application Support/Google/Chrome" \
  > /dev/null 2>&1 &

echo "✅ Chrome已启动（远程调试端口9222）"
echo ""
echo "请在Chrome中："
echo "  1. 登录Google账号"
echo "  2. 打开项目页面"
echo "  3. 然后告诉我'好了'"
