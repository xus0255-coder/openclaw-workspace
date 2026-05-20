# OpenClaw Workspace Sync Script v2
# 自动将本地 workspace 推送到 GitHub
# 安全起见，跳过 _test_* 文件和其他临时内容

$ws = "$env:USERPROFILE\.openclaw\workspace"
$repoDir = "$env:TEMP\gh-sync"

# 确保有最新的仓库
if (-not (Test-Path $repoDir)) {
    gh repo clone xus0255-coder/openclaw-workspace $repoDir 2>&1 | Out-Null
}
Push-Location $repoDir

# 配置身份
git config user.email "xus0255@gmail.com"
git config user.name "xus0255-coder"

# 用 gh token 推
$ghToken = gh auth token 2>&1
git remote set-url origin "https://xus0255-coder:${ghToken}@github.com/xus0255-coder/openclaw-workspace.git"

# 拉取最新
git pull --rebase origin main 2>&1 | Out-Null

# 同步核心文件（安全内容）
Copy-Item "$ws\SOUL.md" . -Force
Copy-Item "$ws\USER.md" . -Force
Copy-Item "$ws\IDENTITY.md" . -Force
Copy-Item "$ws\TOOLS.md" . -Force
Copy-Item "$ws\AGENTS.md" . -Force
if (Test-Path "$ws\MEMORY.md") { Copy-Item "$ws\MEMORY.md" . -Force }

# 同步当日记忆
$today = Get-Date -Format "yyyy-MM-dd"
$todayMemory = "$ws\memory\$today.md"
if (Test-Path $todayMemory) {
    if (-not (Test-Path "memory")) { New-Item -ItemType Directory -Path "memory" -Force | Out-Null }
    Copy-Item $todayMemory "memory\" -Force
}

# 同步 tools -> 只同步非测试文件
if (Test-Path "$ws\tools") {
    $safeTools = Get-ChildItem "$ws\tools" -File -ErrorAction SilentlyContinue | Where-Object { $_.Name -notlike '_test_*' }
    foreach ($t in $safeTools) {
        Copy-Item $t.FullName "tools\" -Force
    }
}

# 提交并推送
$changed = git status --porcelain
if ($changed) {
    Write-Host "检测到变更，推送中..."
    git add -A
    git commit -m "🔄 Auto-sync $(Get-Date -Format 'yyyy-MM-dd HH:mm')" 2>&1
    git push 2>&1
    Write-Host "✅ 推送完成"
} else {
    Write-Host "✅ 无变更，跳过"
}

Pop-Location
