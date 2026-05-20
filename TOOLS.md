# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

### TTS

- 音色：zh-CN-XiaoyiNeural（小艺，女声·活泼）
- 生成脚本：C:\Users\Administrator\.openclaw\workspace\gen_voices.js
- node-edge-tts：全局安装在 AppData\Roaming\npm\node_modules\node-edge-tts
- 微信发音频用绝对Windows路径（C:/Users/...），不能用 F:/ 格式

## 下载路径
- **默认**：`F:\openclaw文件`
- 备用：`F:\workspaces`
- 测试文件：`D:\360MoveData\Users\Administrator\Documents\测试文件\`

Add whatever helps you do your job. This is your cheat sheet.

---

### Session Cleanup Tool

```bash
node C:\Users\Administrator\.openclaw\workspace\tools\sessions-cleanup.js
```

- 删除 stale lock 文件（对应 .jsonl 超过5分钟未更新的 lock）
- 清理 ghost session（< 1KB 且无 trajectory 的 .jsonl）
- 报告各 agent sessions 目录磁盘占用

### zc-stant sessions
- ~~114 个文件，24MB~~ → 清理后 71 个文件，6.2MB（2026-05-10 清理）
- 清理内容：35 个旧 .bak 备份、2 个 .reset 修复残留、8 个孤立轨迹文件、1 个 .tmp
