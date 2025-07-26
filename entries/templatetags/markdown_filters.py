from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

def convert_video_url(match):
    """Convert video URLs to video players"""
    url = match.group(1)
    # Check if URL points to a video file
    video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv', '.m4v', '.mpeg']
    if any(url.lower().endswith(ext) for ext in video_extensions):
        return f'<video controls class="w-100 rounded" style="max-height: 400px;" preload="metadata"><source src="{url}" type="video/mp4">Your browser does not support the video tag.</video>'
    return match.group(0)  # Return original if not a video

@register.filter(name='markdown')
def markdown(value):
    """Convert markdown text to HTML, preserving existing HTML"""
    if not value:
        return ""
    
    # If the content already contains HTML img tags, preserve them
    if '<img' in value:
        # The content contains HTML img tags, so we need to be careful
        # First, let's protect existing HTML img tags
        img_tags = []
        def protect_img(match):
            img_tags.append(match.group(0))
            return f"__IMG_TAG_{len(img_tags)-1}__"
        
        # Protect existing HTML img tags
        value = re.sub(r'<img[^>]+>', protect_img, value)
        
        # Now process markdown
        html = value
        
        # Headers
        html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        
        # Bold and italic
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
        
        # Images (markdown syntax) - MUST come BEFORE links
        html = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1" class="img-fluid">', html)
        
        # Videos (markdown syntax) - MUST come BEFORE links
        html = re.sub(r'@\[(.*?)\]\((.*?)\)', r'<video controls class="w-100 rounded" style="max-height: 400px;" preload="metadata"><source src="\2" type="video/mp4">Your browser does not support the video tag.</video>', html)
        
        # Links - MUST come AFTER images and videos
        html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)
        
        # Convert video URLs to video players
        html = re.sub(r'<a[^>]*href="([^"]*\.(?:mp4|avi|mov|wmv|flv|webm|mkv|m4v|mpeg))"[^>]*>.*?</a>', convert_video_url, html, flags=re.IGNORECASE | re.DOTALL)
        
        # Lists
        html = re.sub(r'^- (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        html = re.sub(r'(\n<li>.*?</li>\n)+', lambda m: f'<ul>{m.group(0)}</ul>', html, flags=re.DOTALL)
        
        # Line breaks
        html = html.replace('\n', '<br>')
        
        # Restore protected img tags
        for i, tag in enumerate(img_tags):
            html = html.replace(f"__IMG_TAG_{i}__", tag)
        
        return mark_safe(html)
    else:
        # Pure markdown content, process normally
        html = value
        
        # Headers
        html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        
        # Bold and italic
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
        
        # Images (markdown syntax) - MUST come BEFORE links
        html = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1" class="img-fluid">', html)
        
        # Videos (markdown syntax) - MUST come BEFORE links
        html = re.sub(r'@\[(.*?)\]\((.*?)\)', r'<video controls class="w-100 rounded" style="max-height: 400px;" preload="metadata"><source src="\2" type="video/mp4">Your browser does not support the video tag.</video>', html)
        
        # Links - MUST come AFTER images and videos
        html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)
        
        # Convert video URLs to video players
        html = re.sub(r'<a[^>]*href="([^"]*\.(?:mp4|avi|mov|wmv|flv|webm|mkv|m4v|mpeg))"[^>]*>.*?</a>', convert_video_url, html, flags=re.IGNORECASE | re.DOTALL)
        
        # Lists
        html = re.sub(r'^- (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        html = re.sub(r'(\n<li>.*?</li>\n)+', lambda m: f'<ul>{m.group(0)}</ul>', html, flags=re.DOTALL)
        
        # Line breaks
        html = html.replace('\n', '<br>')
        
        return mark_safe(html)

@register.filter(name='plain_text')
def plain_text(value):
    """Extract plain text from HTML or markdown"""
    if not value:
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', value)
    
    # Remove markdown syntax
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    text = re.sub(r'!\[(.*?)\]\(.*?\)', r'\1', text)
    text = re.sub(r'@\[(.*?)\]\(.*?\)', r'\1', text)  # Also remove video markdown syntax
    text = re.sub(r'^- ', '', text, flags=re.MULTILINE)
    
    return text.strip() 