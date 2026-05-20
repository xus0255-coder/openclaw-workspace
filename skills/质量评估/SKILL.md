---
name: 质量评估
description: "AI生成内容质量评估技能。评估图片质量（清晰度、构图、色彩）、文本质量（逻辑性、连贯性）和视频质量。用于短剧制作流程中的资产质量把关。当用户需要评估生成内容质量、检查图片是否达标、批量筛选优质内容时触发。"
description_zh: "AI生成内容质量评估，覆盖图片、文本、视频，提供评分和优化建议"
version: 1.0.0
category: AI生成类
---

# 质量评估技能 (Quality Assessment Skill)

## 🎯 功能概述
对AI生成的图片、文本、视频等内容进行质量评估，给出评分和优化建议，用于短剧制作流程中的自动质量把关。

## 📊 评估维度

### 图片质量评估
| 维度 | 权重 | 说明 |
|------|------|------|
| 清晰度 | 30% | 图像是否清晰，无模糊/噪点 |
| 构图 | 25% | 主体突出，视觉焦点明确 |
| 色彩 | 20% | 色彩协调，对比度适中 |
| 细节丰富度 | 15% | 细节完整，无明显失真 |
| 风格一致性 | 10% | 符合指定风格要求 |

### 文本质量评估
| 维度 | 权重 | 说明 |
|------|------|------|
| 逻辑连贯性 | 35% | 情节发展合理，逻辑通顺 |
| 语言表达 | 25% | 语言自然流畅，无语病 |
| 创意性 | 20% | 内容有新意，不落俗套 |
| 格式规范 | 20% | 符合剧本/文档格式要求 |

## 🛠️ 核心工作流

### 图片质量评估流程
```
1. 接收图片路径或URL
2. 分析图片基本属性（分辨率、格式）
3. 多维度评分（清晰度/构图/色彩/细节）
4. 综合评分计算（加权平均）
5. 生成改进建议
6. 判断是否达标（默认阈值：0.75）
```

### 批量评估流程
```
1. 接收图片列表
2. 并行评估所有图片
3. 按评分排序
4. 筛选达标图片（>= threshold）
5. 输出排序后的结果列表
6. 生成批量评估报告
```

## 🚀 使用方法

### 单图评估
```python
# 评估单张图片
result = assess_quality(
    image_path="./generated-images/character_01.png",
    thresholds={
        "clarity": 0.7,
        "composition": 0.65,
        "color": 0.7,
        "overall": 0.75
    }
)

print(f"综合评分: {result['overall']:.2f}")
print(f"是否达标: {result['passed']}")
print(f"改进建议: {result['suggestions']}")
```

### 批量评估（与libtv结合）
```python
# 生成后自动评估
images = libtv.batch_generate(prompts)
quality_results = batch_assess(images, min_score=0.75)

# 过滤达标图片
passed = [r for r in quality_results if r["passed"]]
failed = [r for r in quality_results if not r["passed"]]

print(f"通过: {len(passed)}/{len(images)}")
# 对失败的自动重试
for item in failed:
    retry_result = libtv.generate(item["prompt"])
    # ...
```

### 短剧素材质量报告
```python
def generate_quality_report(asset_list):
    """生成短剧素材质量报告"""
    report = {
        "总素材数": len(asset_list),
        "达标数": 0,
        "平均评分": 0,
        "各类型评分": {},
        "需重生成列表": []
    }
    
    for asset in asset_list:
        score = assess_quality(asset["path"])
        if score["overall"] >= 0.75:
            report["达标数"] += 1
        else:
            report["需重生成列表"].append(asset)
    
    return report
```

## 📈 评分标准

| 评分区间 | 等级 | 处理建议 |
|----------|------|----------|
| 0.90 - 1.00 | 优秀 ⭐⭐⭐⭐⭐ | 直接使用 |
| 0.80 - 0.89 | 良好 ⭐⭐⭐⭐ | 可以使用 |
| 0.75 - 0.79 | 合格 ⭐⭐⭐ | 基本可用，建议优化 |
| 0.60 - 0.74 | 较差 ⭐⭐ | 建议重新生成 |
| 0.00 - 0.59 | 不合格 ⭐ | 必须重新生成 |

## 🔗 集成技能
- **libtv-skill**: 图片生成主平台，结合质量评估实现自动重试
- **图像生成**: 备份生成平台
- **场景概念图生成**: 场景图质量把关
- **短剧制作一体化**: 全流程质量控制节点

## ⚙️ 配置参数
```yaml
quality_config:
  default_threshold: 0.75      # 默认合格阈值
  auto_retry: true             # 不合格自动重试
  max_retries: 3               # 最大重试次数
  report_format: "markdown"    # 报告输出格式
  save_reports: true           # 是否保存评估报告
  report_dir: "./quality-reports/"
```

---
**创建时间**: 2026年4月10日  
**版本**: 1.0.0  
**维护者**: 小白 (Xiao Bai)
