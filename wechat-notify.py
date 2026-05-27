"""Claude Code 权限确认 → 本地守护进程 → 企业微信智能机器人 → 手机微信"""
import sys
import json
import os
import requests

DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(DIR, "wechat-notify-config.json")
PORT_FILE = os.path.join(DIR, ".wecom-port")


def _read_port():
    try:
        with open(PORT_FILE) as f:
            return int(f.read().strip())
    except Exception:
        return 19800


def main():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception:
        print("[wechat-notify] config not found", file=sys.stderr)
        sys.exit(0)

    port = _read_port()

    # 读取 hook 传入的上下文
    ctx = {}
    try:
        raw = sys.stdin.read()
        if raw.strip():
            ctx = json.loads(raw)
    except json.JSONDecodeError:
        pass

    msg_type = ctx.get("notification_type", "permission_prompt")
    message = ctx.get("message", "")
    tool = ctx.get("tool_name", "")
    if tool:
        content = f"Claude Code needs your approval\n\nTool: {tool}\n{message[:1500]}"
    else:
        content = f"Claude Code needs your approval\n\n{message[:1500]}"

    try:
        resp = requests.post(
            f"http://127.0.0.1:{port}/send",
            json={"content": content},
            timeout=5,
        )
        data = resp.json()
        if data.get("ok"):
            print("[wechat-notify] 已推送", file=sys.stderr)
        else:
            print(f"[wechat-notify] {data.get('message')}", file=sys.stderr)
    except requests.ConnectionError:
        print("[wechat-notify] 守护进程未运行", file=sys.stderr)
    except requests.RequestException as e:
        print(f"[wechat-notify] 错误: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
