/**
 * sessions-cleanup.js — 清理 sessions 目录中的问题
 *
 * 功能：
 * 1. 删除 stale lock 文件（对应 .jsonl 超过5分钟未更新的 lock）
 * 2. 清理 ghost session（< 1KB 且无 trajectory 的 .jsonl）
 * 3. 报告各 agent 的 sessions 目录磁盘占用
 */

const fs = require('fs');
const path = require('path');

const AGENTS_DIR = path.join(process.env.USERPROFILE, '.openclaw', 'agents');
const STALE_LOCK_MINUTES = 5; // lock 超过这个时间对应的 .jsonl 未更新视为 stale
const GHOST_SESSION_MAX_BYTES = 1024; // 小于此值且无 trajectory 视为 ghost
const now = Date.now();

let totalFreed = 0;
let totalLockFiles = 0;
let totalGhostFiles = 0;
let totalStaleLocks = 0;

function getAgentSessionsDir(agentName) {
  return path.join(AGENTS_DIR, agentName, 'sessions');
}

function scanAgent(agentName) {
  const dir = getAgentSessionsDir(agentName);
  if (!fs.existsSync(dir)) return;

  console.log(`\n=== Agent: ${agentName} (${dir}) ===`);

  const files = fs.readdirSync(dir);
  const lockMap = new Map(); // sessionId -> { lockFile, lockTime }
  const jsonlMap = new Map(); // sessionId -> { file, stat }
  const trajectoryMap = new Map(); // sessionId -> trajectoryFile

  // 1. 分类文件
  for (const f of files) {
    const fullPath = path.join(dir, f);
    try {
      const stat = fs.statSync(fullPath);
      if (!stat.isFile()) continue;

      // 处理 .jsonl.lock
      if (f.endsWith('.jsonl.lock')) {
        const sessionId = f.replace('.jsonl.lock', '');
        lockMap.set(sessionId, { file: f, mtimeMs: stat.mtimeMs });
        totalLockFiles++;
        continue;
      }

      // 处理 .jsonl
      if (f.endsWith('.jsonl') && !f.includes('.trajectory')) {
        const sessionId = f.replace('.jsonl', '');
        jsonlMap.set(sessionId, { file: f, stat });
        continue;
      }

      // 处理 trajectory
      if (f.endsWith('.trajectory.jsonl')) {
        const sessionId = f.replace('.trajectory.jsonl', '');
        trajectoryMap.set(sessionId, f);
        continue;
      }
    } catch (e) {
      // skip inaccessible files
    }
  }

  // 2. 检查 stale locks
  for (const [sessionId, lockInfo] of lockMap) {
    const jsonlInfo = jsonlMap.get(sessionId);
    if (!jsonlInfo) {
      // 没有对应的 .jsonl 文件，lock 是孤立的
      const lockPath = path.join(dir, lockInfo.file);
      const size = fs.statSync(lockPath).size;
      fs.unlinkSync(lockPath);
      totalFreed += size;
      totalStaleLocks++;
      console.log(`  🗑️ Stale lock (no jsonl): ${lockInfo.file}`);
      continue;
    }

    // 有对应的 .jsonl，检查是否超过 STALE_LOCK_MINUTES 未更新
    const ageMs = now - jsonlInfo.stat.mtimeMs;
    const ageMinutes = ageMs / 60000;
    if (ageMinutes > STALE_LOCK_MINUTES) {
      const lockPath = path.join(dir, lockInfo.file);
      const size = fs.statSync(lockPath).size;
      fs.unlinkSync(lockPath);
      totalFreed += size;
      totalStaleLocks++;
      console.log(`  🗑️ Stale lock (jsonl idle ${Math.round(ageMinutes)}m): ${lockInfo.file}`);
    }
  }

  // 3. 检查 ghost session（极小且无 trajectory 的 .jsonl）
  for (const [sessionId, info] of jsonlMap) {
    if (info.stat.size < GHOST_SESSION_MAX_BYTES && !trajectoryMap.has(sessionId)) {
      // 检查是否被 lockMap 引用（如果有 lock 且 jsonl 很小但可能活跃）
      if (lockMap.has(sessionId)) continue;

      const jsonlPath = path.join(dir, info.file);
      const size = info.stat.size;
      fs.unlinkSync(jsonlPath);
      totalFreed += size;
      totalGhostFiles++;
      console.log(`  🗑️ Ghost session (${size}B, no trajectory): ${info.file}`);
    }
  }

  // 4. 计算目录总大小
  let dirSize = 0;
  for (const f of files) {
    const fp = path.join(dir, f);
    try { dirSize += fs.statSync(fp).size; } catch (e) {}
  }
  const dirSizeMB = (dirSize / 1048576).toFixed(1);
  console.log(`  📊 Directory size: ${dirSizeMB} MB (${files.length} files)`);
}

// 扫描所有 agent
const agents = fs.readdirSync(AGENTS_DIR);
for (const agent of agents) {
  const sessionsDir = path.join(AGENTS_DIR, agent, 'sessions');
  if (fs.existsSync(sessionsDir)) {
    scanAgent(agent);
  }
}

console.log(`\n=== Summary ===`);
console.log(`  Total lock files found: ${totalLockFiles}`);
console.log(`  Stale locks removed: ${totalStaleLocks}`);
console.log(`  Ghost sessions removed: ${totalGhostFiles}`);
console.log(`  Total space freed: ${totalFreed} bytes (${(totalFreed/1048576).toFixed(2)} MB)`);
console.log(`  Status: ${totalStaleLocks + totalGhostFiles > 0 ? '✅ Cleanup performed' : '✅ Clean, no action needed'}`);
