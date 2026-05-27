# Claude Code WeChat Notify

> **Disclaimer:** This project was built with [Claude Code](https://claude.ai/code). Your BotID and Secret grant full access to send messages via your WeCom bot — use at your own risk. The authors assume no liability for any misuse, data leakage, or account issues.

When Claude Code pops up a permission confirmation dialog, this tool pushes a notification to your phone via WeChat (企业微信).

## How it works

```
Claude Code permission dialog
       │
       ▼
Notification Hook (settings.json)
       │
       ▼
wechat-notify.py ──HTTP──► wechat-daemon.py ──WebSocket──► 企业微信 ──► 手机微信
```

- **wechat-daemon.py** — background process that maintains a WebSocket long-connection to the WeCom server
- **wechat-notify.py** — called by Claude Code's hook, sends the notification via the local daemon

## Prerequisites

- Python 3.8+
- A WeChat Work (企业微信) account (free personal registration)
- Claude Code CLI

## Setup

### 1. Install dependencies

```bash
pip install websocket-client requests
```

### 2. Create a WeCom AI Bot

1. Open [WeChat Work Admin Console](https://work.weixin.qq.com) in browser
2. Go to **Application Management** → **Smart Bot (智能机器人)**
3. Create a bot manually, select **API mode**
4. For connection method, choose **Long Connection (长连接)**
5. Copy the **BotID** and **Secret** (Secret is shown only once!)

### 3. Configure

```bash
cp wechat-notify-config.example.json wechat-notify-config.json
```

Edit `wechat-notify-config.json`:

```json
{
    "bot_id": "your-bot-id-here",
    "secret": "your-secret-here"
}
```

### 4. Configure Claude Code Hook

Add the following to your Claude Code `settings.json` (`~/.claude/settings.json` or `.claude/settings.json`):

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "python /path/to/wechat-notify.py"
          }
        ]
      }
    ]
  }
}
```

Replace `/path/to/wechat-notify.py` with the actual absolute path.

### 5. Start the daemon

```bash
python wechat-daemon.py
```

Keep this terminal window open. On first run, send any message to the bot from your phone's WeChat Work app — this captures your chat ID (one-time setup).

## Usage

1. Start the daemon: `python wechat-daemon.py`
2. Use Claude Code normally
3. Whenever Claude Code needs your approval, you'll get a WeChat notification on your phone

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No notification received | Check daemon is running and authenticated |
| "chatid not captured" | Send any message to the bot from WeChat Work on your phone |
| Connection refused | Make sure the daemon is running before notifying |
