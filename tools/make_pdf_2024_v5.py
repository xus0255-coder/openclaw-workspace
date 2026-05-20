"""
聊天截图 → PDF，精确OCR时间排序，最后5张已仔细看图
"""
import os, sys, re
from PIL import Image
import pytesseract
from fpdf import FPDF

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SRC = r'F:\整理完成资料\3.夫妻情变\2024-2025\新建文件夹'
OUT_PDF = os.path.join(SRC, '聊天记录截图.pdf')

PAGE_W = 297; PAGE_H = 210
MARGIN = 7; GAP = 4; IMG_W = 90; IMG_H = 190
START_X = 8.5; IMGS_PER_PAGE = 3

def extract_times(text):
    results = set()
    for year in ['2024', '2025']:
        matches = re.findall(rf'{year}\s*年\s*(\d{{1,2}})\s*月\s*(\d{{1,2}})\s*日\s*(\d{{1,2}}):(\d{{2}})', text)
        for m in matches:
            results.add(f"{year}{int(m[0]):02d}{int(m[1]):02d}{int(m[2]):02d}{m[3]}")
    return sorted(results)

def parse_screenshot_fn(fn):
    m = re.search(r'Screenshot_(\d{8})_(\d{6})', fn)
    return f"{m.group(1)}{m.group(2)}" if m else None

files = [os.path.join(SRC, f) for f in os.listdir(SRC) if f.lower().endswith(('.jpg','.png','.jpeg'))]
files = [f for f in files if os.path.isfile(f)]

print(f"共 {len(files)} 张截图\nOCR中...\n")

results = []
for f in files:
    bn = os.path.basename(f)
    img = Image.open(f)
    w, h = img.size
    text = pytesseract.image_to_string(img, lang='chi_sim+eng')
    
    # 全图OCR + 顶部OCR双重检测
    all_times = extract_times(text)
    if not all_times:
        # 顶部20%区域再试
        top = img.crop((0, 0, w, int(h*0.2)))
        top_text = pytesseract.image_to_string(top, lang='chi_sim+eng')
        all_times = extract_times(top_text)
    
    ocr_ts = all_times[0] if all_times else None
    fn_ts = parse_screenshot_fn(bn)
    
    # ===== 手动修正（基于仔细看图）=====
    # 1460a541: 顶部文本含"2025532448 17:33" → 2025年3月24日 17:33
    if '1460a541' in bn and not ocr_ts:
        ocr_ts = '202503241733'
    # 14a5c252: 顶部清晰显示"2025年4月15日 02:20" ✅
    if '14a5c252' in bn and not ocr_ts:
        ocr_ts = '202504150220'
    # 99d6d05e: 顶部含"2025%F3A 25H 20:22" → 2025年3月25日 20:22
    if '99d6d05e' in bn and not ocr_ts:
        ocr_ts = '202503252022'
    # ede2a0c7: 顶部含"2025%F45 134 20:52" → 2025年4月15日 20:52
    if 'ede2a0c7' in bn and not ocr_ts:
        ocr_ts = '202504132052'  # 用户确认4月13-14日
    # Screenshot 连续截图 
    if '145917' in bn and not ocr_ts:
        ocr_ts = '202501191315'
    if '145926' in bn and not ocr_ts:
        ocr_ts = '202501191316'
    if '145949' in bn and not ocr_ts:
        ocr_ts = '202501191317'
    # 75fd5a0a: 含"年3月30日 11:20"（2025年3月30日）
    if '75fd5a0a' in bn and not ocr_ts:
        ocr_ts = '202503301120'
    # d1b67b0a: 含"202572198 15:13"（2025年2月19日 15:13）
    if 'd1b67b0a' in bn and not ocr_ts:
        ocr_ts = '202502191513'
    
    ts = ocr_ts if ocr_ts else fn_ts
    results.append((ts, f, ocr_ts, fn_ts, text[:300]))

results.sort(key=lambda x: (x[0] is None, x[0]))
sorted_files = [r[1] for r in results]

# 核对输出
print(f"\n{'='*80}")
print(f"排序结果核对（共{len(results)}张）：")
print(f"{'#':<4} {'文件名':<48} {'时间戳':<16} {'来源':<10}")
print('-' * 80)
unresolved = []
for i, (ts, f, ocr_ts, fn_ts, _) in enumerate(results):
    bn = os.path.basename(f)
    if ocr_ts and ocr_ts[:4] in ['2024','2025']:
        src = "OCR" if all_times else "看图"
    elif ocr_ts and any(x in bn for x in ['145917','145926','145949','75fd5a0a','d1b67b0a',
        '1460a541','14a5c252','99d6d05e','ede2a0c7']):
        src = "看图🔍"
    elif fn_ts:
        src = "文件名"
    else:
        src = "无"
        unresolved.append(f"  #{i+1} {bn}")
    
    print(f"{i+1:<4} {bn:<48} {str(ts):<16} {src}")

if unresolved:
    print(f"\n⚠️ 仍有无法确定时间的：")
    for u in unresolved:
        print(u)

# 生成PDF
start_y = (PAGE_H - IMG_H) / 2
if os.path.exists(OUT_PDF):
    try: os.remove(OUT_PDF)
    except: pass

pdf = FPDF(unit='mm', format='A4')
pdf.set_auto_page_break(auto=False)

print(f"\n{'='*80}")
print("PDF页序：")
for i in range(0, len(sorted_files), IMGS_PER_PAGE):
    pdf.add_page(orientation='L')
    batch = sorted_files[i:i + IMGS_PER_PAGE]
    for j, fp in enumerate(batch):
        pdf.image(fp, x=START_X + j*(IMG_W+GAP), y=start_y, w=IMG_W, h=IMG_H)
    names = [os.path.basename(f)[:22] for f in batch]
    times = [str(results[sorted_files.index(fp)][0])[:15] for fp in batch]
    print(f"  第{i//IMGS_PER_PAGE+1}页: {' | '.join(f'{n} [{t}]' for n,t in zip(names,times))}")

pdf.output(OUT_PDF)
pages = (len(sorted_files)-1)//IMGS_PER_PAGE + 1
print(f"\n✅ {OUT_PDF}")
print(f"   共 {len(sorted_files)} 张 / {pages} 页")