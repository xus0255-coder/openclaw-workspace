# -*- coding: utf-8 -*-
"""
OCR筛选含"应酬"相关内容（含联想词）的微信聊天截图 -> 生成PDF
每页3张，A4横向，支持多线程加速
"""

import os, sys, glob, time
from PIL import Image
import pytesseract
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas as rlcanvas
from reportlab.lib.utils import ImageReader

FOLDER = r"F:\夫妻微信沟通"
OUTPUT = r"F:\openclaw文件\应酬证据_扩量_v2.pdf"
IMAGES_PER_PAGE = 3
MARGIN = 30
SPACING = 15

# 应酬相关关键词（含联想）
KEYWORDS = [
    # 核心词
    "应酬", "饭局", "酒局",
    # 吃饭相关
    "吃饭", "有饭吃", "晚饭", "不回来吃", "不回家吃", "不回家吃饭", "回家吃饭",
    "在外面吃", "外面吃", "没空吃", "有饭局", "在吃饭",
    "吃过了", "吃了吗", "吃完了", "吃不下", "吃完再",
    "请客", "聚餐", "订餐", "餐厅",
    # 喝酒相关
    "喝酒", "酒", "喝多了", "喝醉了", "醉酒", "喝酒去",
    "酒量", "劝酒", "倒酒", "敬酒",
    # 联想场景
    "茶桌", "泡茶", "喝茶", "茶具", "茶盘",
    "饭桌", "餐桌", "碗", "盘子", "筷子", "酒杯", "酒瓶",
    "唱歌", "KTV", "包厢", "唱歌去", "唱K",
    "应酣", "应酷", "吃反",  # OCR变体
    # 时间相关
    "晚归", "晚回", "回不来", "晚点回",
    # 客户相关
    "陪客户", "陪吃饭", "客户",
]

def ocr_image(path):
    try:
        img = Image.open(path)
        text = pytesseract.image_to_string(img, lang='chi_sim')
        return text
    except Exception as e:
        return ""

def contains_yc(text):
    if not text:
        return False
    text_no_space = text.replace(" ", "").replace("\u3000", "")
    for kw in KEYWORDS:
        if kw in text_no_space:
            return True
    return False

def make_pdf(image_paths, output_path):
    if not image_paths:
        print("[FAIL] No matching images")
        return False
    
    page_w, page_h = landscape(A4)
    img_w = (page_w - 2 * MARGIN - SPACING * (IMAGES_PER_PAGE - 1)) / IMAGES_PER_PAGE
    
    c = rlcanvas.Canvas(output_path, pagesize=landscape(A4))
    
    for i, img_path in enumerate(image_paths):
        if i % IMAGES_PER_PAGE == 0:
            if i > 0:
                c.showPage()
        
        col = i % IMAGES_PER_PAGE
        x = MARGIN + col * (img_w + SPACING)
        
        try:
            pil_img = Image.open(img_path)
            w_ratio = img_w / pil_img.width
            h_fit = pil_img.height * w_ratio
            if h_fit > page_h - 2 * MARGIN:
                h_ratio = (page_h - 2 * MARGIN) / pil_img.height
                w_fit = pil_img.width * h_ratio
                h_fit = page_h - 2 * MARGIN
            else:
                w_fit = img_w
            
            y_center = MARGIN + (page_h - 2 * MARGIN - h_fit) / 2
            c.drawImage(ImageReader(pil_img), x, y_center, width=w_fit, height=h_fit, preserveAspectRatio=True)
        except Exception as e:
            print("  [WARN] Image failed: %s -> %s" % (os.path.basename(img_path), e))
    
    c.save()
    print("[DONE] PDF: %s (%d images, %d pages)" % (output_path, len(image_paths), (len(image_paths)-1)//IMAGES_PER_PAGE+1))
    return True

def main():
    all_files = sorted(glob.glob(os.path.join(FOLDER, "*")))
    all_files = [f for f in all_files if f.lower().endswith(('.jpg','.jpeg','.png','.bmp','.webp'))]
    
    total = len(all_files)
    print("[INFO] Found %d images. OCR + expanded keywords..." % total)
    
    matched = []
    for idx, fpath in enumerate(all_files):
        fname = os.path.basename(fpath)
        sys.stdout.write("  [%d/%d] %s ... " % (idx+1, total, fname))
        sys.stdout.flush()
        text = ocr_image(fpath)
        if contains_yc(text):
            matched.append(fpath)
            print("[HIT]")
        else:
            print("[NO]")
    
    print("\n[RESULT] %d images match" % len(matched))
    
    if matched:
        matched.sort()
        for m in matched:
            print("  - %s" % os.path.basename(m))
        make_pdf(matched, OUTPUT)
    else:
        print("[RESULT] No matches found")

if __name__ == "__main__":
    main()