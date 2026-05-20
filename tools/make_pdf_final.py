"""
聊天截图 → PDF，A4横向，每页3张并排
精确规格：图片 90x198mm，边距7mm，水平居中起始X=8.5mm
"""
import os, sys, glob, re
from PIL import Image
import pytesseract
from fpdf import FPDF

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SRC = r'F:\整理完成资料\3.夫妻情变\2021年'
OUT_PDF = os.path.join(SRC, '聊天记录截图_横版正式.pdf')

# 精确规格（用户指定）
PAGE_W = 297
PAGE_H = 210
MARGIN = 7        # 页面边距 mm
GAP = 4           # 图片间距 mm
IMG_W = 90        # 图片宽度 mm
IMG_H = 198       # 图片高度 mm（触达高度上限）
START_X = 8.5     # 水平居中起始 X mm

IMGS_PER_PAGE = 3

def parse_ocr_time(text):
    matches = re.findall(r'2021\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日\s*(\d{1,2}):(\d{2})', text)
    if matches:
        m = matches[-1]
        return f"2021{int(m[0]):02d}{int(m[1]):02d}{int(m[2]):02d}{int(m[3]):02d}"
    return None

def parse_filename_time(filepath):
    fn = os.path.basename(filepath)
    m = re.search(r'Screenshot_(\d{8})_(\d{6})', fn)
    if m:
        return f"{m.group(1)}{m.group(2)}"
    return None

screenshots = glob.glob(os.path.join(SRC, 'Screenshot_*.jpg'))

# OCR 提取时间并排序
results = []
for f in screenshots:
    img = Image.open(f)
    text = pytesseract.image_to_string(img, lang='chi_sim+eng')
    ocr_ts = parse_ocr_time(text)
    fn_ts = parse_filename_time(f)
    ts = ocr_ts if ocr_ts else fn_ts
    results.append((ts, f, ocr_ts, fn_ts))

results.sort(key=lambda x: x[0])
sorted_files = [r[1] for r in results]

print(f"共 {len(sorted_files)} 张截图\n")
for i, (ts, f, ocr_ts, fn_ts) in enumerate(results):
    src = ocr_ts if ocr_ts else f"[fn:{fn_ts}]"
    print(f"  {i+1}. {os.path.basename(f)} -> {src}")

# 垂直居中
start_y = (PAGE_H - IMG_H) / 2   # = 6mm

print(f"\n排版规格:")
print(f"  图片: {IMG_W} x {IMG_H} mm | 边距: {MARGIN}mm | 间距: {GAP}mm")
print(f"  水平起始X: {START_X}mm | 垂直起始Y: {start_y}mm")
print(f"  每页 {IMGS_PER_PAGE} 张并排")

# 删除旧文件
if os.path.exists(OUT_PDF):
    try:
        os.remove(OUT_PDF)
    except:
        pass

pdf = FPDF(unit='mm', format='A4')
pdf.set_auto_page_break(auto=False)

for i in range(0, len(sorted_files), IMGS_PER_PAGE):
    pdf.add_page(orientation='L')
    batch = sorted_files[i:i + IMGS_PER_PAGE]
    page_num = i // IMGS_PER_PAGE + 1

    for j, filepath in enumerate(batch):
        x = START_X + j * (IMG_W + GAP)
        y = start_y
        pdf.image(filepath, x=x, y=y, w=IMG_W, h=IMG_H)

    print(f"  第{page_num}页: {[os.path.basename(f) for f in batch]}")

pdf.output(OUT_PDF)
pages = (len(sorted_files) - 1) // IMGS_PER_PAGE + 1
print(f"\n✅ 生成完成: {OUT_PDF}")
print(f"   共 {len(sorted_files)} 张 / {pages} 页 / 每页3张并排")