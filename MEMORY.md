# 全能秘书的记忆库

## 关于老板
- 称呼：老板 / 明明BOSS
- 语言：中文优先
- 偏好：高效、简洁、快速

## 关于我
- 名字：全能秘书
- 角色：AI全能秘书
- 风格：一步到位，先出结论，再补细节

## Agent 分工
- **main**: 全能秘书 🦞（当前唯一，日常所有任务）
- **wa-stant (已删除 2026-05-17)**: 文案创作、提示词专家
- **zc-stant (已删除 2026-05-12)**: 图片制作智能体

## 核心技能（2026-05-14 更新）

### 🔧 系统/基础
- `CLI-Anything` - CLI生成方法论
- `proactive-agent` - 主动行为模式
- `self-improving` - 自我反思+批评+学习+组织
- `cognitive-memory` - 类人记忆系统
- `smart-file-manager` - 文件管理
- `MCP管理器` + `MCP开发指南` - MCP生态
- `skill-vetter` - 安装前安全检查

### 🔍 搜索
- `多引擎搜索` - 17引擎（8中文+9全球）
- `wechat-article-search` - 微信公众号文章搜索
- `clawhub-search` - ClawHub技能搜索

### 🌐 浏览器
- `browser-automation` - browser-use CLI自动化

### 📄 文档/办公
- `word-docx` / `excel-xlsx` / `PPT 演示文稿` - Office三件套
- `PDF 文档生成` / `deck-generator` - PDF+AI配图PPT
- `markdown-converter` / `summarize-pro` - 格式转换+摘要
- `translate-en-zh` - 中英翻译

### 🎨 图片/视频
- `libtv-skill`（系统级）- liblib.tv AI生图生视频
- `jimeng-skills` / `doubao-seedance-skill` - 即梦/火山引擎
- `seedance-shot-design` / `scene-video-generator` - 分镜+视频生成
- `ocr-local` - 本地OCR（无API Key）
- `order-screenshot-ocr` - 京东淘宝订单OCR
- `zeelin-video-analysis` - 视频分析
- `质量评估` - 图文视频质量评分
- `image-enhancer` - 图片增强

### ✍️ 内容创作
- `内容工厂` - 多格式内容分发
- `短剧制作一体化` - 全链路短剧制作
- `提示词工程专家` - 系统化prompt工程
- `去AI味` - 去AI生硬感
- `video-script-writer-claw` - 视频脚本
- `social-pack` - 社交媒体内容生成
- `article-writing` / `diagram-generator` - 文章+图表

### 📡 资讯/社交
- `ai-news-collector` - AI新闻聚合
- `bilibili-hot-monitor` - B站热门日报
- `xiaohongshu-mcp` / `xiaohongshu-all-in-one` - 小红书 ✅

### 📧 邮件
- `agentmail` / `imap-smtp-email` - AI邮箱

### 💻 桌面自动化
- `pywinauto` - GUI自动化
- `AutoHotkey` - 键盘鼠标录制回放
- `desktop-control` - 桌面控制

### Workspace 全部技能（34个）
内容工厂、短剧制作一体化、多引擎搜索、browser-automation、MCP管理器、MCP开发指南、skill-vetter、cognitive-memory、self-improving、bilibili-hot-monitor、excel-xlsx、PDF 文档生成、deck-generator、去AI味、提示词工程专家、word-docx、PPT 演示文稿、ai-news-collector、clawhub-search、cli-anything、doubao-seedance-skill、jimeng-skills、markdown-converter、ocr-local、order-screenshot-ocr、proactive-agent、scene-video-generator、seedance-shot-design、smart-file-manager、summarize-pro、translate-en-zh、wechat-article-search、zeelin-video-analysis、质量评估

## 系统配置

### Gateway
- 版本：v2026.5.12
- 模式：local，port 18789，auth.token
- 主模型：deepseek/deepseek-v4-flash
- 备选：Minimax（MiniMax-M2.7）
- 并行：maxConcurrent=5, subagents=15
- 启动：任务计划"OpenClaw Gateway"
- 插件: deepseek + minimax + openrouter + memory-core + document-extract + web-readability
- 配置: valid:true, issues:[], warnings:[]

### 优化参数历史

#### 2026-04-28 初版
- maxConcurrent: 3 → 5
- subagents.maxConcurrent: 5 → 15
- compaction.reserveTokens: 500 → 1500
- compaction.keepRecentTokens: 500 → 1200
- channelHealthCheckMinutes: 30 → 60

#### 2026-05-15 最终版（当前生效）
- **bootstrapMaxChars**: 2000 → 6000 → **20000** (最终值)
- **bootstrapTotalMaxChars**: **150000**
- **compaction.reserveTokens**: 1500 → **2000**
- **compaction.keepRecentTokens**: 1200 → **1500**
- **compaction.maxHistoryShare**: 0.6 → **0.5**
- **compaction.recentTurnsPreserve**: 2 → **3**
- **compaction.postIndexSync**: **async**
- **heartbeat.every**: 30m → **45m**
- **heartbeat.lightContext**: true ✅
- **heartbeat.isolatedSession**: true ✅
- **thinking**: low → **high** (当前会话)
- **maxConcurrent**: **5**
- **subagents.maxConcurrent**: **15**

### 优化参数（2026-04-30）速度专项
- **主模型**: Minimax-M2.7 → **deepseek/deepseek-v4-flash**
- **移除main agent model覆盖**: 继承defaults
- **wa-stant (2026-05-11)**: 主模型 deepseek/deepseek-v4-flash，备用 minimax-portal → minimax
- **zc-stant (已删除 2026-05-12)**: 配置文件和workspace已清理

## Cron Jobs 永久禁用（2026-05-13 08:18）
- **老板三次明确指示**：Cron Jobs 禁止重建，永久弃用
- **执行操作**：全部 6 个已删除，`jobs.json`/`jobs-state.json` 清空并设为只读 🔒
- **根因**：Gateway 重启后 cron jobs 未持久化到磁盘，RPC 注册的临时项目会丢失
- **影响**：全部定时任务改为按需执行或心跳触发

## 2026-05-12 系统修复
- zc-stant agent 已删除（配置文件和 workspace 已清理）
- Cron Jobs 第 6/7/8 次丢失后通过 RPC 重建，但最终老板下令永久禁用
- 每日资讯推送 delivery 改为 none
- MEMORY.md 更新至 2026-05-12

## 重要规则
- 删除文件 → 移到回收站
- 不擅自更改文件结构
- 回复简洁快速，无异常时 HEARTBEAT_OK
- **所有工作完成后必须复核，确保正确**（老板2026-05-14指令）
- **图片生成**: libtv 或内置 image_generate 工具均可
- **Cron Jobs精简**: 2026-05-12 从6个减至2个（记忆整理+自我学习）

## 自我提升系统
- **学习记录**: .learnings/ (LEARNINGS / ERRORS / FEATURE_REQUESTS)
- **WAL协议**: SESSION-STATE.md 即时记录决策/纠正/偏好
- **自我学习Cron**: 每日02:00，自动分析记忆、更新配置
- **Hook**: self-learning（检测纠正信号）

## 微信连接
- 已连接 ✅ inbound正常，outbound有兼容性问题
- TTS语音：zh-CN-XiaoyiNeural（小仪）
- 发送音频用绝对路径（C:/...）

## 系统优化规范
### 排查维度
- Gateway状态、定时任务、配置、网络、磁盘

### 清理规范
- browser Cache可清、workspace旧文件可删
- 大文件移至 F:\openclaw文件\
- temp文件定期清理

## 学习笔记

### 已知问题
- **Gateway RPC**: token模式RPC超时（影响gateway/cron工具），直接写文件
- **微信outbound**: v2026.4.24+不兼容，inbound正常，outbound adapter无法加载，需等插件更新
- **SIGKILL**: exec进程会被kill，后台任务继续运行（exec并发高时触发，已限制并发）
- **wizard重置auth**: wizard configure重置auth.mode为password，注意保护
### 2026-05-09 系统修复
- Cron Jobs第5次丢失后全部重建
- 资讯推送delivery改为none（避免无channel报错）
- npm openclaw@2026.5.7（版本升级）
- exec工具恢复正常（之前频繁Aborted）
- Config系统完全健康（valid:true, issues:[], warnings:[]）
- ⚠️ 根因不明：jobs.json在gateway未重启期间多次清空，jobs存储在gateway内存中
- **每日资讯推送**: delivery.mode=none（2026-05-09修复，避免无channel报错）
- **健康检查session键**: 避免在main session繁忙时触发，改用isolated模式
- **Minimax API域名变更(2026-04-28修复)**: 旧`api.minimax.chat`→已失效，新`api.minimaxi.com`（国内）/ `api.minimax.io`（全球）
- **dreaming凝固率低**: 候选积累多但无一突破阈值（0.62封顶），持续天数无新输出。根因：short-term-recall.json损坏（已重置但恢复慢）

### 2026-05-06 Cron Jobs丢失事件
- 所有5个定时任务丢失（jobs.json空数组）
- 根因：未知（可能是gateway重启时清空或写入操作覆盖）
- 已于22:22紧急重建，全部恢复

### 2026-05-07 系统稳定期
- 5月3-7日无明显用户对话，系统进入稳定运行期
- 每日自我学习分析（22:43）完成分析后编辑MEMORY.md失败，手动补录
- Gateway于22:50重启，中断2个cron job（健康检查+记忆整理），consecutiveErrors=1
- 已知5个重复问题持续存在（RPC超时/wizard重置/cron丢失/资讯超时/dreaming无输出）
- 磁盘C: 149.9GB可用 (50.7%)
- 主模型: deepseek/deepseek-v4-flash 运行正常

### 2026-05-11 wa-stant/zc-stant API Key 修复
- 22:21 cron job(每日记忆整理) 因 wa-stant/zc-stant 的 DeepSeek Key 无效而失败
- **Key 位置**: `~/.openclaw/agents/<agent>/agent/auth-profiles.json`（agent/子目录）
- **修复**: 替换无效 key `sk-e76e968ba3b74d7f9a64924a72c6babf` → 有效 key
- **auth-state**: 清除 lastGood cooldown 标记

### 2026-05-12 Minimax Key 失效修复
- **问题**: minimax API Key (`sk-cp-4kW6...j7ks`) 已失效（invalid api key）
- **影响范围**: 三个 agent 共享同一 key，均为 fallback 或 primary 模型
- **修复**:
  - 删除 wa-stant/zc-stant auth-profiles 中的 `minimax:cn` 条目
  - zc-stant 主模型: minimax → deepseek-v4-flash（原 primary minimax 导致每次调用都失败）
  - main/wa-stant fallback: minimax → deepseek-v4-pro
  - 清理 zc-stant auth-state 过期 cooldown 标记
- ✅ 2026-05-12 07:23 老板提供了新 Key，已替换并恢复原模型配置
  - main: primary=deepseek-v4-flash, fallback=minimax
  - wa-stant: primary=deepseek-v4-flash, fallback=minimax
  - zc-stant: primary=minimax, fallback=deepseek-v4-flash

## 2026-05-16 首次进化流程
- **🧬 EVO-20260516-001**: 成功跑通GEPA式进化流程
  - 目标: HEARTBEAT.md 心跳检查流程
  - 变体: Variant A (纵深扫描版), 得分8.25/10
  - 变更: 5项 → 7项检查（+资源扫描、异常检测、趋势追踪、自我进化）
  - 基础设施: ~/self-improving/ 目录结构已搭建（traces/ projects/ domains/ archive/）
  - 流程: 轨迹分析→目标识别→变异生成→质量评分→用户确认→应用→归档
  - 追踪: 未来7天观察效果

## 2026-05-16 全面自我检查
- **🎯 系统状态**: Gateway v2026.5.12, 4m uptime（刚启动）, 健康 ✅
- **💾 磁盘**: C: 160GB/295GB(54%), D: 180GB/293GB(61%), E: 112GB/272GB(41%), F: 76GB/90GB(84%) ✅
- **🧠 RAM**: 32GB total, 仅用4GB ✅
- **⚙️ Config**: valid:true, issues:[], warnings:[] ✅
- **🔑 Auth**: deepseek + minimax 均正常（no errors, no cooldown）
- **💻 依赖**: Tesseract 5.5.0 ✅, AutoHotkey ✅
- **📁 Sessions**: main 270文件/101MB, wa-stant 15文件/5MB, 无ghost ✅
- **🧹 清理**: wa-stant node_modules(386MB) → 已清理, workspace temp文件(3个)→ 已清理
- **📚 .learnings**: 15条LEARNINGS全部resolved/applied/monitoring ✅
- **🎨 DREAMS.md**: 最后May 12, dreaming已禁用（memory-core配置:dreaming:enabled=false）
- **🚫 Cron**: 永久禁用, jobs.json空（32字节只读）
- **⚠️ 已知未修复**: 微信outbound（外部依赖）、Brave Search key（未配置）

### 2026-05-09 系统全面自检
- 🗑️ 清理 6 个旧 config 备份、5 个旧日志、19MB 孤立 DLL
- ⚡ wa-stant 主模型 → deepseek/deepseek-v4-flash
- 🔧 bundledDiscovery → allowlist（安全修复）
- 系统整体健康、高效、干净 🦞

### 应用状态
- pywinauto 0.6.9 ✅ 已安装
- AutoHotkey 2.0.23 ✅ 已安装（C:\AutoHotkey）
- CLI-Anything ✅ 已安装

## Promoted From Short-Term Memory (2026-05-12)

<!-- openclaw-memory-promotion:memory:memory/2026-04-19.md:129:142 -->
- System: 总结：OpenClaw 近期聚焦模型升级和 UI 体验；Hermes Agent 重心在 Tool Gateway 降低门槛，v0.9 到 v0.10 迭代飞快，社区参与度也相当高。 System (untrusted): [2026-04-19 10:06:36 GMT+8] Exec failed (nova-clo, signal SIGKILL) :: izard openclaw --update # Shorthand for openclaw update Notes: - Switch channels with --channel stable|beta|dev - For global installs: auto-updates via detected package manager wh… An async command you ran earlier has completed. The result is shown in the system messages above. Handle the result internally. Do not relay it to the user unless explicitly requested. Current time: Sunday, April 19th, 2026 - 10:07 (Asia/Shanghai) / 2026-04-19 02:07 UTC user: System: [2026-04-19 10:09:28 GMT+8] Gateway restart restart ok (gateway.restart) System: auth 模式已从 password 恢复为 token，网关重启完成 System: Run: openclaw doctor --non-interactive Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK. When reading HEARTBEAT.md, use workspace file C:/Users/Administrator/.openclaw/workspace/HEARTBEAT.md (exact case). Do not read docs/heartbeat.md. Current time: Sunday, April 19th, 2026 - 10:09 (Asia/Shanghai) / 2026-04-19 02:09 UTC assistant: HEARTBEAT_OK [score=0.842 recalls=3 avg=1.000 source=memory/2026-04-19.md:129-142]


## 2026-05-14 技能精简
- **删除**: image-generation（16个文件）、logwatcher、clawhub-local（功能已并入 clawhub-search）
- **合并**: clawhub-local 的 install/update/publish CLI 操作已添加到 clawhub-search SKILL.md
- **剩余 workspace 技能**: 13 个
