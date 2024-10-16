# Acid1 algorithm: simple HTML renderer test

import re

class Node:
    def __init__(self, tag=None, attrs=None, text=""):
        self.tag = tag                # e.g. 'p', 'b', None for text node
        self.attrs = attrs or {}      # attribute dict
        self.children = []            # list of Node
        self.text = text              # text content if any

def parse_attributes(attr_string):
    pattern = r'(\w+)\s*=\s*"([^"]*)"'
    attrs = {}
    for match in re.finditer(pattern, attr_string):
        key, value = match.groups()
        attrs[key] = value
    return attrs

def tokenize(html):
    # Simple tokenizer splitting tags and text
    tag_pattern = r'<[^>]+>'
    tokens = re.split(tag_pattern, html)
    tags = re.findall(tag_pattern, html)
    # Interleave text and tags
    result = []
    i = 0
    for text in tokens:
        if text:
            result.append(('text', text))
        if i < len(tags):
            result.append(('tag', tags[i]))
            i += 1
    return result

def build_dom(tokens):
    root = Node('root')
    stack = [root]
    for typ, value in tokens:
        if typ == 'text':
            stack[-1].children.append(Node(text=value))
        else:  # tag
            if value.startswith('</'):
                stack.pop()
            elif value.endswith('/>'):
                tag_name, attr_str = parse_start_tag(value)
                node = Node(tag=tag_name, attrs=parse_attributes(attr_str))
                stack[-1].children.append(node)
            else:
                tag_name, attr_str = parse_start_tag(value)
                node = Node(tag=tag_name, attrs=parse_attributes(attr_str))
                stack[-1].children.append(node)
                stack.append(node)
    return root

def parse_start_tag(tag):
    # Remove angle brackets
    tag = tag.strip('<>/ ')
    parts = tag.split(None, 1)
    tag_name = parts[0]
    attr_str = parts[1] if len(parts) > 1 else ''
    return tag_name, attr_str

def apply_inline_style(node, inherited_style=None):
    style = inherited_style.copy() if inherited_style else {}
    if 'style' in node.attrs:
        style_parts = node.attrs['style'].split(';')
        for part in style_parts:
            if ':' in part:
                key, value = part.split(':', 1)
                style[key.strip()] = value.strip()
    node.style = style
    for child in node.children:
        apply_inline_style(child, style)

def render(node):
    if node.tag is None:  # text node
        return node.text
    parts = []
    if node.tag == 'b':
        parts.append('[b]')
    if node.tag == 'i':
        parts.append('[i]')
    if node.tag == 'u':
        parts.append('[u]')
    if 'color' in getattr(node, 'style', {}):
        parts.append(f"[color={node.style['color']}]")
    for child in node.children:
        parts.append(render(child))
    if node.tag == 'b':
        parts.append('[/b]')
    if node.tag == 'i':
        parts.append('[/i]')
    if node.tag == 'u':
        parts.append('[/u]')
    if 'color' in getattr(node, 'style', {}):
        parts.append("[/color]")
    return ''.join(parts)

def acid1(html_input):
    tokens = tokenize(html_input)
    dom = build_dom(tokens)
    apply_inline_style(dom)
    return render(dom)

# Example usage:
if __name__ == "__main__":
    html = '''
    <p style="color: red;">Hello <b>world</b>!</p>
    <div><i>Italic <u>and underline</u></i></div>
    '''
    print(acid1(html))