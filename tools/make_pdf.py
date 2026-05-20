import os, sys, glob, re
from PIL import Image
import pytesseract
from fpdf import FPDF

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SRC = r'F:\整理完成资料\3.过错方证据\2024-2025年\双方聊天记录'
OUT_PDF = os.path.join(SRC, '聊天记录截图.pdf')

PAGE_W, PAGE_H = 297, 210
MARGIN, GAP = 7, 4
IMG_W, IMG_H = 90, 198
START_X = 8.5
IMGS_PER_PAGE = 3

# ===== 手动修正（OCR确认后的精确日期）=====
MANUAL_TS = {
    'ede2a0c7': '202504132052',  # OCR确认: 2025年4月13日 20:52
    '1460a541': '202503241733',  # OCR原文"20255635 248 17:33" = 2025年3月24日 17:33
    'd1b67b0a': '202502191518',  # 与7255b42c同段对话(22:31), 推断2025-02-19前后
    '145917': '202501191853',  # 夹在scr_145848(2025-01-19)和scr_145949(2025-01-19)之间
    '145926': '202501191853',  # 与scr_145917同时截, 同段对话
}

def extract_dates(text):
    results = set()
    for year in ['2024','2025','2026']:
        # 标准: 2024年11月19日 16:46
        for m in re.finditer(rf'{year}\s*年\s*(\d+)\s*月\s*(\d+)\s*日\s*(\d+):(\d+)', text):
            results.add((f'{year}{int(m.group(1)):02d}{int(m.group(2)):02d}{int(m.group(3)):02d}{m.group(4)}', 'std'))
        # 乱码: 2025F3A 25H 20:22
        for m in re.finditer(rf'{year}\s*[^\d\s\n]{{1,3}}\s*(\d+)\s*[^\d\s\n]{{1,3}}\s*(\d+)\s*[^\d\s\n]{{1,3}}\s*(\d+)[:.：](\d+)', text):
            mon, day, h, mi = int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4)
            if 1 <= mon <= 12 and 1 <= day <= 31 and 0 <= h <= 23:
                results.add((f'{year}{mon:02d}{day:02d}{h:02d}{mi}', 'garbled'))
        # 极度乱码: "20255635 248 17:33" → 数字代替了年月日
        for m in re.finditer(rf'{year}(\d)(\d+)\s+(\d+)\s+(\d+):(\d+)', text):
            # Try to interpret: first digit after year might be garbled 年
            rest = m.group(2)
            if len(rest) >= 2:
                mon = int(rest[:2])
                day_idx = 2
                if 1 <= mon <= 12:
                    for end in range(day_idx + 1, min(len(rest), day_idx + 3)):
                        day = int(rest[day_idx:end])
                        if 1 <= day <= 31:
                            h, mi = int(m.group(4)), m.group(5)
                            if 0 <= h <= 23:
                                results.add((f'{year}{mon:02d}{day:02d}{h:02d}{mi}', 'heavily-garbled'))
    return sorted(results)

def parse_fn_ts(bn):
    m = re.search(r'Screenshot_(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})', bn, re.IGNORECASE)
    return f'{m.group(1)}{m.group(2)}{m.group(3)}{m.group(4)}{m.group(5)}{m.group(6)}' if m else None

files = sorted(glob.glob(os.path.join(SRC, '*.jpg')) + glob.glob(os.path.join(SRC, '*.jpeg')) + glob.glob(os.path.join(SRC, '*.png')))
files = [f for f in files if os.path.isfile(f)]

print(f'共 {len(files)} 张，OCR中...\n', flush=True)

all_results = []
for fi, f in enumerate(files):
    bn = os.path.basename(f).lower()
    img = Image.open(f)
    w, h = img.size
    
    # === 先检查手动修正 ===
    manual_found = None
    for key, val in MANUAL_TS.items():
        if key in bn:
            manual_found = val
            break
    
    if manual_found:
        ts = manual_found
        src_label = 'manual'
    else:
        # === OCR多区域识别 ===
        all_dates = {}
        
        for region_pct, region_name in [(0.30, 'T30'), (0.20, 'T20')]:
            region = img.crop((0, 0, w, int(h * region_pct)))
            text = pytesseract.image_to_string(region, lang='chi_sim+eng')
            for d, _ in extract_dates(text):
                all_dates.setdefault(d, []).append(region_name)
        
        # 全图（尽快识别一次）
        text_full = pytesseract.image_to_string(img, lang='chi_sim+eng')
        for d, _ in extract_dates(text_full):
            all_dates.setdefault(d, []).append('Full')
        
        fn_ts = parse_fn_ts(bn)
        
        # 决策：优先用2024-2025的OCR日期
        ocr_2024_2025 = [d for d in all_dates.keys() if d[:4] in ('2024','2025')]
        ocr_2026 = [d for d in all_dates.keys() if d[:4] == '2026']
        
        if ocr_2024_2025:
            ts = min(ocr_2024_2025)
            src_label = f'OCR({",".join(all_dates[ts])})'
        elif ocr_2026:
            ts = min(ocr_2026)
            src_label = f'OCR({",".join(all_dates[ts])})'
        elif fn_ts:
            ts = fn_ts
            src_label = 'fn'
        else:
            ts = f'ZZZZ_NO_DATE_{fi:03d}'
            src_label = 'none'
    
    print(f'  [{fi+1:2d}] {ts:<20} {os.path.basename(f):<45} [{src_label}]', flush=True)
    all_results.append((ts, f, src_label))
    img.close()

# 排序：2024-2025最先，2026次之，无日期最后
all_results.sort(key=lambda x: (
    2 if x[0].startswith('ZZZZ') else (1 if x[0].startswith('2026') else 0),
    x[0]
))

print(f'\n排序结果:', flush=True)
for i, (ts, f, src) in enumerate(all_results):
    print(f'  {i+1}. {ts} {os.path.basename(f)[:45]} [{src}]', flush=True)

# ===== 生成PDF =====
start_y = (PAGE_H - IMG_H) / 2

if os.path.exists(OUT_PDF):
    try: os.remove(OUT_PDF)
    except: pass

pdf = FPDF(unit='mm', format='A4')
pdf.set_auto_page_break(auto=False)

sorted_files = [r[1] for r in all_results]

print(f'\nPDF生成...', flush=True)
for i in range(0, len(sorted_files), IMGS_PER_PAGE):
    pdf.add_page(orientation='L')
    batch = sorted_files[i:i + IMGS_PER_PAGE]
    page_num = i // IMGS_PER_PAGE + 1
    
    for j, fp in enumerate(batch):
        x = START_X + j * (IMG_W + GAP)
        y = start_y
        pdf.image(fp, x=x, y=y, w=IMG_W, h=IMG_H)
    
    ts_list = [r[0] for r in all_results if r[1] in batch]
    print(f'  第{page_num}页: {" | ".join(t[:12] for t in ts_list)}', flush=True)

pdf.output(OUT_PDF)
pages = (len(sorted_files) - 1) // IMGS_PER_PAGE + 1
size_mb = os.path.getsize(OUT_PDF) / 1024 / 1024
print(f'\n✅ PDF完成: {OUT_PDF} | {len(sorted_files)}张 | {pages}页 | {size_mb:.1f}MB', flush=True)
