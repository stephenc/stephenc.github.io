#!/usr/bin/env python3
"""
Script to migrate blog posts from Java Adventure Blogspot to Hugo markdown files.
Scrapes the blog and creates properly formatted Hugo posts.

Usage:
    uv pip install -r requirements.txt
    python3 scripts/migrate-blog.py
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
    
    # Debug: Print some HTML structure to understand the page
    print("Looking for post containers...")
    
    # First, let's see what we're working with
    title_tag = soup.find('title')
    if title_tag:
        print(f"Page title: {title_tag.get_text()}")
    
    # Look for all links that might be blog post links
    all_links = soup.find_all('a', href=True)
    blog_post_links = []
    for link in all_links:
        href = link.get('href', '')
        if 'javaadventure.blogspot.com' in href and '/20' in href and '.html' in href:
            blog_post_links.append(link)
    
    print(f"Found {len(blog_post_links)} potential blog post links")
    
    # Blogspot uses different selectors - try multiple approaches
    selectors_to_try = [
        'div.post',
        'div[class*="post"]',
        'article',
        'div.blog-post',
        'div.hentry',
        'div.entry',
        '.post-outer',
        '.blog-posts .post',
        '.post-title',
        'h1 a[href*="blogspot.com"]',
        'h2 a[href*="blogspot.com"]',
        'h3 a[href*="blogspot.com"]'
    ]
    
    post_containers = []
    for selector in selectors_to_try:
        containers = soup.select(selector)
        if containers:
            print(f"Found {len(containers)} containers with selector: {selector}")
            post_containers = containers
            break
    
    if not post_containers:
        # Fallback: look for any element containing blog post links
        print("Trying fallback approach...")
        for link in blog_post_links:
            # Find the parent container that likely contains the full post
            parent = link.parent
            while parent and parent.name != 'body':
                # Look for a container that seems to hold a full post
                if parent.name in ['div', 'article', 'section']:
                    text_content = parent.get_text()
                    if len(text_content) > 100:  # Likely contains post content
                        post_containers.append(parent)
                        break
                parent = parent.parent
        
        # Remove duplicates
        post_containers = list(set(post_containers))
        print(f"Found {len(post_containers)} posts via fallback")
    
    for container in post_containers:
        try:
            # Extract title - look for header with link
            title_elem = None
            title = ""
            post_url = ""
            
            # Look for title in various ways
            for header_tag in ['h1', 'h2', 'h3']:
                header = container.find(header_tag)
                if header:
                    link = header.find('a')
                    if link and 'blogspot.com' in link.get('href', ''):
                        title_elem = header
                        title = header.get_text().strip()
                        post_url = link.get('href', '')
                        break
            
            # If no title found in headers, look for any link to a blog post
            if not title:
                link = container.find('a', href=lambda x: x and 'javaadventure.blogspot.com' in x and '.html' in x)
                if link:
                    title = link.get_text().strip()
                    post_url = link.get('href', '')
            
            if not title:
                continue
                
            print(f"Found post: {title}")
            print(f"URL: {post_url}")
            
            # Extract date - look for various date patterns
            date_str = "2006-01-01"  # Default
            
            # First try to extract from URL
            if post_url:
                url_date_match = re.search(r'/(\d{4})/(\d{2})/[^/]+\.html', post_url)
                if url_date_match:
                    year, month = url_date_match.group(1), url_date_match.group(2)
                    date_str = f"{year}-{month}-01"
                    print(f"Extracted date from URL: {date_str}")
            
            # If URL date extraction failed, look in text content
            if date_str == "2006-01-01":
                date_text = container.get_text()
                date_patterns = [
                    r'Posted.*?(\d{1,2})(?:st|nd|rd|th)?\s+(\w+)\s+(\d{4})',
                    r'(\d{1,2})(?:st|nd|rd|th)?\s+(\w+)\s+(\d{4})',
                    r'(\w+)\s+(\d{1,2})(?:st|nd|rd|th)?\s*,?\s*(\d{4})'
                ]
                
                for pattern in date_patterns:
                    date_match = re.search(pattern, date_text)
                    if date_match:
                        if date_match.group(1).isdigit():  # Day first
                            day = date_match.group(1).zfill(2)
                            month_name = date_match.group(2)
                            year = date_match.group(3)
                        else:  # Month first
                            month_name = date_match.group(1)
                            day = date_match.group(2).zfill(2)
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
                        print(f"Extracted date from text: {date_str}")
                        break
            
            # Extract content - get the main text content
            content = ""
            
            # Remove title and metadata from content
            content_container = container
            
            # Try to find the main content area
            content_elem = (container.find('div', class_='post-body') or 
                          container.find('div', class_='entry-content') or
                          container.find('div', class_='post-content') or
                          container)
            
            if content_elem:
                # Remove script, style, and navigation elements
                for elem in content_elem(['script', 'style', 'nav', 'header', 'footer']):
                    elem.decompose()
                
                # Get text and clean it up
                content = content_elem.get_text()
                
                # Clean up the content
                lines = content.split('\n')
                cleaned_lines = []
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('Posted') and 'Add a comment' not in line:
                        cleaned_lines.append(line)
                
                content = '\n\n'.join(cleaned_lines)
            
            # Extract tags
            tags = []
            labels_text = container.get_text()
            if 'Labels:' in labels_text:
                labels_match = re.search(r'Labels:\s*([^\n]+)', labels_text)
                if labels_match:
                    # Simple extraction - just look for common tag names
                    tag_text = labels_match.group(1)
                    common_tags = ['Java', 'Maven', 'Jenkins', 'Shell', 'JavaEE', 'CloudBees']
                    for tag in common_tags:
                        if tag in tag_text:
                            tags.append(tag)
            
            if title and content:
                posts.append({
                    'title': title,
                    'date': date_str,
                    'tags': tags,
                    'content': content.strip()
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
