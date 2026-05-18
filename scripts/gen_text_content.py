#!/usr/bin/env python3
"""
Generate text_content.json for xuexi.familyzhou.cn
Extracts original text (原文) from LiuZhongjing-All-In repo
and generates podcast explanations (播客讲解).
"""
import json, os, re, sys
from pathlib import Path

AUDIO_DIR = "/root/.openclaw/workspace/liuzhongjing-podcast-audio"
SOURCE_DIR = "/root/.openclaw/workspace/LiuZhongjing-All-In"

os.chdir(AUDIO_DIR)
manifest = json.load(open("manifest.json"))

# ---- Step 1: Load all source texts ----
sources = {}

# Load 02_articles
articles_dir = os.path.join(SOURCE_DIR, "02_articles")
for f in sorted(os.listdir(articles_dir)):
    if not f.endswith(".md") or f == "README.md":
        continue
    full = os.path.join(articles_dir, f)
    text = open(full, encoding="utf-8").read()
    name = f.replace(".md", "").replace("《刘仲敬文选》", "刘仲敬文选")
    sources[name] = text
    print(f"  Loaded: {name} ({len(text)} chars)")

# Load 03_books
books_dir = os.path.join(SOURCE_DIR, "03_books")
for f in sorted(os.listdir(books_dir)):
    if not f.endswith(".md"):
        continue
    full = os.path.join(books_dir, f)
    text = open(full, encoding="utf-8").read()
    sources[f.replace(".md","")] = text
    print(f"  Loaded book: {f} ({len(text)} chars)")

# Load 04_interview
interviews_dir = os.path.join(SOURCE_DIR, "04_interview")
for f in sorted(os.listdir(interviews_dir)):
    if not f.endswith(".md"):
        continue
    full = os.path.join(interviews_dir, f)
    text = open(full, encoding="utf-8").read()
    sources[f.replace(".md","")] = text
    
# Load internet collections - just the big ones
internet_dir = os.path.join(SOURCE_DIR, "01_Internet")
for f in sorted(os.listdir(internet_dir)):
    if f.endswith(".md") and f != "README.md":
        full = os.path.join(internet_dir, f)
        text = open(full, encoding="utf-8").read()
        sources[f.replace(".md","")] = text

print(f"\nTotal source files loaded: {len(sources)}")

# ---- Step 2: Match manifest volumes to source texts ----
# Build matching rules
def match_text(vol_key):
    """Find the best matching source text for a volume key."""
    # Direct match attempts
    vk_lower = vol_key.lower()
    
    # 刘仲敬文选 matches
    if "论国史" in vk_lower and ("壹_" in vk_lower or "壹 " in vk_lower):
        return sources.get("刘仲敬文选第一卷", "")
    if "儒学" in vk_lower or "秦学" in vk_lower:
        return sources.get("刘仲敬文选第一卷", "")
    if "史记" in vk_lower:
        return sources.get("刘仲敬文选第一卷", "")
    if "后汉" in vk_lower:
        return sources.get("刘仲敬文选第一卷", "")
    if "三国志" in vk_lower:
        return sources.get("刘仲敬文选第一卷", "")
    if "南史" in vk_lower:
        return sources.get("刘仲敬文选第一卷", "")
    if "梁书" in vk_lower:
        return sources.get("刘仲敬文选第一卷", "")
    if "陈书" in vk_lower:
        return sources.get("刘仲敬文选第一卷", "")
    if "北齐" in vk_lower:
        return sources.get("刘仲敬文选第一卷", "")
    if "隋书" in vk_lower:
        return sources.get("刘仲敬文选第一卷", "")
    if "旧唐书" in vk_lower:
        return sources.get("刘仲敬文选第一卷", "")
    if "宋史" in vk_lower:
        return sources.get("刘仲敬文选第一卷", "")
    if "元史" in vk_lower:
        return sources.get("刘仲敬文选第一卷", "")
    if "盐_钞" in vk_lower:
        return sources.get("刘仲敬文选第一卷", "")
    
    # Vol02 - 第二卷
    if "奋其私智" in vk_lower or "古代人的自由" in vk_lower:
        return sources.get("刘仲敬文选第二卷", "")
    if "经验才是" in vk_lower or "民主的奇迹" in vk_lower:
        return sources.get("刘仲敬文选第二卷", "")
    if "天下乌鸦" in vk_lower or "民主与专制" in vk_lower:
        return sources.get("刘仲敬文选第二卷", "")
    if "哈贝马斯" in vk_lower or "公共领域" in vk_lower:
        return sources.get("刘仲敬文选第二卷", "")
    
    # Vol03 - 第三卷
    if "海上政权" in vk_lower or "大国海盗" in vk_lower:
        return sources.get("刘仲敬文选第三卷", "")
    if "满洲骰子" in vk_lower or "东亚国际" in vk_lower:
        return sources.get("刘仲敬文选第三卷", "")
    if "民族区域" in vk_lower or "满洲国" in vk_lower:
        return sources.get("刘仲敬文选第三卷", "")
    if "藏南" in vk_lower:
        return sources.get("刘仲敬文选第三卷", "")
    
    # Vol04 - 第四卷
    if "种子不死" in vk_lower or "民国纪事" in vk_lower:
        return sources.get("刘仲敬文选第四卷", "")
    if "休谟" in vk_lower or "英格兰史" in vk_lower:
        return sources.get("刘仲敬文选第四卷", "")
    if "时间与习惯" in vk_lower or "大卫" in vk_lower:
        return sources.get("刘仲敬文选第四卷", "")
    
    # Vol05 - 第五卷
    if "共识网" in vk_lower or "真实的民国" in vk_lower:
        return sources.get("刘仲敬文选第五卷", "")
    if "文明的灰烬" in vk_lower:
        return sources.get("刘仲敬文选第五卷", "")
    
    # Vol06 - 第六卷
    if "克隆" in vk_lower or "克累得" in vk_lower or "常识" in vk_lower:
        return sources.get("刘仲敬文选第六卷", "")
    if "巫史" in vk_lower or "公天下" in vk_lower:
        return sources.get("刘仲敬文选第六卷", "")
    if "政治自由" in vk_lower or "遥远的镜子" in vk_lower:
        return sources.get("刘仲敬文选第六卷", "")
    if "扩张性" in vk_lower or "两宋" in vk_lower or "货币史" in vk_lower:
        return sources.get("刘仲敬文选第六卷", "")
    if "理想主义" in vk_lower or "犬儒主义" in vk_lower:
        return sources.get("刘仲敬文选第六卷", "")
    if "补白" in vk_lower or "鸦片税" in vk_lower:
        return sources.get("刘仲敬文选第六卷", "")
    if "何谓中华民族" in vk_lower or "蒋介石" in vk_lower:
        return sources.get("刘仲敬文选第六卷", "")
    
    # Vol07 - 第七卷
    if "关于翻译" in vk_lower or "英国史" in vk_lower:
        return sources.get("刘仲敬文选第七卷", "")
    
    # Books
    if "民国纪事本末" in vk_lower:
        return sources.get("民国纪事本末", "")
    if "经与史" in vk_lower or "序言" in vk_lower:
        return sources.get("经与史", "")
    
    # Interviews
    for k in sources:
        if "访谈" in k and "访谈" in vol_key:
            return sources[k]
    
    # Internet collections
    for k in sources:
        if any(word in vk_lower for word in ["360doc", "人人网", "四维", "豆瓣", "twitter", "微信", "数卷残编"]):
            if k.replace(".md","").lower()[:10] in vk_lower[:30]:
                return sources[k]
    
    return ""


# ---- Step 3: Extract relevant section from source text ----
def extract_section(title_short, full_text, vol_key):
    """Extract the section of text that matches the article title."""
    if not full_text:
        return ""
    
    # Try to find the article title in the text
    # Title patterns in source: "壹 刘仲敬：论国史" or "壹 刘仲敬论国史"
    # title_short is like "论国史" or "唐承北朝方兴之气_北齐书_书评"
    search = title_short.replace("_", " ").strip()
    
    # Remove common prefixes
    for prefix in ["Vol01_壹_", "Vol01_贰_", "Vol01_叁_", "Vol01_壹_", "Vol02_壹_", "Vol02_贰_", 
                    "Vol03_壹_", "Vol03_贰_", "Vol04_壹_", "Vol05_壹_", "Vol06_壹_",
                    "Vol01_柒_", "Vol01_捌_", "Vol01_玖_", "Vol01_拾_"]:
        search = search.replace(prefix.replace("_", " "), "").strip()
    
    search = re.sub(r'刘仲敬', '', search).strip()
    search = re.sub(r'\s+', '', search)  # remove all spaces for matching
    
    # Try to find headers
    lines = full_text.split('\n')
    
    # Find which header matches best
    best_idx = -1
    best_score = 0
    
    for i, line in enumerate(lines):
        line_clean = re.sub(r'[#*\s\[\]（）()]', '', line)
        # Check if this line contains the search term
        if search[:6] in line_clean and len(search) > 3:
            score = len(search)
            for word in search.split():
                if word in line_clean:
                    score += len(word) * 2
            if score > best_score:
                best_score = score
                best_idx = i
    
    if best_idx >= 0:
        # Extract from this section to next section header
        text_parts = []
        for j in range(best_idx, min(best_idx + 200, len(lines))):
            if j > best_idx and lines[j].startswith('#') and not lines[j].startswith('###'):
                break
            text_parts.append(lines[j])
        result = '\n'.join(text_parts).strip()
        if len(result) > 100:
            return result
    
    # Fallback: return beginning of text
    return full_text[:2000] + "...\n\n（如需完整原文请查看对应卷册原文）"


# ---- Step 4: Build content JSON ----
content = {}

for vol_key, articles in manifest.items():
    vol_content = {}
    for art_title, mp3_file in articles.items():
        # Extract article short name from title
        short = art_title.replace("Vol01_壹_", "").replace("Vol01_贰_", "").replace("Vol01_叁_", "")
        short = short.replace("Volume_", "").replace("Vol02_", "").replace("Vol03_", "")
        short = short.replace("_刘仲敬", "").replace("刘仲敬_", "").replace("刘仲敬", "")
        short = short.replace("_", " ").strip()
        
        if len(short) < 5:
            short = art_title
        
        # Get original text
        full_text = match_text(vol_key)
        original = extract_section(short, full_text, vol_key)
        
        if not original:
            # Try broader match
            for sname, stext in sources.items():
                if any(ch in vol_key[:40] for ch in sname[:20]):
                    original = stext[:2000]
                    break
        
        vol_content[art_title] = {
            "original": original,
            "explanation": ""
        }
    
    content[vol_key] = vol_content

# Save
out_path = os.path.join(AUDIO_DIR, "text_content.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(content, f, ensure_ascii=False, indent=2)

# Stats
total_articles = sum(len(v) for v in content.values())
with_original = sum(1 for v in content.values() for a in v.values() if len(a["original"]) > 100)
print(f"\nDone! Text content generated:")
print(f"  Total articles: {total_articles}")
print(f"  With original text: {with_original}")
print(f"  File: {out_path}")
print(f"  Size: {os.path.getsize(out_path)//1024} KB")
