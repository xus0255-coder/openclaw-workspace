import os, sys, json, subprocess, re
os.environ["LIBTV_ACCESS_KEY"] = "sk-libtv-b2ff262d988241eaa5fa7245bbbe4093"
sid = "32429d09-dc78-41e0-9654-e60e6bd3b465"
scripts = os.path.join(os.environ["USERPROFILE"], ".openclaw", "skills", "libtv-skill", "scripts")
query = os.path.join(scripts, "query_session.py")
env = {**os.environ, "LIBTV_ACCESS_KEY": "sk-libtv-b2ff262d988241eaa5fa7245bbbe4093"}

r = subprocess.run([sys.executable, query, sid], capture_output=True, text=True, timeout=30, env=env)
data = json.loads(r.stdout)
msgs = data.get("messages", [])

# Find the last task with image URL
image_urls = []
for m in msgs:
    if m["role"] == "assistant" and isinstance(m.get("content"), str):
        if "task_result" in m["content"]:
            try:
                tc = json.loads(m["content"])
                if tc.get("task_result", {}).get("images"):
                    for img in tc["task_result"]["images"]:
                        url = img.get("previewPath") or img.get("url") or img.get("originalPath")
                        if url:
                            image_urls.append(url)
            except:
                pass
        # Also check for markdown image URLs in assistant text
        urls = re.findall(r'https?://[^\s)]+\.(?:png|jpg|jpeg|webp)', m["content"])
        image_urls.extend(urls)

# Deduplicate
seen = set()
unique_urls = []
for u in image_urls:
    if u not in seen:
        seen.add(u)
        unique_urls.append(u)

print(f"Found {len(unique_urls)} image URLs:")
for u in unique_urls:
    print(f"  {u[:120]}...")

# Download the last image (most recent)
if unique_urls:
    last_url = unique_urls[-1]
    print(f"\nDownloading: {last_url[:100]}...")
    out = os.path.join(os.environ["USERPROFILE"], "Desktop", "fujian_poster")
    os.makedirs(out, exist_ok=True)
    dl = os.path.join(scripts, "download_results.py")
    dr = subprocess.run([sys.executable, dl, "--urls", last_url, "--output-dir", out], 
                       capture_output=True, text=True, timeout=30, env=env)
    print("Download stdout:", dr.stdout[:300])
    if dr.stderr:
        print("Download stderr:", dr.stderr[:200])
    
    # List downloaded files
    for f in os.listdir(out):
        fp = os.path.join(out, f)
        size = os.path.getsize(fp)
        print(f"  📁 {f} ({size/1024:.0f}KB)")
else:
    print("No image URLs found. Last assistant messages:")
    for m in msgs[-3:]:
        if m["role"] == "assistant":
            print(f"  [{m['role']}] {m.get('content','')[:200]}")

print(f"\nProject URL: {data.get('projectUrl', 'N/A')}")
