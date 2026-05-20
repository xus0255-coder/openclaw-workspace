"""
截图 → PDF，每页3张满铺排列
布局: A4横版，3列横排，参考购物订单截图样式
"""
import os, glob, time
from PIL import Image
from fpdf import FPDF

SRC_DIR = r'F:\整理完成资料\3.夫妻情变\2021年'
OUT_PDF = r'F:\整理完成资料\3.夫妻情变\2021年\聊天记录截图.pdf'

PAGE_W, PAGE_H = 297, 210  # A4 横置 mm
IMGS_PER_PAGE = 3

files = sorted(glob.glob(os.path.join(SRC_DIR, 'Screenshot_*.jpg')))
print(f"共 {len(files)} 张截图 -> {len(files)//IMGS_PER_PAGE + (1 if len(files)%IMGS_PER_PAGE else 0)} 页")

# 每张图: 高度=页高210mm，宽度按原比例(1088x2400)等比
img_aspect = 1088 / 2400
img_h = PAGE_H
img_w = img_h * img_aspect  # 约 95.2mm

# 3张图片总宽 = 3*img_w + 2*gap，需 ≤ PAGE_W - 2*margin
# 参考原PDF: gap≈4mm, margin≈1.7mm
GAP = 4
MARGIN = (PAGE_W - (3 * img_w + 2 * GAP)) / 2  # 自动计算

print(f"图片: {img_w:.1f} x {img_h:.1f} mm | 间距: {GAP}mm | 边距: {MARGIN:.1f}mm")

# 先删旧文件（可能被占用）
if os.path.exists(OUT_PDF):
    try:
        os.remove(OUT_PDF)
        print("已删除旧PDF")
    except:
        # 如果被占用，输出到临时路径
        OUT_PDF = os.path.join(SRC_DIR, f'聊天记录截图_{int(time.time())}.pdf')
        print(f"旧文件被占用，改输出到: {os.path.basename(OUT_PDF)}")

pdf = FPDF(unit='mm', format='A4')
pdf.set_auto_page_break(auto=False)

for i in range(0, len(files), IMGS_PER_PAGE):
    batch = files[i:i+IMGS_PER_PAGE]
    pdf.add_page(orientation='L')

    for j, f in enumerate(batch):
        x = MARGIN + j * (img_w + GAP)
        y = 0  # 顶对齐
        pdf.image(f, x=x, y=y, w=img_w, h=img_h)

    names = [os.path.basename(f).replace('Screenshot_','').replace('_com.tencent.mm.jpg','') for f in batch]
    print(f"  第{i//IMGS_PER_PAGE+1}页: {names}")

pdf.output(OUT_PDF)
print(f"\nPDF: {OUT_PDF}")
