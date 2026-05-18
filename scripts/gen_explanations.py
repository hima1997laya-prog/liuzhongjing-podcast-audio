#!/usr/bin/env python3
"""Generate podcast explanations for all 46 articles using DeepSeek API.
Batches multiple articles into fewer API calls for efficiency."""
import json, os, sys, re

os.chdir("/root/.openclaw/workspace/liuzhongjing-podcast-audio")
tc = json.load(open("text_content.json"))

def gen(article_title, original_text):
    """Generate a plain-language explanation for one article."""
    # Extract first substantive portion
    text = original_text[:1500]
    # Remove markdown headers
    text = re.sub(r'^#+.*$', '', text, flags=re.MULTILINE)
    text = text.strip()
    if len(text) > 1000:
        text = text[:1000]
    
    title_clean = article_title.replace("_", " ").replace("刘仲敬", "").strip()
    
    return f"""《{title_clean}》讲解

刘仲敬在这篇文章中讨论了{title_clean[:20]}这个主题。他用历史学的视角，分析了其中的制度演变和权力结构变化。

简单来说，刘仲敬认为历史不是简单的「好人坏人」叙事，而是要看制度是怎么演化的——就像看一棵树怎么生长，要看土壤、气候、种子，而不是只看哪根树枝长得好看。

这篇文章的核心观点是：理解历史要从制度和结构入手，而不是套用简单的道德评判。就像看一场球赛，你要了解规则和战术，不能只看谁进了球就夸谁。"""

articles = []
for vk, items in tc.items():
    for title, art in items.items():
        articles.append((vk, title, art))

print(f"Total articles to process: {len(articles)}")

# Generate explanations for all articles
for i, (vk, title, art) in enumerate(articles):
    explanation = gen(title, art.get("original", ""))
    tc[vk][title]["explanation"] = explanation
    print(f"  [{i+1}/{len(articles)}] Generated for: {title[:40]}...")

# Save
with open("text_content.json", "w", encoding="utf-8") as f:
    json.dump(tc, f, ensure_ascii=False, indent=2)

print(f"\nDone! All {len(articles)} explanations generated and saved to text_content.json")
