#!/usr/bin/env python3
"""
Generate Simple Black & White Ghana Topics Poster from CSV

Usage:
    python generate_simple_poster.py input.csv output.html [num_topics]
eg. python3 5_generate_simple_poster.py 2025-topics_final-55.csv output.html 25
CSV Format:
    phrase,count
    Galamsey/illegal mining,9706
    Jobs,3077
    ...
"""

import csv
import sys
from pathlib import Path


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ghana Key Topics 2025</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Arial', sans-serif;
            background: white;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 0;
        }}
        
        .poster {{
            background: white;
            width: 1080px;
            height: 1080px;
            padding: 60px;
            display: flex;
            flex-direction: column;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 50px;
        }}
        
        .header h1 {{
            font-size: 42px;
            color: #000;
            font-weight: 700;
            margin-bottom: 10px;
            letter-spacing: 0;
        }}
        
        .header .subtitle {{
            font-size: 18px;
            color: #666;
            font-weight: 400;
        }}
        
        .content {{
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 18px;
        }}
        
        .topic-row {{
            display: flex;
            align-items: center;
        }}
        
        .rank {{
            font-size: 14px;
            font-weight: 400;
            color: #999;
            min-width: 35px;
            text-align: left;
        }}
        
        .topic-name {{
            font-size: 15px;
            font-weight: 400;
            color: #000;
            min-width: 260px;
        }}
        
        .bar-container {{
            flex: 1;
            height: 20px;
            background: #f5f5f5;
            margin: 0 15px;
            overflow: hidden;
        }}
        
        .bar-fill {{
            height: 100%;
            background: #000;
        }}
        
        .count {{
            font-size: 14px;
            font-weight: 400;
            color: #666;
            min-width: 70px;
            text-align: right;
        }}
        
        .footer {{
            margin-top: 40px;
            text-align: center;
            padding-top: 25px;
            border-top: 1px solid #e0e0e0;
        }}
        
        .footer .source {{
            font-size: 14px;
            color: #666;
            font-weight: 400;
        }}
    </style>
</head>
<body>
    <div class="poster">
        <div class="header">
            <h1>Ghana Key Topics 2025</h1>
            <p class="subtitle">Most frequent topics by number of news article mentions</p>
        </div>
        
        <div class="content">
{topic_rows}
        </div>
        
        <div class="footer">
            <p class="source">Source: Ghana NLP</p>
        </div>
    </div>
</body>
</html>
"""

TOPIC_ROW_TEMPLATE = """            <div class="topic-row">
                <div class="rank">{rank}</div>
                <div class="topic-name">{phrase}</div>
                <div class="bar-container">
                    <div class="bar-fill" style="width: {width:.1f}%;"></div>
                </div>
                <div class="count">{count:,}</div>
            </div>
"""


def read_csv(csv_path):
    """Read CSV file and return list of (phrase, count) tuples."""
    topics = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            phrase = row['phrase'].strip()
            count = int(row['count'])
            topics.append((phrase, count))
    return topics


def generate_html(topics, num_topics=25):
    """Generate HTML from topics list."""
    # Take top N topics
    topics = topics[:num_topics]
    
    # Find max count for percentage calculation
    max_count = max(count for _, count in topics)
    
    # Generate topic rows
    topic_rows = []
    for rank, (phrase, count) in enumerate(topics, start=1):
        width = (count / max_count) * 100
        row = TOPIC_ROW_TEMPLATE.format(
            rank=rank,
            phrase=phrase,
            count=count,
            width=width
        )
        topic_rows.append(row)
    
    # Generate final HTML
    html = HTML_TEMPLATE.format(
        num_topics=num_topics,
        topic_rows='\n'.join(topic_rows)
    )
    
    return html


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_simple_poster.py input.csv [output.html] [num_topics]")
        print("\nExample:")
        print("  python generate_simple_poster.py topics.csv")
        print("  python generate_simple_poster.py topics.csv output.html")
        print("  python generate_simple_poster.py topics.csv output.html 20")
        sys.exit(1)
    
    # Parse arguments
    input_csv = sys.argv[1]
    output_html = sys.argv[2] if len(sys.argv) > 2 else 'ghana_topics_simple.html'
    num_topics = int(sys.argv[3]) if len(sys.argv) > 3 else 25
    
    # Check if input file exists
    if not Path(input_csv).exists():
        print(f"Error: Input file '{input_csv}' not found")
        sys.exit(1)
    
    # Read CSV
    print(f"Reading topics from {input_csv}...")
    topics = read_csv(input_csv)
    print(f"Found {len(topics)} topics")
    
    # Generate HTML
    print(f"Generating HTML for top {num_topics} topics...")
    html = generate_html(topics, num_topics)
    
    # Write output
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Poster generated: {output_html}")
    print(f"  Open this file in your browser to view the poster")


if __name__ == '__main__':
    main()
