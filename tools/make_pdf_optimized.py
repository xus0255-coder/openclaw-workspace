"""
聊天截图 → PDF（优化版）
在正式版基础上增加：页码、页眉日期范围、图底时间标签
"""
import os, sys, glob, re
from PIL import Image
import pytesseract
from fpdf import FPDF

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SRC = r'F:\整理完成资料\3.过错方证据\2024-2025年\双方聊天记录'
OUT_PDF = os.path.join(SRC, '聊天记录截图_优化版.pdf')

PAGE_W, PAGE_H = 297, 210
MARGIN, GAP = 7, 4
IMG_W, IMG_H = 90, 190
START_X = 8.5
IMGS_PER_PAGE = 3

MANUAL_TS = {
    'ede2a0c7': '202504132052',
    '1460a541': '202503241733',
    'd1b67b0a': '202502191518',
    '145917': '202501191853',
    '145926': '202501191853',
}

def extract_dates(text):
    results = set()
    for year in ['2024','2025','2026']:
        for m in re.finditer(rf'{year}\s*年\s*(\d+)\s*月\s*(\d+)\s*日\s*(\d+):(\d+)', text):
            results.add((f'{year}{int(m.group(1)):02d}{int(m.group(2)):02d}{int(m.group(3)):02d}{m.group(4)}', 'std'))
    return sorted(results)

def parse_fn_ts(bn):
    m = re.search(r'Screenshot_(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})', bn, re.IGNORECASE)
    return f'{m.group(1)}{m.group(2)}{m.group(3)}{m.group(4)}{m.group(5)}{m.group(6)}' if m else None

def fmt_ts(ts):
    if not ts or len(ts) < 12: return ts or '?'
    return f'{ts[:4]}-{ts[4:6]}-{ts[6:8]} {ts[8:10]}:{ts[10:12]}'

files = sorted(glob.glob(os.path.join(SRC, '*.jpg')) + glob.glob(os.path.join(SRC, '*.jpeg')) + glob.glob(os.path.join(SRC, '*.png')))
files = [f for f in files if os.path.isfile(f)]

print(f'{len(files)} images...', flush=True)

all_results = []
for fi, f in enumerate(files):
    bn = os.path.basename(f).lower()
    img = Image.open(f)
    w, h = img.size
    
    manual_found = None
    for key, val in MANUAL_TS.items():
        if key in bn:
            manual_found = val
            break
    
    if manual_found:
        ts = manual_found
    else:
        all_dates = {}
        for region_pct, region_name in [(0.30, 'T30'), (0.20, 'T20')]:
            region = img.crop((0, 0, w, int(h * region_pct)))
            for d, _ in extract_dates(pytesseract.image_to_string(region, lang='chi_sim+eng')):
                all_dates.setdefault(d, []).append(region_name)
        
        for d, _ in extract_dates(pytesseract.image_to_string(img, lang='chi_sim+eng')):
            all_dates.setdefault(d, []).append('Full')
        
        fn_ts = parse_fn_ts(bn)
        ocr_2024_2025 = [d for d in all_dates.keys() if d[:4] in ('2024','2025')]
        ocr_2026 = [d for d in all_dates.keys() if d[:4] == '2026']
        
        if ocr_2024_2025:
            ts = min(ocr_2024_2025)
        elif ocr_2026:
            ts = min(ocr_2026)
        elif fn_ts:
            ts = fn_ts
        else:
            ts = f'ZZZZ_NO_DATE_{fi:03d}'
    
    all_results.append((ts, f))
    img.close()

all_results.sort(key=lambda x: (2 if x[0].startswith('ZZZZ') else (1 if x[0].startswith('2026') else 0), x[0]))

# ===== 生成优化版PDF =====
if os.path.exists(OUT_PDF):
    try: os.remove(OUT_PDF)
    except: pass

pdf = FPDF(unit='mm', format='A4')
pdf.set_auto_page_break(auto=False)

start_y = (PAGE_H - IMG_H) / 2
sorted_files = [r[1] for r in all_results]
total_pages = (len(sorted_files) - 1) // IMGS_PER_PAGE + 1

for i in range(0, len(sorted_files), IMGS_PER_PAGE):
    pdf.add_page(orientation='L')
    batch = sorted_files[i:i + IMGS_PER_PAGE]
    page_num = i // IMGS_PER_PAGE + 1
    
    # 页眉：页码 + 时间标签
    page_ts = [r[0] for r in all_results if r[1] in batch]
    valid_ts = [t for t in page_ts if t and not t.startswith('ZZZZ')]
    left_ts = fmt_ts(valid_ts[0]) if valid_ts else ''
    right_ts = fmt_ts(valid_ts[-1]) if len(valid_ts) >= 2 else left_ts
    header = f'{page_num}/{total_pages}  {left_ts} - {right_ts}'
    
    pdf.set_font('Helvetica', '', 7)
    pdf.set_text_color(130, 130, 130)
    pdf.set_y(3)
    pdf.cell(0, 4, header, align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.set_text_color(0, 0, 0)
    
    for j, fp in enumerate(batch):
        x = START_X + j * (IMG_W + GAP)
        y = start_y
        pdf.image(fp, x=x, y=y, w=IMG_W, h=IMG_H)
        
        # 图底时间标签
        ts = [r[0] for r in all_results if r[1] == fp][0]
        label = fmt_ts(ts)
        pdf.set_font('Helvetica', '', 5)
        pdf.set_text_color(130, 130, 130)
        pdf.set_xy(x + 1, y + IMG_H + 0.5)
        pdf.cell(IMG_W - 2, 3, label)
        pdf.set_text_color(0, 0, 0)

pdf.output(OUT_PDF)
size_mb = os.path.getsize(OUT_PDF) / 1024 / 1024
print(f'Done: {OUT_PDF} | {len(sorted_files)}pics | {total_pages}pages | {size_mb:.1f}MB', flush=True)
