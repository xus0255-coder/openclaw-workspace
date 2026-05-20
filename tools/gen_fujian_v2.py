import os, sys, json, subprocess, time, urllib.request
os.environ["LIBTV_ACCESS_KEY"] = "sk-libtv-b2ff262d988241eaa5fa7245bbbe4093"
scripts = os.path.join(os.environ["USERPROFILE"], ".openclaw", "skills", "libtv-skill", "scripts")
env = {**os.environ, "LIBTV_ACCESS_KEY": "sk-libtv-b2ff262d988241eaa5fa7245bbbe4093"}

PROMPT = "生成一张福建省文化旅游海报，3D皮克斯卡通风格，带有巨大醒目的白色书法大字'福建'作为主标题。画面中心两位少女：左边穿惠安女传统服饰（蓝色短衫、黑裤、黄斗笠、花头巾），右边穿白色连衣裙戴草帽，欢快表情。背景是福建微缩景观：武夷山丹霞地貌、福建土楼圆形建筑群、鼓浪屿钢琴码头、厦门环岛路。周围漂浮宝丽来相框展示各地风景照片。底部摆放福建美食：沙县小吃、佛跳墙、海蛎煎、土笋冻、安溪铁观音茶。画面有闽南红砖古厝元素。底部微缩景观有蜿蜒河流和茶园。漂浮的三角梅和白玉兰点缀。色彩鲜艳明亮，高细节，海报设计感强"

create = os.path.join(scripts, "create_session.py")
print("Creating session...")
sys.stdout.flush()
r = subprocess.run([sys.executable, create, PROMPT], capture_output=True, text=True, timeout=120, env=env)
if r.returncode != 0:
    print("ERROR:", r.stderr)
    print("STDOUT:", r.stdout)
    sys.exit(1)
data = json.loads(r.stdout)
sid = data["sessionId"]
print(f"Session: {sid}")
sys.stdout.flush()

query = os.path.join(scripts, "query_session.py")
for i in range(40):
    time.sleep(10)
    sys.stdout.flush()
    qr = subprocess.run([sys.executable, query, sid], capture_output=True, text=True, timeout=30, env=env)
    if qr.returncode != 0:
        print(f"[{i+1}] query error")
        continue
    try:
        msgs = json.loads(qr.stdout).get("messages", [])
        # Check latest assistant messages for images
        for m in msgs[-8:]:
            ct = m.get("content", "")
            if m["role"] == "assistant" and isinstance(ct, str) and "task_result" in ct:
                tc = json.loads(ct)
                for img in tc.get("task_result", {}).get("images", []):
                    url = img.get("previewPath", "")
                    if url:
                        out = os.path.join(os.environ["USERPROFILE"], "Desktop", "fujian_poster_v2")
                        os.makedirs(out, exist_ok=True)
                        local = os.path.join(out, "fujian_poster_v2.png")
                        urllib.request.urlretrieve(url, local)
                        print(f"[{i+1}] IMAGE READY! {local} ({os.path.getsize(local)/1024:.0f}KB)")
                        sys.exit(0)
        print(f"[{i+1}] waiting... ({len(msgs)} msgs)")
        sys.stdout.flush()
    except Exception as e:
        print(f"[{i+1}] parse error: {e}")
        sys.stdout.flush()

print("Timeout")
