"""
全面OCR扫描，提取所有日期信息，逐张核对时间
"""
import os, sys, re
from PIL import Image
import pytesseract

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SRC = r'F:\整理完成资料\3.夫妻情变\2024-2025\新建文件夹'
files = sorted([f for f in os.listdir(SRC) if f.lower().endswith(('.jpg','.png','.jpeg'))])

print(f"共 {len(files)} 张截图\n")

for f in files:
    fp = os.path.join(SRC, f)
    img = Image.open(fp)
    w, h = img.size
    text = pytesseract.image_to_string(img, lang='chi_sim+eng')
    
    # 找所有2024/2025年日期
    dates = []
    for year in ['2024', '2025']:
        matches = re.findall(rf'{year}\s*年\s*(\d{{1,2}})\s*月\s*(\d{{1,2}})\s*日\s*(\d{{1,2}}):(\d{{2}})', text)
        for m in matches:
            dates.append(f"{year}-{int(m[0]):02d}-{int(m[1]):02d} {int(m[2]):02d}:{m[3]}")
    
    # 也找任何"年X月X日"模式
    year_month = re.findall(r'202[45]\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日', text)
    # 找任何月份日期组合
    month_day = re.findall(r'\d{1,2}\s*月\s*\d{1,2}\s*日\s*\d{1,2}:\d{2}', text)
    
    # 文件名时间
    fn_m = re.search(r'Screenshot_(\d{8})_(\d{6})', f)
    fn_ts = f"{fn_m.group(1)}{fn_m.group(2)}" if fn_m else "—"
    
    print("=" * 80)
    print(f"文件: {f}")
    print(f"尺寸: {w}x{h} | 文件时间: {fn_ts}")
    print(f"OCR日期: {dates}")
    print(f"全文:")
    print(text)
    print()