"""
聊天截图 → 法院证据版PDF
排版规范：
- A4纵向，每页1-2张截图（大字清晰）
- 证据目录页（页号、内容摘要、证明事项）
- 页眉：证据编号 + 页码
- 页脚：截图时间标签
- 左侧装订留边
"""
import os, sys, glob, re
from PIL import Image
import pytesseract
from fpdf import FPDF

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SRC = r'F:\整理完成资料\3.情变证据\2024-2025年\双方聊天记录'
OUT_PDF = os.path.join(SRC, '聊天记录截图_证据版.pdf')

# A4纵向规格
PAGE_W, PAGE_H = 210, 297  # portrait
LEFT_MARGIN = 25    # 装订边
RIGHT_MARGIN = 15
TOP_MARGIN = 20
BOTTOM_MARGIN = 15
CONTENT_W = PAGE_W - LEFT_MARGIN - RIGHT_MARGIN  # 170mm
IMGS_PER_PAGE = 2  # 每页2张，更清晰

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
    if not ts or len(ts) < 12: return ts or '??'
    return f'{ts[:4]}年{ts[4:6]}月{ts[6:8]}日 {ts[8:10]}:{ts[10:12]}'

# ===== OCR处理 + 排序 =====
files = sorted(glob.glob(os.path.join(SRC, '*.jpg')) + glob.glob(os.path.join(SRC, '*.jpeg')) + glob.glob(os.path.join(SRC, '*.png')))
files = [f for f in files if os.path.isfile(f)]
print(f'共{len(files)}张截图，处理中...', flush=True)

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

sorted_files = [r[1] for r in all_results]
total_items = len(sorted_files)
total_pages = (total_items + IMGS_PER_PAGE - 1) // IMGS_PER_PAGE

# ===== 生成证据版PDF =====
if os.path.exists(OUT_PDF):
    try: os.remove(OUT_PDF)
    except: pass

pdf = FPDF(unit='mm', format='A4')
pdf.set_auto_page_break(auto=False)
pdf.add_font('CN', '', r'C:\Windows\Fonts\simhei.ttf', uni=True)

# ---- 封面 ----
pdf.add_page()
pdf.set_font('CN', '', 22)
pdf.set_y(55)
pdf.cell(0, 15, '证据材料', align='C', new_x='LMARGIN', new_y='NEXT')
pdf.set_font('CN', '', 14)
pdf.cell(0, 10, '微信聊天记录', align='C', new_x='LMARGIN', new_y='NEXT')
pdf.ln(12)
pdf.set_font('CN', '', 10)
pdf.cell(0, 7, f'共 {total_items} 张截图  |  {total_pages} 页', align='C', new_x='LMARGIN', new_y='NEXT')
pdf.cell(0, 7, '时间范围: 2024-11-19 ~ 2025-05-02', align='C', new_x='LMARGIN', new_y='NEXT')
pdf.cell(0, 7, '分类: 过错方证据', align='C', new_x='LMARGIN', new_y='NEXT')
pdf.ln(15)
pdf.set_font('CN', '', 8)
pdf.set_text_color(120,120,120)
pdf.cell(0, 5, '说明: 原始截图未经修改, 按聊天内容时间排序', align='C', new_x='LMARGIN', new_y='NEXT')

# ---- 证据目录 ----
pdf.add_page()
pdf.set_text_color(0,0,0)
pdf.set_font('CN', '', 14)
pdf.cell(0, 10, '证据目录', align='C', new_x='LMARGIN', new_y='NEXT')
pdf.ln(5)

col_w = [10, 20, 55, 55, 20]
headers = ['No.', '编号', '日期', '内容摘要', '页码']
pdf.set_font('CN', '', 7)
pdf.set_fill_color(230, 230, 230)
x_start = LEFT_MARGIN
for i, (h, w) in enumerate(zip(headers, col_w)):
    pdf.set_xy(x_start + sum(col_w[:i]), pdf.get_y())
    pdf.cell(w, 6, h, border=1, align='C', fill=True)
pdf.ln(6)

pdf.set_font('CN', '', 6)
for page_i in range(total_pages):
    start_idx = page_i * IMGS_PER_PAGE
    end_idx = min(start_idx + IMGS_PER_PAGE, total_items)
    batch = sorted_files[start_idx:end_idx]
    page_num = page_i + 1
    
    page_ts = [r[0] for r in all_results if r[1] in batch]
    valid_ts = [t for t in page_ts if t and not t.startswith('ZZZZ')]
    date_str = f'{fmt_ts(valid_ts[0])} ~ {fmt_ts(valid_ts[-1])}' if len(valid_ts) >= 2 else (fmt_ts(valid_ts[0]) if valid_ts else '')
    
    # 内容摘要
    first_img = Image.open(batch[0])
    first_text = pytesseract.image_to_string(first_img.crop((0,0,first_img.width,int(first_img.height*0.20))), lang='chi_sim+eng')
    summary = first_text[:55].replace(chr(10), ' ').replace(chr(13), '').strip()[:48]
    first_img.close()
    
    row_data = [str(start_idx+1), f'Ex.{page_i+1}', date_str[:40], summary, str(page_num)]
    row_h = 5
    for i, (d, w) in enumerate(zip(row_data, col_w)):
        pdf.set_xy(x_start + sum(col_w[:i]), pdf.get_y())
        pdf.cell(w, row_h, d, border=1, align='C' if i != 3 else 'L')
    pdf.ln(row_h)

# ---- 截图正文 ----
for page_i in range(total_pages):
    pdf.add_page()
    start_idx = page_i * IMGS_PER_PAGE
    end_idx = min(start_idx + IMGS_PER_PAGE, total_items)
    batch = sorted_files[start_idx:end_idx]
    page_num = page_i + 1
    
    # 页眉
    page_ts = [r[0] for r in all_results if r[1] in batch]
    valid_ts = [t for t in page_ts if t and not t.startswith('ZZZZ')]
    date_range = f'{fmt_ts(valid_ts[0])} ~ {fmt_ts(valid_ts[-1])}' if len(valid_ts) >= 2 else (fmt_ts(valid_ts[0]) if valid_ts else '')
    
    pdf.set_font('CN', '', 6)
    pdf.set_text_color(100, 100, 100)
    pdf.set_y(5)
    pdf.set_x(LEFT_MARGIN)
    pdf.cell(0, 4, f'Ex.{page_num}  |  {date_range}  |  Page {page_num}/{total_pages}', align='L')
    pdf.set_text_color(0, 0, 0)
    
    # 每张截图
    img_area_h = PAGE_H - TOP_MARGIN - BOTTOM_MARGIN
    gap = 4
    single_h = (img_area_h - gap) // IMGS_PER_PAGE if IMGS_PER_PAGE == 2 else img_area_h
    
    for j, fp in enumerate(batch):
        tmp = Image.open(fp)
        orig_w, orig_h = tmp.size
        tmp.close()
        
        w_scale = CONTENT_W / orig_w
        h_scale = single_h / orig_h
        scale = min(w_scale, h_scale)
        img_w = orig_w * scale
        img_h = orig_h * scale
        
        x = LEFT_MARGIN + (CONTENT_W - img_w) / 2
        y = TOP_MARGIN + j * (single_h + gap)
        
        pdf.image(fp, x=x, y=y, w=img_w, h=img_h)
        
        # 时间标注
        ts = [r[0] for r in all_results if r[1] == fp][0]
        pdf.set_font('CN', '', 5)
        pdf.set_text_color(120, 120, 120)
        pdf.set_xy(x, y + img_h + 0.3)
        pdf.cell(img_w, 3, fmt_ts(ts), align='C')
        pdf.set_text_color(0, 0, 0)

pdf.output(OUT_PDF)
size_mb = os.path.getsize(OUT_PDF) / 1024 / 1024
print(f'\n证据版PDF完成: {OUT_PDF}')
print(f'  共 {total_items} 张截图, {total_pages} 页正文 + 2页(封面+目录)')
print(f'  大小: {size_mb:.1f} MB')
print(f'  包含: 封面 / 证据目录 / 正文(每页2张, A4纵向)', flush=True)
