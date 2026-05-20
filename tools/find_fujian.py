import os, sys, json, subprocess
os.environ["LIBTV_ACCESS_KEY"] = "sk-libtv-b2ff262d988241eaa5fa7245bbbe4093"
sid = "32429d09-dc78-41e0-9654-e60e6bd3b465"
scripts = os.path.join(os.environ["USERPROFILE"], ".openclaw", "skills", "libtv-skill", "scripts")
query = os.path.join(scripts, "query_session.py")
env = {**os.environ, "LIBTV_ACCESS_KEY": "sk-libtv-b2ff262d988241eaa5fa7245bbbe4093"}

r = subprocess.run([sys.executable, query, sid], capture_output=True, text=True, timeout=30, env=env)
data = json.loads(r.stdout)
msgs = data.get("messages", [])

# Get the full tool result (message 62)
m62 = msgs[62]
tc = json.loads(m62["content"])
task_result = tc.get("task_result", {})
images = task_result.get("images", [])
for img in images:
    url = img.get("previewPath", "")
    print(f"FUJIAN POSTER URL: {url}")

# Save it to the output dir
out = os.path.join(os.environ["USERPROFILE"], "Desktop", "fujian_poster")
os.makedirs(out, exist_ok=True)

import urllib.request
local_path = os.path.join(out, "fujian_poster.png")
urllib.request.urlretrieve(url, local_path)
size = os.path.getsize(local_path)
print(f"Downloaded: {local_path} ({size/1024:.0f}KB)")
