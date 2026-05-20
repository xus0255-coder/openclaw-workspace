import os, sys, glob, re
from PIL import Image
import pytesseract

# 解决 Windows GBK 控制台输出
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SRC = r'F:\整理完成资料\3.夫妻情变\2021年'
out_pdf = os.path.join(SRC, '聊天记录截图_new.pdf')

files = sorted(glob.glob(os.path.join(SRC, 'Screenshot_*.jpg')))
print(f"共 {len(files)} 张截图")

# OCR 每个截图，提取时间戳
def extract_timestamp(filepath):
    img = Image.open(filepath)
    text = pytesseract.image_to_string(img, lang='chi_sim+eng')
    basename = os.path.basename(filepath)
    print(f"\nOCR: {basename}")
    print(f"  文本前300字: {text[:300].strip()}")
    
    # 尝试提取文件名自带的时间 (最可靠)
    fn_basename = os.path.basename(filepath)
    fn_match = re.search(r'Screenshot_(\d{8})_(\d{6})', fn_basename)
    if fn_match:
        date_part = fn_match.group(1)  # YYYYMMDD
        time_part = fn_match.group(2)   # HHMMSS
        return f"{date_part}_{time_part}", text
    
    return None, text

timestamps = []
for f in files:
    ts, _ = extract_timestamp(f)
    timestamps.append(ts)

print("\n\n提取的时间戳:")
for i, ts in enumerate(timestamps):
    print(f"  {os.path.basename(files[i])} -> {ts}")

print("\n文件顺序（按时间）:")
for i, f in enumerate(files):
    print(f"  {i+1}. {os.path.basename(f)} [{timestamps[i]}]")