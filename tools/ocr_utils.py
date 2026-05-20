"""
改进版OCR时间提取工具 - v2
- 双重区域OCR: 顶部20% → 全图 双重保障
- 乱码容错: 支持数字拼接模式 (202503241733)
- 多年份支持
"""
import re
from PIL import Image
import pytesseract

def extract_chat_times(img, years=['2024','2025']):
    """
    从微信截图中提取聊天时间戳
    返回: 排序后的时间列表 ['202503241733', ...]
    """
    w, h = img.size
    results = set()
    texts = []
    
    # 1) 顶部20%区域（微信日期标题栏所在位置）
    top = img.crop((0, 0, w, int(h*0.2)))
    texts.append(pytesseract.image_to_string(top, lang='chi_sim+eng'))
    
    # 2) 全图OCR
    texts.append(pytesseract.image_to_string(img, lang='chi_sim+eng'))
    
    for text in texts:
        for year in years:
            # 模式A: 标准 "2025年3月24日 17:33"
            for m in re.finditer(rf'{year}\s*年\s*(\d{{1,2}})\s*月\s*(\d{{1,2}})\s*日\s*(\d{{1,2}}):(\d{{2}})', text):
                results.add(f"{year}{int(m.group(1)):02d}{int(m.group(2)):02d}{m.group(3)}{m.group(4)}")
            
            # 模式B: 容错 "2025年3月24日 17:33"（各种乱码间隔）
            for m in re.finditer(rf'{year}\s*\S*\s*(\d{{1,2}})\s*\S*\s*(\d{{1,2}})\s*\S*\s*(\d{{1,2}}):(\d{{2}})', text):
                if '年' in m.group() or '月' in m.group() or '日' in m.group():
                    results.add(f"{year}{int(m.group(1)):02d}{int(m.group(2)):02d}{m.group(3)}{m.group(4)}")
            
            # 模式C: 数字拼接 "202503241733" → 还原为时间
            for m in re.finditer(rf'{year}(\d{{6}})\s*(\d{{2}}):(\d{{2}})', text):
                d = m.group(1)
                results.add(f"{year}{d[:2]}{d[2:4]}{d[4:6]}")  # 注意这里的时间是拼接在数字中
            
            # 模式D: "年X月X日 HH:MM" 无年份→取当前年份
            for m in re.finditer(r'(\d{1,2})\s*月\s*(\d{1,2})\s*日\s*(\d{1,2}):(\d{2})', text):
                pass  # 由模式A/B覆盖
    
    # 模式C特殊处理 - 从连续数字中提取"年年月月日日时时分分"
    for text in texts:
        for year in years:
            for m in re.finditer(rf'{year}(\d{{2}})(\d{{2}})(\d{{2}})\s+\d{{2}}:\d{{2}}', text):
                results.add(f"{year}{m.group(1)}{m.group(2)}{m.group(3)}00")
    
    return sorted(results)


def extract_earliest_chat_time(img, years=['2024','2025']):
    """取最早时间"""
    times = extract_chat_times(img, years)
    return times[0] if times else None
