import os, sys, glob, re
from PIL import Image
import pytesseract

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SRC = r'F:\整理完成资料\3.过错方证据\2024-2025年\双方聊天记录'

def extract_dates(text):
    results = set()
    for year in ['2024','2025','2026']:
        for m in re.finditer(rf'{year}\s*年\s*(\d{{1,2}})\s*月\s*(\d{{1,2}})\s*日\s*(\d{{1,2}}):(\d{{2}})', text):
            results.add(f"{year}-{int(m.group(1)):02d}-{int(m.group(2)):02d} {int(m.group(3)):02d}:{m.group(4)}")
        for m in re.finditer(rf'{year}[-\/](\d{{1,2}})[-\/](\d{{1,2}})\s+(\d{{1,2}}):(\d{{2}})', text):
            results.add(f"{year}-{int(m.group(1)):02d}-{int(m.group(2)):02d} {int(m.group(3)):02d}:{m.group(4)}")
    return sorted(results)

files = sorted(glob.glob(os.path.join(SRC, '*.jpg')) + glob.glob(os.path.join(SRC, '*.jpeg')) + glob.glob(os.path.join(SRC, '*.png')))
files = [f for f in files if os.path.isfile(f)]

print(f"共 {len(files)} 张截图\n")

for f in files:
    bn = os.path.basename(f)
    img = Image.open(f)
    w, h = img.size
    
    # 顶部25%区域OCR（聊天时间通常在这里）
    top = img.crop((0, 0, w, int(h * 0.25)))
    text = pytesseract.image_to_string(top, lang='chi_sim+eng')
    dates = extract_dates(text)
    
    # 全部OCR
    text_full = pytesseract.image_to_string(img, lang='chi_sim+eng')
    dates_full = extract_dates(text_full)
    
    # 文件名时间
    fn_match = re.search(r'Screenshot_(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})', bn)
    fn_ts = f"{fn_match.group(1)}-{fn_match.group(2)}-{fn_match.group(3)} {fn_match.group(4)}:{fn_match.group(5)}:{fn_match.group(6)}" if fn_match else "N/A"
    
    # OCR原文（顶部）
    raw_top = text[:200].replace('\n', '\\n')
    
    print(f"【{bn[:35]}】")
    print(f"  文件名: {fn_ts}")
    print(f"  OCR顶部日期: {dates[:3] if dates else '无'}")
    print(f"  OCR全图日期: {dates_full[:3] if dates_full else '无'}")
    if dates:
        print(f"  取用: {dates[0]}")
    print(f"  原文顶部: {raw_top}")
    print()
    
    img.close()
