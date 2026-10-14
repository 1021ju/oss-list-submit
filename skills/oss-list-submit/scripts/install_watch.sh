#!/usr/bin/env bash
# 安装/卸载定时检查：每 N 小时跑一次 watch_submissions.py，PR/issue 有变化就通知。
#   bash install_watch.sh            # 默认每 6 小时
#   bash install_watch.sh 3          # 每 3 小时
#   bash install_watch.sh --uninstall
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd -P)"
SCRIPT="$DIR/watch_submissions.py"
PY="$(command -v python3)"
GH="$(command -v gh || true)"
LABEL="com.oss-list-submit.watch"
DATA="$HOME/.oss-list-submit"

if [[ "${1:-}" == "--uninstall" ]]; then
  if [[ "$(uname)" == "Darwin" ]]; then
    launchctl unload "$HOME/Library/LaunchAgents/$LABEL.plist" 2>/dev/null || true
    rm -f "$HOME/Library/LaunchAgents/$LABEL.plist"
  else
    crontab -l 2>/dev/null | grep -v "$SCRIPT" | crontab - || true
  fi
  echo "已卸载定时检查（提交记录和状态文件保留在 $DATA）"
  exit 0
fi

HOURS="${1:-6}"
[[ -n "$GH" ]] || { echo "没找到 gh，先安装并 gh auth login"; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "gh 未登录，先运行 gh auth login"; exit 1; }
mkdir -p "$DATA"
[[ -f "$DATA/submissions.csv" ]] || cp "$DIR/../references/tracker-template.csv" "$DATA/submissions.csv"
PATHS="$(dirname "$GH"):$(dirname "$PY"):/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin"

if [[ "$(uname)" == "Darwin" ]]; then
  PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
  mkdir -p "$(dirname "$PLIST")"
  cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key><array><string>$PY</string><string>$SCRIPT</string></array>
  <key>EnvironmentVariables</key><dict><key>PATH</key><string>$PATHS</string></dict>
  <key>StartInterval</key><integer>$((HOURS * 3600))</integer>
  <key>RunAtLoad</key><true/>
  <key>StandardErrorPath</key><string>$DATA/watch.err</string>
</dict></plist>
EOF
  launchctl unload "$PLIST" 2>/dev/null || true
  launchctl load "$PLIST"
else
  LINE="0 */$HOURS * * * PATH=$PATHS $PY $SCRIPT >/dev/null 2>>$DATA/watch.err"
  (crontab -l 2>/dev/null | grep -v "$SCRIPT"; echo "$LINE") | crontab -
fi

echo "已安装：每 $HOURS 小时检查一次 $DATA/submissions.csv 里的 PR/issue"
