#!/usr/bin/env python3
"""
Script to migrate blog posts from Java Adventure Blogspot to Hugo markdown files.
Scrapes the blog and creates properly formatted Hugo posts.
"""

import re
import os
import requests
from datetime import datetime
from pathlib import Path
import html
from bs4 import BeautifulSoup
import time

def fetch_blog_content(url):
    """Fetch the blog content from the URL."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def clean_content(content):
    """Clean and convert HTML content to markdown."""
    # Remove script and style elements
    for script in content(["script", "style"]):
        script.decompose()
    
    # Get text content
    text = content.get_text()
    
    # Clean up whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)
    
    return text

def extract_posts_from_page(soup):
    """Extract blog posts from a single page."""
    posts = []
    
    # Find post containers - adjust selector based on actual HTML structure
    post_containers = soup.find_all('div', class_='post')
    if not post_containers:
        # Try alternative selectors
        post_containers = soup.find_all('article')
        if not post_containers:
            post_containers = soup.find_all('div', class_='blog-post')
    
    for container in post_containers:
        try:
            # Extract title
            title_elem = container.find('h1') or container.find('h2') or container.find('h3')
            if not title_elem:
                continue
                
            title = title_elem.get_text().strip()
            
            # Extract date
            date_elem = container.find('time') or container.find(class_=re.compile('date|time'))
            date_str = "2006-01-01"  # Default
            
            if date_elem:
                date_text = date_elem.get_text()
                # Parse various date formats
                date_match = re.search(r'(\d{1,2})(?:st|nd|rd|th)?\s+(\w+)\s+(\d{4})', date_text)
                if date_match:
                    day = date_match.group(1).zfill(2)
                    month_name = date_match.group(2)
                    year = date_match.group(3)
                    
                    month_names = {
                        'January': '01', 'February': '02', 'March': '03', 'April': '04',
                        'May': '05', 'June': '06', 'July': '07', 'August': '08',
                        'September': '09', 'October': '10', 'November': '11', 'December': '12',
                        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                        'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                        'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
                    }
                    month = month_names.get(month_name, '01')
                    date_str = f"{year}-{month}-{day}"
            
            # Extract content
            content_elem = container.find('div', class_='post-body') or container
            content = clean_content(content_elem)
            
            # Extract tags
            tags = []
            labels_elem = container.find(class_=re.compile('label|tag'))
            if labels_elem:
                tag_links = labels_elem.find_all('a')
                tags = [link.get_text().strip() for link in tag_links]
            
            posts.append({
                'title': title,
                'date': date_str,
                'tags': tags,
                'content': content
            })
            
        except Exception as e:
            print(f"Error processing post: {e}")
            continue
    
    return posts

def get_all_archive_urls(base_url):
    """Get all archive page URLs."""
    urls = [base_url]
    
    # Try to find archive links
    try:
        soup = BeautifulSoup(fetch_blog_content(base_url), 'html.parser')
        archive_links = soup.find_all('a', href=re.compile(r'archive\.html|_archive\.html'))
        
        for link in archive_links:
            href = link.get('href')
            if href.startswith('http'):
                urls.append(href)
            else:
                urls.append(f"{base_url.rstrip('/')}/{href.lstrip('/')}")
                
    except Exception as e:
        print(f"Could not fetch archive URLs: {e}")
    
    return list(set(urls))

def create_hugo_post(post, output_dir):
    """Create a Hugo markdown file for a blog post."""
    # Create filename from date and title
    title_slug = re.sub(r'[^\w\s-]', '', post['title'].lower())
    title_slug = re.sub(r'[-\s]+', '-', title_slug).strip('-')
    filename = f"{post['date']}-{title_slug}.md"
    
    # Create frontmatter
    frontmatter = f"""---
title: "{post['title']}"
date: {post['date']}T00:00:00Z"""
    
    if post['tags']:
        tags_str = ', '.join([f'"{tag}"' for tag in post['tags']])
        frontmatter += f"\ntags: [{tags_str}]"
    
    frontmatter += "\n---\n\n"
    
    # Create full content
    full_content = frontmatter + post['content']
    
    # Write file
    output_path = output_dir / filename
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print(f"Created: {filename}")

def main():
    """Main function to migrate all blog posts."""
    blog_url = "https://javaadventure.blogspot.com/"
    
    # Create output directory
    output_dir = Path('content/posts')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("Fetching blog content...")
    
    # Get all archive URLs
    urls = get_all_archive_urls(blog_url)
    
    all_posts = []
    
    for url in urls:
        print(f"Processing: {url}")
        try:
            html_content = fetch_blog_content(url)
            soup = BeautifulSoup(html_content, 'html.parser')
            posts = extract_posts_from_page(soup)
            all_posts.extend(posts)
            
            # Be nice to the server
            time.sleep(1)
            
        except Exception as e:
            print(f"Error processing {url}: {e}")
            continue
    
    # Remove duplicates based on title and date
    seen = set()
    unique_posts = []
    for post in all_posts:
        key = (post['title'], post['date'])
        if key not in seen:
            seen.add(key)
            unique_posts.append(post)
    
    # Sort by date
    unique_posts.sort(key=lambda x: x['date'])
    
    print(f"\nCreating {len(unique_posts)} blog posts...")
    
    for post in unique_posts:
        create_hugo_post(post, output_dir)
    
    print(f"\nMigration complete! Created {len(unique_posts)} posts.")

if __name__ == "__main__":
    main()
