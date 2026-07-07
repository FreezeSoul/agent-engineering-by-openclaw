#!/usr/bin/env python3
"""
生成文章地图 (Article Map) - 优化版
- 按发布时间倒序排列
- 包含目录位置和创建时间
- 输出到仓库根目录 ARTICLES_MAP.md
- 优化：单次 git log 调用获取所有文件创建日期
- 2026-07-07: 增加 Type 列（monitoring | independent）区分「系统产物」与「读者产物」
"""

import subprocess
import os
import re
from datetime import datetime

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILE = os.path.join(REPO_DIR, "ARTICLES_MAP.md")

def get_all_file_dates() -> dict:
    """一次性获取所有文件的创建日期"""
    date_map = {}
    try:
        # Single git log call to get all added files with their dates
        result = subprocess.run(
            ["git", "log", "--diff-filter=A", "--format=%ai", "--name-only", "--", "articles/"],
            cwd=REPO_DIR,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            # Format from `git log --diff-filter=A --format=%ai --name-only`:
            #   date_line (e.g. "2026-06-17 10:07:14 +0800")
            #   blank line
            #   filename_line(s) (one or more .md files, each on own line)
            #   ... repeats for each commit
            i = 0
            while i < len(lines):
                date_line = lines[i].strip()
                # Date lines start with a digit (year)
                if date_line and date_line[0].isdigit():
                    date_str = date_line.split()[0]  # "YYYY-MM-DD"
                    i += 1
                    while i < len(lines):
                        filename_line = lines[i].strip()
                        if not filename_line:  # skip blank lines
                            i += 1
                            continue
                        if filename_line[0].isdigit():  # next date line
                            break
                        if '/' in filename_line and filename_line.endswith('.md'):
                            date_map[filename_line] = date_str
                        i += 1
                else:
                    i += 1
    except Exception as e:
        print(f"Warning: git log failed: {e}")
    return date_map

def extract_title(filepath: str) -> str:
    """从文章中提取标题（第一个 # 开头的内容）"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("# "):
                    return line[2:].strip()
    except Exception:
        pass
    return os.path.basename(filepath).replace(".md", "")


# === 2026-07-07: 文章类型分类 ===
# 区分「monitoring」（R-round 系统产物，不发布头条）和「independent」（读者向深度文）
def classify_article(filename: str) -> str:
    """根据文件名模式判断文章类型

    monitoring 特征（命中任一即 monitoring）：
    - 包含 R\d{3}-phase-、R\d{3}-stars-、R\d{3}-cluster- 等监测快照模式
    - 包含 cluster-signal、phase-N、baseline-boost、rebound-confirmed 等方法论术语

    其他默认为 independent（读者向深度文）
    """
    fn = filename.lower()

    # Monitoring 报告的典型文件命名模式
    monitoring_patterns = [
        # R\d{3} 状态码 + monitoring 上下文（高优先级）
        r"-r\d{3}-(phase|stars|cluster|break|rebound|update|round|stagnant|baseline|rate|calibration|tracking|sustained)",
        # R\d{3} + BREAK 预测
        r"-r\d{3}-[\d.]+k-break",
        # 监测方法论术语
        r"cluster-signal",
        r"phase-\d",
        r"baseline-boost",
        r"rebound-confirmed",
        r"calibration-shift",
        r"rate-extrap",
        r"p-tracking",
        r"-sustained-\d",
        r"-stars-r\d{3}-",
    ]

    for pat in monitoring_patterns:
        if re.search(pat, fn):
            return "monitoring"

    return "independent"

def get_all_articles():
    """遍历 articles/ 目录获取所有 .md 文件"""
    articles_dir = os.path.join(REPO_DIR, "articles")
    if not os.path.exists(articles_dir):
        return []

    # Get all file dates in one git call
    file_dates = get_all_file_dates()

    articles = []
    for root, _, files in os.walk(articles_dir):
        for filename in sorted(files):
            if filename.endswith(".md"):
                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, REPO_DIR)
                title = extract_title(filepath)
                date = file_dates.get(rel_path, "unknown")
                category = rel_path.split(os.sep)[1] if os.sep in rel_path else "root"
                article_type = classify_article(rel_path)
                articles.append({
                    "title": title,
                    "path": rel_path,
                    "category": category,
                    "date": date,
                    "type": article_type
                })
    return articles

def sort_key(article):
    """排序：日期倒序，未知日期排最后"""
    date_str = article["date"]
    if date_str == "unknown":
        return (1, "9999-99-99")
    return (0, date_str)

def generate_map():
    """生成文章地图 Markdown"""
    articles = get_all_articles()
    articles.sort(key=sort_key, reverse=True)

    lines = [
        "# 📚 Article Map\n",
        f"> Auto-generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        f"> Total articles: {len(articles)}\n",
        "---\n",
        "",
        "| # | Title | Category | Created | Type | Path |",
        "|---|-------|----------|---------|------|------|",
    ]

    for i, art in enumerate(articles, 1):
        title = art["title"]
        category = art["category"]
        date = art["date"]
        article_type = art["type"]
        path = art["path"]
        link = f"https://github.com/FreezeSoul/agent-engineering-by-openclaw/blob/master/{path}"
        lines.append(f"| {i} | {title} | {category} | {date} | {article_type} | [{path}]({link}) |")

    # === 2026-07-07: 增加类型分布统计 ===
    type_counter = {}
    for art in articles:
        t = art["type"]
        type_counter[t] = type_counter.get(t, 0) + 1

    lines.extend([
        "",
        "---",
        "",
        "## 📊 Type Distribution",
        "",
    ])
    for t, count in sorted(type_counter.items(), key=lambda x: -x[1]):
        lines.append(f"- **{t}**: {count} 篇")

    return "\n".join(lines)

def main():
    print(f"📊 Generating article map for: {REPO_DIR}")
    content = generate_map()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Article map generated: {OUTPUT_FILE}")

    # 统计各类别数量
    articles = get_all_articles()
    categories = {}
    type_counter = {}
    for art in articles:
        cat = art["category"]
        categories[cat] = categories.get(cat, 0) + 1
        t = art["type"]
        type_counter[t] = type_counter.get(t, 0) + 1

    print("\n📂 Category breakdown:")
    for cat, count in sorted(categories.items()):
        print(f"   {cat}: {count}")

    print("\n🏷️  Type breakdown:")
    for t, count in sorted(type_counter.items(), key=lambda x: -x[1]):
        print(f"   {t}: {count}")

if __name__ == "__main__":
    main()
