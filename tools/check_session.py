import os, sys, json, subprocess
os.environ["LIBTV_ACCESS_KEY"] = "sk-libtv-b2ff262d988241eaa5fa7245bbbe4093"
sid = "32429d09-dc78-41e0-9654-e60e6bd3b465"
scripts = os.path.join(os.environ["USERPROFILE"], ".openclaw", "skills", "libtv-skill", "scripts")
query = os.path.join(scripts, "query_session.py")
env = {**os.environ, "LIBTV_ACCESS_KEY": "sk-libtv-b2ff262d988241eaa5fa7245bbbe4093"}

r = subprocess.run([sys.executable, query, sid], capture_output=True, text=True, timeout=30, env=env)
data = json.loads(r.stdout)
msgs = data.get("messages", [])

print("Total:", len(msgs))
for i in range(64, len(msgs)):
    m = msgs[i]
    c = m.get("content", "")
    if isinstance(c, str):
        print(f"[{i}][{m['role']}] {c[:300]}")
        print()
    elif isinstance(c, list):
        for x in c:
            xtype = x.get("type", "?")
            if xtype == "image":
                url = x.get("image", {}).get("url", "")
                print(f"[{i}][{m['role']}] IMAGE: {url[:150]}")
            else:
                print(f"[{i}][{m['role']}] {str(x)[:200]}")
        print()
