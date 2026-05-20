#!/usr/bin/env python3
"""Poll libtv session for results."""
import os, sys, json, time, subprocess

os.environ["LIBTV_ACCESS_KEY"] = "sk-libtv-b2ff262d988241eaa5fa7245bbbe4093"

SID = "32429d09-dc78-41e0-9654-e60e6bd3b465"
SCRIPTS = os.path.join(os.environ["USERPROFILE"], ".openclaw", "skills", "libtv-skill", "scripts")
QUERY = os.path.join(SCRIPTS, "query_session.py")
DOWNLOAD = os.path.join(SCRIPTS, "download_results.py")
OUTPUT = os.path.join(os.environ["USERPROFILE"], "Desktop", "fujian_poster")
ENV = {**os.environ, "LIBTV_ACCESS_KEY": "sk-libtv-b2ff262d988241eaa5fa7245bbbe4093"}

print("Polling for image result...")
for i in range(30):
    time.sleep(8)
    r = subprocess.run([sys.executable, QUERY, SID], capture_output=True, text=True, timeout=30, env=ENV)
    if r.returncode != 0:
        print(f"[{i+1}] error: {r.stderr[:200]}")
        continue
    try:
        data = json.loads(r.stdout)
        messages = data.get("messages", [])
        status = data.get("status", "unknown")
        
        # Check for completed images
        for m in messages:
            if m.get("role") == "assistant" and m.get("content"):
                for c in m["content"]:
                    if c.get("type") == "image" and c.get("image", {}).get("url"):
                        url = c["image"]["url"]
                        print(f"\n✅ IMAGE GENERATED! (poll {i+1})")
                        print(f"URL: {url}")
                        
                        # Download
                        os.makedirs(OUTPUT, exist_ok=True)
                        dl = subprocess.run(
                            [sys.executable, DOWNLOAD, "--urls", url, "--output-dir", OUTPUT],
                            capture_output=True, text=True, timeout=30, env=ENV
                        )
                        print(f"Download output: {dl.stdout[:300]}")
                        if dl.stderr:
                            print(f"Download stderr: {dl.stderr[:200]}")
                        
                        print(f"Project URL: https://www.liblib.tv/canvas?projectId=1e6d6d5bb4fa43fb9df280d88f15ca2f")
                        sys.exit(0)
        
        # Also check for text/image in other message structures
        for m in messages:
            if m.get("content") and isinstance(m["content"], str) and "http" in m["content"]:
                print(f"[{i+1}] Content has URL:", m["content"][:200])
        
        print(f"[{i+1}] status={status}, messages={len(messages)}")
        
    except json.JSONDecodeError:
        print(f"[{i+1}] JSON parse error:", r.stdout[:200])
    except Exception as e:
        print(f"[{i+1}] Error:", str(e)[:200])

print("\n⏰ Timeout - image not ready yet.")
print(f"Check manually: https://www.liblib.tv/canvas?projectId=1e6d6d5bb4fa43fb9df280d88f15ca2f")
