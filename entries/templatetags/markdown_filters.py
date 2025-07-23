from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter(name='markdown')
def markdown(value):
    """Convert markdown text to HTML"""
    if not value:
        return ""
    
    # Convert markdown to HTML
    html = value
    
    # Headers
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # Bold and italic
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    
    # Links
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)
    
    # Images
    html = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1" class="img-fluid">', html)
    
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
    text = re.sub(r'^- ', '', text, flags=re.MULTILINE)
    
    return text.strip() 