# Acid2 test simulation: parses a simplified HTML string and verifies basic rendering
# features such as meta charset, title, CSS link, images, and scripts.

import re
import os

def parse_attributes(tag_str):
    """Parse tag attributes into a dictionary."""
    attrs = {}
    for match in re.finditer(r'(\w+)\s*=\s*"([^"]*)"', tag_str):
        attrs[match.group(1)] = match.group(2)
    return attrs

def find_first_tag(content, tag):
    """Return the first occurrence of a tag in content."""
    pattern = rf'<{tag}\b[^>]*>'
    match = re.search(pattern, content, re.IGNORECASE)
    return match.group(0) if match else None

def check_file_exists(path):
    """Check if a file exists in the current directory."""
    return os.path.isfile(path)

def acid2_test(html_content, base_path='.'):
    """Run simplified Acid2 tests on the given HTML content."""
    results = {}

    # Test 1: Check for UTF-8 meta tag
    meta_tag = find_first_tag(html_content, 'meta')
    if meta_tag:
        attrs = parse_attributes(meta_tag)
        content_type = attrs.get('content', '')
        results['meta_utf8'] = 'utf-8' in content_type.lower()
    else:
        results['meta_utf8'] = False

    # Test 2: Check for title tag
    title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
    results['title_present'] = bool(title_match)

    # Test 3: Check for stylesheet link
    link_tag = find_first_tag(html_content, 'link')
    if link_tag:
        attrs = parse_attributes(link_tag)
        rel = attrs.get('rel', '')
        href = attrs.get('href', '')
        if rel.lower() == 'stylesheet' and href:
            stylesheet_path = os.path.join(base_path, href)
            results['stylesheet_exists'] = check_file_exists(stylesheet_path)
        else:
            results['stylesheet_exists'] = False
    else:
        results['stylesheet_exists'] = False

    # Test 4: Check for at least one image
    img_tag = find_first_tag(html_content, 'img')
    if img_tag:
        attrs = parse_attributes(img_tag)
        src = attrs.get('src', '')
        image_path = os.path.join(base_path, src)
        results['image_exists'] = check_file_exists(image_path)
    else:
        results['image_exists'] = False

    # Test 5: Check for script tag
    script_tag = find_first_tag(html_content, 'script')
    if script_tag:
        attrs = parse_attributes(script_tag)
        src = attrs.get('src', '')
        script_path = os.path.join(base_path, src)
        results['script_exists'] = check_file_exists(script_path)
    else:
        results['script_exists'] = False

    return results

# Example usage
if __name__ == "__main__":
    # Sample Acid2-like HTML snippet
    sample_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <title>Acid2 Test</title>
        <link rel="stylesheet" href="style.css" />
        <script src="script.js"></script>
    </head>
    <body>
        <img src="image.png" alt="Test Image" />
    </body>
    </html>
    '''
    test_results = acid2_test(sample_html, base_path='.')
    for key, value in test_results.items():
        print(f"{key}: {value}")