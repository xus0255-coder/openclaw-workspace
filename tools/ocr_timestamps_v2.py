import os, sys, glob, re
from PIL import Image
import pytesseract

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SRC = r'F:\整理完成资料\3.夫妻情变\2021年'
out_pdf = os.path.join(SRC, '聊天记录截图_new.pdf')

files = sorted(glob.glob(os.path.join(SRC, 'Screenshot_*.jpg')))

# 从 OCR 文本中提取"2021 年 X 月 X 日 HH:MM"格式的时间
def parse_ocr_time(text):
    # 匹配 "2021 年 2 月 4 日 21:01" 或 "2021 年 2 月 4 日 21:01" 等
    matches = re.findall(r'2021\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日\s*(\d{1,2}):(\d{2})', text)
    if matches:
        # 取最后一个（聊天记录越往后时间越大）
        m = matches[-1]
        return f"2021{int(m[0]):02d}{int(m[1]):02d}{int(m[2]):02d}{int(m[3]):02d}"
    return None

# 也从文件名提取作为备用
def parse_filename_time(filepath):
    fn = os.path.basename(filepath)
    m = re.search(r'Screenshot_(\d{8})_(\d{6})', fn)
    if m:
        return f"{m.group(1)}{m.group(2)}"
    return None

# 分析所有截图
print("=" * 60)
results = []
for f in files:
    img = Image.open(f)
    text = pytesseract.image_to_string(img, lang='chi_sim+eng')
    ocr_ts = parse_ocr_time(text)
    fn_ts = parse_filename_time(f)
    results.append((f, ocr_ts, fn_ts, text[:150]))

print("\n时间分析：")
print(f"{'文件':<50} {'OCR时间':>12} {'文件名时间':>14}")
print("-" * 76)
for f, ocr_ts, fn_ts, _ in results:
    bn = os.path.basename(f)
    print(f"{bn:<50} {str(ocr_ts):>12} {str(fn_ts):>14}")

print("\n\n最终排序（按OCR聊天时间，无则用文件名）：")
sorted_results = sorted(results, key=lambda x: x[1] if x[1] else x[2])
for i, (f, ocr_ts, fn_ts, _) in enumerate(sorted_results):
    bn = os.path.basename(f)
    ts = ocr_ts if ocr_ts else fn_ts
    print(f"  {i+1}. {bn} -> {ts}")

print("\n\n聊天内容摘要（OCR时间）：")
for f, ocr_ts, _, text in results:
    bn = os.path.basename(f)
    ts = ocr_ts or "(无OCR时间)"
    snippet = text[:120].replace('\n', ' ').strip()
    print(f"\n[{ts}] {bn}")
    print(f"  {snippet}")